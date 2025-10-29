from grammer.TtlParserLexer import TtlParserLexer
from grammer.TtlParserParser import TtlParserParser
from antlr4.InputStream import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.tree.Tree import ParseTreeVisitor
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException
import time
import paramiko
import socket
import re
import subprocess


class TtlContinueFlagException(Exception):
    """ continue 用の例外 """
    def __init__(self, message):
        """ コンストラクタ """
        super().__init__(message)


class TtlBreakFlagException(Exception):
    """ break 用の例外 """
    def __init__(self, message):
        """ コンストラクタ """
        super().__init__(message)


class TtlReturnFlagException(Exception):
    """ return 用の例外 """
    def __init__(self, message):
        """ コンストラクタ """
        super().__init__(message)


class TtlExitFlagException(Exception):
    """ exit 用の例外 """
    def __init__(self, message):
        """ コンストラクタ """
        super().__init__(message)


class TtlParseTreeVisitor(ParseTreeVisitor):
    def visit(self, tree):
        return tree.accept(self)

    def visitChildren(self, node):
        result = {}
        result['name'] = node.__class__.__name__
        line_number = node.start.line
        result['line'] = line_number
        #
        n = node.getChildCount()
        if n == 0:
            return result
        worker_list = []
        for i in range(n):
            c = node.getChild(i)
            childResult = c.accept(self)
            if childResult is not None:
                worker_list.append(childResult)
        if worker_list != 0:
            result["child"] = worker_list
        return result

    def visitTerminal(self, node):
        type = node.getSymbol().type
        # print(f"visitErrorNode type={type} text={node.getText()}")
        if type < 0:
            return None
        x = TtlParserLexer.ruleNames[type - 1]
        if x == "RN" or x == "WS":
            return None
        return node.getText()

    def visitErrorNode(self, node):
        x = node.getSymbol().type
        x = TtlParserLexer.ruleNames[x - 1]
        y = node.getText()
        raise TypeError(f"visitErrorNode type={x} text={y}")


class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise TypeError(f"Token recognition error at line {line}:{column} - {msg}")


class TtlPaserWolker():
    """ tera tekitou lang の実装部分(GUI除く) """
    def __init__(self):
        """" init """
        self.value_list = {}
        self.result_file_json = {}
        self.end_flag = False
        self.client = None
        self.shell = None
        self.stdout = ''
        self.process = None

    def stop(self, error=None):
        """ 強制停止処理 """
        if error is not None:
            self.setValue('error', error)
            self.setValue('result', 0)
        self.end_flag = True
        #
        # SSH接続していたら止める
        self.closeClient()

    def closeClient(self):
        """ SSH接続していたら止める """
        # print("closeClient()")
        self.stdout = ''
        #
        client = self.client
        self.client = None
        if client is not None:
            try:
                client.close()
            except Exception:
                # どんなエラーがでようと必ず殺す
                pass
                client = self.client
        shell = self.shell
        self.shell = None
        if shell is not None:
            try:
                shell.close()
            except Exception:
                # どんなエラーがでようと必ず殺す
                pass
        process = self.process
        self.process = None
        if process is not None:
            try:
                process.terminate()
            except Exception:
                # どんなエラーがでようと必ず殺す
                pass

    def execute(self, filename: str, param_list: list):
        try:
            #
            # default値の設定
            self.setValue('error', "")
            self.setValue('result', 1)
            #
            # 初期パラメータの設定
            i = 0
            # print(f" data={json.dumps(param_list, indent=2)}")
            for param in param_list:
                self.setValue('param' + str(i), param)
                i = i + 1
            #
            # 一発目のinclude
            self.include(filename)
            #
        finally:
            # なにがあろうとセッションは必ず殺す
            self.closeClient()

    def include(self, filename: str):
        if self.end_flag:
            return
        try:
            #
            result_json = {}
            # print(f"filename={filename} param={self.result_file_json}")        
            if filename in self.result_file_json:
                result_json = self.result_file_json[filename]
            else:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = f.read()
                input_stream = InputStream(data)
                lexer = TtlParserLexer(input_stream)
                lexer.removeErrorListeners()
                lexer.addErrorListener(ThrowingErrorListener())
                token_stream = CommonTokenStream(lexer)
                parser = TtlParserParser(token_stream)
                #
                # パーサが失敗していたら止める
                parser._errHandler = BailErrorStrategy()
                #
                tree = parser.statement()
                visitor = TtlParseTreeVisitor()
                result_json = tree.accept(visitor)
                #
                # for call command
                self.result_file_json[filename] = result_json
                #
            self.execute_result(result_json['child'])
            #
        except TtlExitFlagException:
            # exitコマンドが呼び出されときは正常終了です
            pass
        except ParseCancellationException as e:
            self.stop(f"ParseCancellationException f={filename} e={e}")
        except TypeError as e:
            self.stop(f"TypeError f={filename} e={e}")
        except KeyError as e:
            self.stop(f"KeyError f={filename} e={e}")
        except Exception as e:
            self.stop(f"{type(e).__name__} f={filename} e={e} error!")
        #

    def setValue(self, strvar: str, data):
        # print(f"bbb strvar={strvar} data={data}")
        self.value_list[strvar] = data

    def getValue(self, strvar: str, error_stop=True):
        if strvar not in self.value_list:
            if error_stop:
                self.stop(error=f"Value not found err value={strvar}")
            return None
        return self.value_list[strvar]

    def execute_result(self, x_list, ifFlag=1):
        """execute_result"""
        if self.end_flag:
            return
        for x in x_list:
            name = x['name']
            line = x['line']
            # print(f"CommandlineContext name={name}")
            if 'CommandlineContext' == name:
                if ifFlag != 0:
                    self.commandlineContext(x['child'])
            elif 'ElseifContext' == name:
                if ifFlag == 0:
                    first = int(self.getData(x['child'][1]))
                    if first != 0:
                        self.execute_result(x['child'][3:])
                        ifFlag = 1
            elif 'ElseContext' == name:
                if ifFlag == 0:
                    self.execute_result(x['child'][1:])
            else:
                self.stop(error=f"execute_result Unkown name={name} line={line} x={x}")
            if self.end_flag:
                break

    def commandlineContext(self, token_list):
        for x in token_list:
            # print(f"commandlineContext data={json.dumps(x, indent=2)}")
            name = x['name']
            line = x['line']
            if 'InputContext' == name:
                strvar = x['child'][0]
                data = x['child'][2]
                data = self.getData(data)
                self.setValue(strvar, data)
            elif 'CommandContext' == name:
                command_name = x['child'][0]
                if "dummy" == command_name:
                    print(f"### l={line} c={name}", end="")
                    for data in x['child'][1:]:
                        result = self.getData(data)
                        print(f" p={result}", end="")
                    print()
                elif "break" == command_name:
                    raise TtlBreakFlagException("break")
                elif "continue" == command_name:
                    raise TtlContinueFlagException("Continue")
                elif "end" == command_name:
                    self.end_flag = True
                elif "exit" == command_name:
                    raise TtlExitFlagException("exit")
                elif "return" == command_name:
                    raise TtlReturnFlagException("return")
                elif "include" == command_name:
                    filename = self.getData(x['child'][1])
                    self.include(filename)
                elif "call" == command_name:
                    label = x['child'][1]
                    # print(f"call label={label}")
                    self.callContext(label)
                elif "str2int" == command_name:
                    left = x['child'][1]
                    right = int(self.getData(x['child'][2]))
                    # print(f"left={left} right={right}")
                    self.setValue(left, right)
                elif "strcompare" == command_name:
                    left = str(self.getData(x['child'][1]))
                    right = str(self.getData(x['child'][2]))
                    result = 0
                    if left == right:
                        result = 0
                    elif left < right:
                        result = -1
                    else:
                        result = 1
                    self.setValue('result', result)
                elif "strconcat" == command_name:
                    left = x['child'][1]
                    left_str = self.getValue(left)
                    right_str = x['child'][2]
                    left_str = left_str + self.getData(right_str)
                    self.setValue(left, left_str)
                elif "strlen" == command_name:
                    left = len(self.getData(x['child'][1]))
                    self.setValue('result', left)
                elif "strscan" == command_name:
                    left = str(self.getData(x['child'][1]))
                    right = str(self.getData(x['child'][2]))
                    index = left.find(right)
                    if index < 0:
                        result = 0
                    else:
                        index = index + 1
                    self.setValue('result', index)
                elif "mpause" == command_name:
                    left = int(self.getData(x['child'][1]))
                    left = left / 1000.0
                    time.sleep(left - int(left))  # 小数点以下を眠る
                    for _ in range(int(left)):
                        time.sleep(1)
                        if self.end_flag:
                            break
                elif "pause" == command_name:
                    left = int(self.getData(x['child'][1]))
                    for _ in range(int(left)):
                        time.sleep(1)
                        if self.end_flag:
                            break
                elif 'connect' == command_name:
                    self.doConnect(self.getData(x['child'][1]), line)
                elif 'closett' == command_name or 'disconnect' == command_name:
                    self.closeClient()
                elif 'testlink' == command_name:
                    self.doTestlink()
                elif 'send' == command_name:
                    self.doSend(x['child'][1:])
                elif 'sendln' == command_name:
                    self.doSendln(x['child'][1:])
                elif 'wait' == command_name:
                    self.doWait(x['child'][1:])
                elif 'waitln' == command_name:
                    self.doWaitln(x['child'][1:])
                else:
                    # コマンドが分からない
                    self.commandContext(command_name, line, x['child'][1:])
            elif 'ForNextContext' == name:
                self.forNextContext(x['child'])
            elif 'WhileEndwhileContext' == name:
                self.whileEndwhileContext(x['child'])
            elif 'UntilEnduntilContext' == name:
                self.untilEnduntilContext(x['child'])
            elif 'DoLoopContext' == name:
                self.doLoopContext(x['child'])
            elif 'If1Context' == name:
                self.if1Context(x['child'])
            elif 'If2Context' == name:
                self.if2Context(x['child'])
            elif 'LabelContext' != name:
                pass
            else:
                self.stop(error=f"Unkown name={name} line={line}")
            if self.end_flag:
                break

    def commandContext(self, name, line, data_list):
        self.stop(error=f"Unsupport command n={name} line={line}")

    def callContext(self, label):
        #
        try:
            for token_list in self.result_file_json.values():
                token_list = token_list['child']  # StatementContext
                i = 0
                label_found_flag = True
                while i < len(token_list):
                    targetContext = token_list[i]['child']
                    if label_found_flag:
                        j = 0
                        while j < len(targetContext):
                            # print(f"xxx data={json.dumps(targetContext, indent=2)}")
                            context = targetContext[j]
                            name = context['name']
                            if 'LabelContext' == name:
                                label_name = context['child']
                                if label == label_name[1]:
                                    label_found_flag = False
                                    break
                            j = j + 1
                            if self.end_flag:
                                break
                    else:
                        self.commandlineContext(targetContext)
                    i = i + 1
                    if not label_found_flag:
                        break
                    if self.end_flag:
                        break
                if not label_found_flag:
                    break
                if self.end_flag:
                    break
            if label_found_flag:
                # 一つもヒットしていない
                self.stop(error=f"No hit label error label={label}")
        except TtlReturnFlagException:
            pass
        #

    def forNextContext(self, data_list):
        intvar = data_list[1]
        first = int(self.getData(data_list[2]))
        self.setValue(intvar, first)
        last = int(self.getData(data_list[3]))
        # print(f"for intvar={intvar} first={first} last={last}")
        add = -1
        if first < last:
            add = 1
        while True:
            #
            try:
                self.execute_result(data_list[4:-1])
                #
                if self.end_flag:
                    break
                #
                self.setValue(intvar, self.getValue(intvar) + add)
                if (0 < add):
                    if last < self.getValue(intvar):
                        break
                else:
                    if self.getValue(intvar) < last:
                        break
            except TtlContinueFlagException:
                pass
            except TtlBreakFlagException:
                break

    def whileEndwhileContext(self, data_list):
        while int(self.getData(data_list[1])) != 0:
            try:
                #
                self.execute_result(data_list[2:-1])
                #
                if self.end_flag:
                    break
            except TtlContinueFlagException:
                pass
            except TtlBreakFlagException:
                break

    def untilEnduntilContext(self, data_list):
        while int(self.getData(data_list[1])) == 0:
            try:
                #
                self.execute_result(data_list[2:-1])
                #
                if self.end_flag:
                    break
            except TtlContinueFlagException:
                pass
            except TtlBreakFlagException:
                break

    def doLoopContext(self, data_list):
        while True:
            try:
                for data in data_list:
                    if isinstance(data, str):
                        # do/loop
                        # print(f"do/loop={data}")
                        pass
                    elif 'CommandlineContext' == data['name']:
                        # print(f"LineContext={data}")
                        self.execute_result([data])
                    else:
                        # print(f"data={data['name']}")
                        value = int(self.getData(data))
                        # print(f"value ={value}")
                        if value == 0:
                            # print(f"data ok={data}")
                            raise TtlBreakFlagException('doLoopContext')
            except TtlContinueFlagException:
                pass
            except TtlBreakFlagException:
                break

    def if1Context(self, data_list):
        first = int(self.getData(data_list[1]))
        # print(f"if1 first={first}")
        if 0 != first:
            self.execute_result(data_list[2:])

    def if2Context(self, data_list):
        first = int(self.getData(data_list[1]))
        # print(f"if2 first={first}")
        self.execute_result(data_list[3:-1], first)

    def getData(self, data):
        result = ""
        if 'P11ExpressionContext' == data['name']:
            result = self.p11ExpressionContext(data['child'])
        elif 'P10ExpressionContext' == data['name']:
            result = self.p10ExpressionContext(data['child'])
        elif 'P9ExpressionContext' == data['name']:
            result = self.p9ExpressionContext(data['child'])
        elif 'P8ExpressionContext' == data['name']:
            result = self.p8ExpressionContext(data['child'])
        elif 'P7ExpressionContext' == data['name']:
            result = self.p8ExpressionContext(data['child'])
        elif 'P6ExpressionContext' == data['name']:
            result = self.p7ExpressionContext(data['child'])
        elif 'P6ExpressionContext' == data['name']:
            result = self.p6ExpressionContext(data['child'])
        elif 'P5ExpressionContext' == data['name']:
            result = self.p5ExpressionContext(data['child'])
        elif 'P4ExpressionContext' == data['name']:
            result = self.p4ExpressionContext(data['child'])
        elif 'P3ExpressionContext' == data['name']:
            result = self.p3ExpressionContext(data['child'])
        elif 'P2ExpressionContext' == data['name']:
            result = self.p2ExpressionContext(data['child'])
        elif 'P1ExpressionContext' == data['name']:
            result = self.p1ExpressionContext(data['child'])
        elif 'IntExpressionContext' == data['name']:
            result = self.intExpressionContext(data['child'])
        elif 'StrExpressionContext' == data['name']:
            result = self.strExpressionContext(data['child'])
        elif 'IntContextContext' == data['name']:
            result = self.intContext(data['child'])
        elif 'StrContextContext' == data['name']:
            result = self.strContext(data['child'])
        elif 'KeywordContext' == data['name']:
            result = self.keywordContext(data['child'])
        else:
            self.stop(error=f"unkown keyword n={data['name']}")
            result = data
        return result

    def p11ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = self.getData(data[0])
        val2 = self.getData(data[2])
        return val1 or val2

    def p10ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = self.getData(data[0])
        val2 = self.getData(data[2])
        return val1 and val2

    def p9ExpressionContext(self, data: list):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        # print(f"p9ExpressionContext count={count} data={data[0]['name']} child={data[0]['child'][0]} ")
        # print("xxx 1")
        val1 = int(self.getData(data[0]))
        # print("xxx 2")
        oper = data[1]
        # print(f"p9ExpressionContext count={1} data={oper}")
        # print(f"p9ExpressionContext count={2} data={data[2]['name']} child={data[2]['child']} ")
        val2 = int(self.getData(data[2]))
        result = 0
        if '==' == oper or '=' == oper:
            result = val1 == val2
        else:  # <> or !=
            result = val1 != val2
        if result:
            return 1
        return 0

    def p8ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        oper = data[1]
        val2 = int(self.getData(data[2]))
        result = 0
        if '<' == oper:
            result = val1 < val2
        elif '<=' == oper:
            result = val1 <= val2
        elif '>' == oper:
            result = val1 > val2
        else:  # '>='
            result = val1 >= val2
        if result:
            return 1
        return 0

    def p7ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        val2 = int(self.getData(data[2]))
        result = val1 or val2
        if result:
            return 1
        return 0

    def p6ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        val2 = int(self.getData(data[2]))
        result = val1 ^ val2
        if result:
            return 1
        return 0

    def p5ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        val2 = int(self.getData(data[2]))
        result = val1 and val2
        if result:
            return 1
        return 0

    def p4ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        oper = data[1]
        val2 = int(self.getData(data[2]))
        result = 0
        if '>>>' == oper:
            result = val1 >> val2
        elif '>>' == oper:
            result = val1 >> val2
        elif '<<' == oper:
            result = val1 << val2
        return result

    def p3ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        oper = data[1]
        val2 = int(self.getData(data[2]))
        result = 0
        if '+' == oper:
            result = val1 + val2
        elif '-' == oper:
            result = val1 - val2
        return result

    def p2ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[0]))
        oper = data[1]
        val2 = int(self.getData(data[2]))
        result = 0
        if '*' == oper:
            result = val1 * val2
        elif '/' == oper:
            result = val1 / val2
        elif '%' == oper:
            result = val1 % val2
        return result

    def p1ExpressionContext(self, data):
        count = len(data)
        if count == 1:
            return self.getData(data[0])
        val1 = int(self.getData(data[1]))
        if 0 == val1:
            return 1
        return 0

    def intExpressionContext(self, data_list):
        count = len(data_list)
        if count == 1:
            return self.getData(data_list[0])
        # ()表現=data_list[0]には'('が入っている
        return self.getData(data_list[1])

    def strExpressionContext(self, data_list):
        return self.getData(data_list[0])

    def strContext(self, data_list):
        # print(f"str={data_list}")
        result = ""
        for data in data_list:
            state = 0
            base = ''
            sharp_flag = False
            for i in range(len(data)):
                ch0 = data[i]
                if state == 0:
                    if ch0 == '\'':
                        state = 1
                    elif ch0 == '\"':
                        state = 2
                    elif ch0 == '#' or ch0 == '$':
                        state = 0
                        sharp_flag = True
                    if state != 0 or sharp_flag:
                        if 0 < len(base):
                            if '#' == base[0]:
                                base = chr(self.getAsciiNum(data[1:]))
                            elif '$' == data[0]:
                                base = self.getAsciiNum(data[1:])
                        base = base + ch0
                        base = ''
                    else:
                        base = base + ch0
                elif state == 1:
                    if ch0 == '\'':
                        state = 0
                    else:
                        result = result + ch0
                elif state == 2:
                    if ch0 == '\"':
                        state = 0
                    else:
                        result = result + ch0
            if 0 < len(base):
                if '#' == base[0]:
                    base = chr(self.getAsciiNum(data[1:]))
                elif '$' == data[0]:
                    base = self.getAsciiNum(data[1:])
                result = result + base
        return result

    def intContext(self, data_list):
        # print(f"int={data_list}")
        result = 0
        data = data_list[0]
        if 0 < len(data) and data[0] == '$':
            result = self.getAsciiNum(data[1:])
        else:
            result = int(data)
        return result

    def getAsciiNum(self, data):
        if (0 < len(data)) and ('$' == data[0]):
            return int(data[1:], 16)
        return int(data)

    def keywordContext(self, data):
        return self.getValue(data[0])

    def doConnect(self, data: str, line):
        ''' 接続する '''
        # print(f"do connect data={data}")
        if self.client is not None:
            self.setValue('error', "Already connected")
            self.setValue('result', 0)
            return
        param_list = re.split(r'[ \t]+', data)
        server = "localhost"
        user = None
        passwd = None
        keyfile = None
        port_number = 22
        param_cmd = False
        for param in param_list:
            if len(param) <= 0:
                continue
            if param[0] != '/':
                server = param.split(':')
                if len(server) == 1:
                    server = server[0]
                elif len(server) == 2:
                    port_number = int(server[1])
                    server = server[0]
                else:
                    self.setValue('error', "Invalid server name")
                    self.setValue('result', 0)
                    return
            else:
                user_string = "user="
                passwd_string = "passwd="
                keyfile_string = "keyfile="
                param = param[1:]
                # print(f"\tparam={param}")
                if 'ssh' == param:
                    pass
                elif '1' == param:
                    self.setValue('error', "SSH1 not support")
                    self.setValue('result', 0)
                    return
                elif '2' == param:
                    pass  # SSH2
                elif 'cmd' == param:
                    param_cmd = True
                elif 'ask4passwd' == param:
                    self.setValue('error', "Not Support ask4passwd error!")
                    self.setValue('result', 0)
                    return
                elif 'auth=password' == param:
                    pass  # わからん
                elif 'auth=publickey' == param:
                    pass  # わからん
                elif 'auth=challenge' == param:
                    pass  # わからん
                elif re.search('^' + user_string, param):
                    user = param[len(user_string):]
                elif re.search('^' + passwd_string, param):
                    passwd = param[len(passwd_string):]
                elif re.search('^' + keyfile_string, param):
                    keyfile = param[len(keyfile_string):]
                else:
                    # 知らないパラメータが来たら停止する
                    self.setValue('error', f"unkown paramater={param}")
                    self.setValue('result', 0)
                    return
        #
        # 前の接続は削除
        self.closeClient()
        #
        # ここから接続処理
        if not param_cmd:
            try:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #
                # print(f"p1 {server}, port={port_number}, username={user}, password={passwd}, key_filename={keyfile}")
                self.client.connect(server, port=port_number, username=user, password=passwd, key_filename=keyfile)
                # print(f"p2 {server}, port={port_number}, username={user}, password={passwd}, key_filename={keyfile}")
                #
                self.shell = self.client.invoke_shell()
                if self.shell is None:
                    raise paramiko.SSHException("shell is None")
                # print(f"p3 {server}, port={port_number}, username={user}, password={passwd}, key_filename={keyfile}")
                #
                # 接続成功
                #
                self.setValue('result', 2)
                # print("connect OK !")
                #
            except socket.gaierror as e:
                self.setValue('error', f"gaierror line={line} e={e}")
                self.setValue('result', 0)
                self.closeClient()
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                self.setValue('error', f"gaierror line={line} e={e}")
                self.setValue('result', 0)
                self.closeClient()
            except paramiko.AuthenticationException as e:
                self.setValue('error', f"AuthenticationException line={line} e={e}")
                self.setValue('result', 0)
                self.closeClient()
            except paramiko.SSHException as e:
                self.setValue('error', f"SSHException line={line} e={e}")
                self.setValue('result', 0)
                self.closeClient()
        else:
            # ここからcmd起動
            self.process = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #
            # 接続成功
            self.setValue('result', 2)
 
    def doTestlink(self):
        if (self.client is None or self.shell is None or not self.shell.active) and (self.process is None):
            self.setValue('result', 0)
        else:
            self.setValue('result', 2)

    def doSend(self, data_list):
        # print(f"doSend() d={data_list}")
        for data in data_list:
            result = self.getData(data)
            self.doSendAll(result)

    def doSendln(self, data_list):
        # print(f"doSendln() d={data_list}")
        if len(data_list) <= 0:
            self.doSendAll("\n")
        else:
            for data in data_list:
                message = self.getData(data)
                self.doSendAll(message + "\n")

    def doSendAll(self, message):
        # print(f"doSendAll d={message}")
        if self.process is None:
            while not self.end_flag:
                shell = self.shell
                if shell is None:
                    # print("doSendAll shell None")
                    break
                elif shell.send_ready():
                    # print(f"send! f=/{message}/")
                    shell.send(message)
                    break
                else:
                    time.sleep(0.1)
        else:
            # ここからCMD
            while not self.end_flag:
                process = self.process
                if process is None:
                    # print("doSendAll shell None")
                    break
                elif process.stdin.writable():
                    # print(f"send! f=/{message}/")
                    process.stdin.write(message)
                    process.stdin.flush()
                    break
                else:
                    time.sleep(0.1)

    def doWait(self, data_list):
        result_list = []
        for data in data_list:
            result = self.getData(data)
            result_list.append(result)
        self.doWaitAll(result_list)

    def doWaitln(self, data_list):
        result_list = []
        for data in data_list:
            result = self.getData(data) + "\n"
            result_list.append(result)
        self.doWaitAll(result_list)

    def doWaitAll(self, result_list):
        m_timeout = self.getTimer()
        now_time = int(time.time() * 1000)
        result = 0
        hit_flag = False
        while m_timeout is None and not self.end_flag and not hit_flag:
            if m_timeout is not None:
                if (now_time + m_timeout) < int(time.time()):
                    # タイムアウトを超えた
                    result = 0
                    break
            #
            process = self.process
            if self.process is None:
                shell = self.shell
                if shell is None:
                    break
                #
                # m_timeout は Noneの時無限待ちになる
                if shell.recv_ready():
                    # 最後の時間更新
                    now_time = int(time.time() * 1000)
                    output = shell.recv(1024).decode("utf-8")
                    self.setLog(output)
                    self.stdout = self.stdout + output
                    result = 1
                    for reslut_text in result_list:
                        index = self.stdout.find(reslut_text)
                        # print(f"reslut_text=/{reslut_text}/ target={self.stdout.strip()} index={index}")
                        if 0 <= index:
                            # 見つかった地点まで切り飛ばす
                            self.stdout = self.stdout[index + len(reslut_text):]
                            # print(f"remain={self.stdout}")
                            hit_flag = True
                            # hitした
                            break
                        result = result + 1
                else:
                    time.sleep(0.1)
            else:
                # ここからcmd
                # print("x4")
                if process.poll() is not None:
                    # process not alive
                    self.closeClient()
                    break
                if process.stdout.readable():
                    # 最後の時間更新
                    # print("x3")
                    now_time = int(time.time() * 1000)
                    # 読み込み
                    output = process.stdout.read(1)
                    # print("x2")
                    self.setLog(output)
                    self.stdout = self.stdout + output
                    result = 1
                    for reslut_text in result_list:
                        index = self.stdout.find(reslut_text)
                        # print(f"reslut_text=/{reslut_text}/ target={self.stdout.strip()} index={index}")
                        if 0 <= index:
                            # 見つかった地点まで切り飛ばす
                            self.stdout = self.stdout[index + len(reslut_text):]
                            # print(f"remain={self.stdout}")
                            hit_flag = True
                            # hitした
                            break
                        result = result + 1
                else:
                    # print("x5")
                    time.sleep(0.1)
        #
        if hit_flag:
            self.setValue('result', result)
        else:
            self.setValue('result', 0)

    def getTimer(self):
        m_timeout = None
        x = self.getValue('timeout', error_stop=False)
        if x is not None:
            m_timeout = int(x) * 1000
        x = self.getValue('mtimeout', error_stop=False)
        if x is not None:
            if m_timeout is None:
                m_timeout = 0
            m_timeout = m_timeout + int(x)
        return m_timeout

    def setLog(self, strvar):
        print(strvar, end='')
#

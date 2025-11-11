
#
# pyinstaller --noconsole --noconfirm nextnextping.py
#
import json
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import os
import threading
import time
from datetime import datetime
import subprocess
import re
import locale
import csv
from grammer.TtlParserWorker import TtlPaserWolker

SAMPLE_TTL = '''
;INPUT_START

;file_name = "029c1_ok_connect.ttl"
;target_display = "pingを打つ装置"
;target_ip = "127.0.0.1"
;target_type = 1  ; 1=ping, 2=traceroute, 3=show run
;base_type = 2 ; 1=cisco, 2=linux, 3=qx-s
;base_display = "SSH接続する装置"
;base_ip = "localhost:2200"
;base_account = "foo" ; アカウント情報
;next_ssh = 2  ; "0=Windows, 1=SSHログイン", "2=SSH踏み台"
;next_type = 1 ; 1=cisco, 2=linux, 3=qx-s
;next_display = "SSHからさらに接続する装置"
;next_ip  = "c1"  ; 踏み台SSHのIPアドレス
;next_account = "bar"  ; 踏み台先のIPアドレス

;INPUT_END
ifdefined file_name
if result == 0 then
    file_name = "build/connect_test.ttl"
endif

ifdefined target_display
if result == 0 then
    target_display = "pingを打つ装置"
endif
ifdefined target_ip
if result == 0 then
    target_ip = "127.0.0.1"
endif
ifdefined target_type
if result == 0 then
    target_type = 1  ; 1=ping, 2=traceroute, 3=show run
endif
ifdefined base_type
if result == 0 then
    base_type = 2 ; 1=cisco, 2=linux, 3=qx-s
endif
ifdefined base_display
if result == 0 then
    base_display = "SSH接続する装置"
endif
ifdefined base_ip
if result == 0 then
    base_ip = "localhost:2200"
endif
ifdefined base_account
if result == 0 then
    base_account = "foo"
endif
ifdefined next_ssh
if result == 0 then
    next_ssh = 2
endif
ifdefined next_type
if result == 0 then
    next_type = 1 ; 1=cisco, 2=linux, 3=qx-s
endif
ifdefined next_display
if result == 0 then
    next_display = "SSHからさらに接続する装置"
endif
ifdefined next_ip
if result == 0 then
    next_ip  = "c1"  ; 踏み台SSHのIPアドレス
endif
ifdefined next_account
if result == 0 then
    next_account = "bar"  ; 踏み台先のIPアドレス
endif

; ログファイルを設定する
log_file_name_work = file_name
strreplace log_file_name_work 1 'ttl' ''
strconcat log_file_name_work 'log'  ; 拡張子がttlでないときは replaceでlogできないので追加
; ログファイルを絶対パスに変える
getdir log_file_name
strconcat log_file_name #92
strconcat log_file_name log_file_name_work

; ログを開く
logopen log_file_name 0 0

; すでに接続されていたらエラー
testlink
if result==2  then
    messagebox "already connected" "title"
    call call_ending
    end
endif

;; ベースとなるパスワードを取得する
call call_base_password
base_password = password

; 接続する 'localhost:2200 /ssh /auth=password /user=aaa /passwd=bbb'
command = base_ip
strconcat command " /ssh /auth=password /user="
strconcat command base_account
strconcat command " /passwd="
strconcat command base_password
connect command
if result <> 2 then
    int2str strvar result
    message = "connection failer"
    strconcat message strvar
    messagebox message "title"
    call call_ending
    end
endif


prompt = '$'
timeout = 10
command = 'pwd'
sendln command
wait command
if result == 0 then
    messagebox 'input check timeout failer' 'title'
    call call_ending
    end
endif
while 1
    ; プロンプトチェック
    wait '>' '#' '$' '(yes/no)' 'assword:' '-- More --' 
    result_type = result
    if result_type == 0 then
        messagebox 'prompt check timeout failer' 'title'
        call call_ending
        end
    elseif result_type == 1 then
        prompt = '>'
        if base_type == 1 then
            ; ciscoの場合は特権へ移行
            sendln 'enable'
            continue
        endif
    elseif result_type == 2 then
        prompt = '#'
    elseif result_type == 3 then
        prompt = '$'
    elseif result_type == 4 then
        sendln "yes"
        continue
    elseif result_type == 5 then
        strcompare prompt '>'
        if result == 0 then
            call call_base_password_enable  ; 特権モード移行用
        else
            call call_base_password
        endif
        sendln password
        continue
    elseif result_type == 6 then
        sendln ''
        continue
    else
        int2str strvar result_type
        message = "prompt not found("
        strconcat message strvar
        strconcat message ")"
        messagebox message 'title'
        call call_ending
        end
    endif
    ;
    ; while を終わる
    break
endwhile


if next_ssh == 2 then
    ; ssh 接続 'ssh account@ip'
    command = "ssh "
    strconcat command next_account
    strconcat command "@"
    strconcat command next_ip
    sendln command
    while 1
        ; プロンプトチェック
        wait '>' '#' '$' '(yes/no)' 'assword:' '-- More --'
        result_type = result
        if result_type == 0 then
            messagebox 'next prompt check fail!' 'title'
            call call_ending
            end
        elseif result_type == 1 then
            prompt = '>'
            if base_type == 1 then
                sendln 'enable'
                continue
            endif
        elseif result_type == 2 then
            prompt = '#'
        elseif result_type == 3 then
            prompt = '$'
        elseif result_type == 4 then
            sendln "yes"
            continue
        elseif result_type == 5 then
            strcompare prompt '>'
            if result == 0 then
                call call_next_enable_password ; 特権モード移行用
            else
                call call_next_password
            endif
            sendln password
            continue
        elseif result_type == 6 then
            sendln ''
            continue
        else
            int2str strvar result_type
            message = "next promot not found("
            strconcat message strvar
            strconcat message ")"
            messagebox message 'title'
            call call_ending
            end
        endif
        ;
        ; while を終わる
        break
    endwhile
endif

; サーバ種別を決める
if next_ssh == 1 then ; "0=Windows, 1=SSHログイン", "2=SSH踏み台"
    server_type = base_type
else
    server_type = next_type
endif


;; ここでおまじない必要
if server_type == 1 then ; 1=cisco, 2=linux, 3=qx-s
    command = 'terminal length 0'
    sendln command
    wait command
    wait prompt
elseif server_type == 3 then ; 1=cisco, 2=linux, 3=qx-s
    command = 'screen-length disable'
    sendln command
    wait command
    wait prompt
    command = 'terminal pager offscreen-length disable'
    sendln command
    wait command
    wait prompt
    command = 'set terminal pager disable'
    sendln command
    wait command
    wait prompt
endif

;; 実コマンドの投入
if target_type = 1 then  ; 1=ping, 2=traceroute, 3=show run
    if server_type == 1 then ; 1=cisco, 2=linux, 3=qx-s
        command = 'ping '
    elseif server_type == 2 then
        command = 'ping -c 1 '
    else
        command = 'ping '
    endif
    strconcat command target_ip
    sendln command
    wait command
    wait prompt '0% packet loss' 'Success rate is 100 percent'
    if result <= 1 then
        call call_ending
        end
    endif
elseif target_type = 2 then 
    if server_type == 1 then ; 1=cisco, 2=linux, 3=qx-s
        command = 'traceroute '
    elseif server_type == 2 then
        command = 'tracepath '
    else
        command = 'traceroute '
    endif
    strconcat command target_ip
    sendln command
    wait prompt
    if result == 0 then
        messagebox 'command is time up!' command
        call call_ending
        end
    endif
else
    if server_type == 1 then ; 1=cisco, 2=linux, 3=qx-s
        command = 'show running-config'
        sendln command
        wait prompt '-- More --'
        if result = 0 then
            messagebox 'command is time up!' command
            call call_ending
            end
        elseif result = 2 then
            sendln ''
            continue
        endif
        command = 'show ip interface brief'
    elseif server_type == 2 then
        command = 'ifconfig -a'
    else
        command = 'display current-configuration'
    endif
    sendln command
    ; プロントのチェックを行う
    while 1
        ;
        wait prompt '-- More --'
        if result = 0 then
            messagebox 'command is time up!' command
            call call_ending
            end
        elseif result = 2 then
            sendln ''
            continue
        endif
        ;
        break
    endwhile
endif

; 終了処理
call call_ending

; 正常終了を通知
error=''
result = 1
end

; SSHでログインするときに使うパスワード
:call_base_password
key_target = 'normal_'
strconcat key_target base_account
key_ip = base_ip
key_base_display = base_display
call call_pass_all
return

; SSHからSSHにさらにログインするときのパスワード
:call_base_password_enable
key_target = 'enable_'
strconcat key_target base_account
key_ip = base_ip
key_base_display = base_display
call call_pass_all
return

; 特権ユーザのパスワード
:call_next_password
key_target = 'normal_'
strconcat key_target next_account
key_ip = next_ip
key_base_display = next_display
call call_pass_all
return

; 特権ユーザのパスワード
:call_next_enable_password
key_target = 'enable_'
strconcat key_target next_account
key_ip = next_ip
key_base_display = next_display
return

; パスワード関連まとめ
:call_pass_all
key_ip_replace = key_ip
strreplace key_ip_replace 1 ':' '_' ; ipv6
strreplace key_ip_replace 1 #92'.' '_' ; ipv4 # 正規表現なので単純に.を渡すと全部消える
getdir key_data
strconcat key_data #92 ;
strconcat key_data "pass_" ; パスワード保存用
strconcat key_data key_ip_replace
strconcat key_data '.key'
ispassword key_data key_target  ; パスワードの有無確認
if result == 0 then  ; 設定されていない
    message = key_target
    strconcat message "("
    strconcat message key_ip
    strconcat message ")を入力"
    strconcat message #10#13
    strconcat message key_ip
    passwordbox message base_display
    password = inputstr ; パスワードを入力
    setpassword key_data key_target password  ; パスワードを設定
else
    getpassword key_data key_target password  ; パスワードを取得
endif
return

:call_ending
testlink
if result==2  then
    closett
endif
logclose
result = 0
return

'''


class MyTtlPaserWolker(TtlPaserWolker):
    """ パサーをオーバーライドしてgui周りの処理を行わせる """
    def __init__(self, threading, next_next_ping, log_type_param):
        self.threading = threading
        self.next_next_ping = next_next_ping
        self.log_type_param = log_type_param
        self.log_type_param['stdout'] = ""
        super().__init__()

    def setLog(self, strvar):
        self.log_type_param['stdout'] = self.log_type_param['stdout'] + strvar

    def commandContext(self, name, line, data_list):
        """ GUI側で処理すべきコマンド群 """
        # print(f"commandContext {name}")
        if "passwordbox" == name:
            p1 = str(self.getData(data_list[0]))
            p2 = str(self.getData(data_list[1]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_password_dialog(done_event, p1, p2))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                self.setValue('result', 0)
                self.setValue('inputstr', '')
            else:
                self.setValue('result', 1)
                self.setValue('inputstr', inputstr)
            return
        if "inputbox" == name:
            p1 = str(self.getData(data_list[0]))
            p2 = str(self.getData(data_list[1]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_inputdialog(done_event, p1, p2))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                self.setValue('result', 0)
                self.setValue('inputstr', '')
            else:
                self.setValue('result', 1)
                self.setValue('inputstr', inputstr)
            return
        elif "dirnamebox" == name:
            p1 = str(self.getData(data_list[0]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_dirdialog(done_event, p1))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                self.setValue('result', 0)
            else:
                self.setValue('result', 1)
                self.setValue('inputstr', inputstr)
            return
        elif "filenamebox" == name:
            p1 = str(self.getData(data_list[0]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_filedialog(done_event, p1))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                self.setValue('result', 0)
            else:
                self.setValue('result', 1)
                self.setValue('inputstr', inputstr)
            return
        elif "listbox" == name:
            p1 = str(self.getData(data_list[0]))
            p2 = str(self.getData(data_list[1]))
            p3 = str(self.getKeywordName(data_list[2]))
            i = 0
            list_data = []
            while True:
                target = f"{p3}[{str(i)}]"
                # print(f"target={target}")
                if self.isValue(target):
                    list_data.append(self.getData(target))
                    i = i + 1
                else:
                    break
            if len(list_data) <= 0:
                list_data.append("None")
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_listbox_dialog(done_event, p1, p2, list_data))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                # print("result is none")
                self.setValue('inputstr', -1)
            else:
                # print(f"inputstr is {inputstr}")
                self.setValue('inputstr', inputstr)
            return
        elif "messagebox" == name:
            p1 = str(self.getData(data_list[0]))
            p2 = str(self.getData(data_list[1]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_messagebox_dialog(done_event, p1, p2))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            return
        elif "yesnobox" == name:
            p1 = str(self.getData(data_list[0]))
            p2 = str(self.getData(data_list[1]))
            done_event = threading.Event()
            self.next_next_ping.root.after(
                0, lambda: self.next_next_ping.show_yesnobox_dialog(done_event, p1, p2))
            # 待ち処理
            while not self.end_flag:
                signaled = done_event.wait(timeout=1.0)
                if signaled:
                    break
            inputstr = self.next_next_ping.result
            if inputstr is None:
                self.setValue('result', 0)
            else:
                self.setValue('result', 1)
            return
        #
        #
        # 未実装のコマンド表示
        if self.next_next_ping.init['debug']:
            self.setLog(f"\t### command value={name} line={line}\r\n")
            for data in data_list:
                data = self.getData(data)
                self.setLog(f"\t### debug value={data}\r\n")
        super().commandContext(name, line, data_list)
        #

    def setValue(self, x, y):
        if self.next_next_ping.init['debug']:
            self.log_type_param['stdout'] = self.log_type_param['stdout'] + f"### x={x} value={y}\r\n"
        super().setValue(x, y)

    def setTitle(self, title: str):
        """ タイトルの設定 """
        # print(f"setTitle {title}")
        self.next_next_ping.root.after(
            0, lambda: self.next_next_ping.setTitle(title))

    def getTitle(self) -> str:
        """ タイトルの取得 """
        title = self.next_next_ping.init['title']
        return title  # self.next_next_ping.title


class MyThread():
    def __init__(self):
        self.stop_flag = True
        self.next_next_ping = None
        self.threading = None
        self.values_values = []
        self.myTtlPaserWolker = None

    def set_therad(self, next_next_ping, threading, values_values):
        self.next_next_ping = next_next_ping
        self.threading = threading
        self.values_values = values_values

    def start(self):
        while (self.stop_flag):
            for values in self.values_values:
                (result, type, date, command) = values
                #
                flag = False
                if type not in self.next_next_ping.log:
                    self.next_next_ping.log[type] = {}
                if command not in self.next_next_ping.log[type]:
                    self.next_next_ping.log[type][command] = {}
                self.next_next_ping.log[type][command]['stdout'] = 'unkown'
                for command_dict in self.next_next_ping.init['data']:
                    if type in command_dict['name']:
                        # hit
                        if command_dict['ttl']:
                            flag = self.ttl_result(type, command)
                            # print(f"flag={flag}")
                        else:
                            flag = self.subprocess_result(type, command_dict, command)
                        #
                        break
                #
                if flag:
                    result = "OK"
                    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                else:
                    if result != "NG":
                        # NGになった時間を入力し、２回目NGは時間更新しない
                        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    result = "NG"
                if type not in self.next_next_ping.log:
                    self.next_next_ping.log[type] = {}
                if command not in self.next_next_ping.log[type]:
                    self.next_next_ping.log[type][command] = {}
                self.next_next_ping.log[type][command]['result'] = result
                self.next_next_ping.log[type][command]['date'] = date
                #
                self.next_next_ping.root.after(
                    0, lambda: self.next_next_ping.command_ping_threading(result, type, date, command))
                self.command_status_threading(f"{result} ({type}) {command}")
                #
                if not self.stop_flag:
                    break
                # print(f"wait_time={self.next_next_ping.init['wait_time']}")
                time.sleep(self.next_next_ping.init['wait_time'])
                if not self.stop_flag:
                    break
            #
            # loopフラグが落ちていたら終了する
            if self.next_next_ping.init["loop"] is False:
                messagebox.showinfo("Info", "ping end!")
                self.stop()
                break

    def ttl_result(self, type, param):
        param_list = param.split(',')
        filename = param_list[0]
        param_list_next = []
        for param_list_next_list in param_list:
            param_list_next.append(param_list_next_list.strip())
        try:
            self.myTtlPaserWolker = MyTtlPaserWolker(self.threading, self.next_next_ping, self.next_next_ping.log[type][param])
        except Exception as e:
            self.myTtlPaserWolker.setLog(f"Exception create {str(e)}")
            return 0  # this is NG!
        try:
            self.myTtlPaserWolker.execute(filename, param_list_next)
        except Exception as e:
            self.myTtlPaserWolker.setLog(f"Exception execute {str(e)}")
            return 0  # this is NG!
        finally:
            # なにがあろうとworkerは絶対に殺す
            if self.myTtlPaserWolker is not None:
                self.myTtlPaserWolker.stop()
        return int(self.myTtlPaserWolker.getValue('result')) != 0

    def subprocess_result(self, type, command_dict, command):
        flag = False
        command_next = command_dict['command']
        seconds = command_dict['timeout'] + time.time()
        command_list = command.split(',')
        if type not in self.next_next_ping.log:
            self.next_next_ping.log[type] = {}
        if command not in self.next_next_ping.log[type]:
            self.next_next_ping.log[type][command] = {}
        # print(f"T1={type} C=/{command}/")
        self.next_next_ping.log[type][command]['stdout'] = ''
        for i, command_data in enumerate(command_list):
            key = '%' + str(i + 1)
            value = command_data.strip()
            command_next = command_next.replace(key, value)
        command_next_list = command_next.split(' ')
        proc = None
        try:
            # print(f"f f={command_next_list}")
            proc = subprocess.Popen(command_next_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            # print(f"T2={type} C=/{command}/")
            while time.time() < seconds:
                if proc.stdout.readable():
                    buffer = proc.stdout.read(1)
                    if buffer is None:
                        break
                    if buffer == '':
                        continue
                    print(f"{buffer}", end='')
                    x = self.next_next_ping.log[type][command]['stdout']
                    self.next_next_ping.log[type][command]['stdout'] = x + buffer
                else:
                    time.sleep(0.1)
            # print(f"T3={type} C=/{command}/")
            #
            if 'ok' in command_dict:
                if command_dict['ok'] in self.next_next_ping.log[type][command]['stdout']:
                    flag = True
            if 'returncode' in command_dict:
                if command_dict['returncode']:
                    if proc.returncode == 0:
                        flag = True
        except subprocess.TimeoutExpired:
            pass
        finally:
            if proc is not None:
                try:
                    proc.stdout.close()
                except Exception:
                    pass
                try:
                    proc.stderr.close()
                except Exception:
                    pass
                try:
                    proc.close()
                except Exception:
                    pass
        return flag

    def stop(self):
        if self.myTtlPaserWolker is not None:
            self.myTtlPaserWolker.stop()
        self.stop_flag = False

    def command_status_threading(self, message: str):
        self.next_next_ping.root.after(
            0, lambda: self.next_next_ping.command_status_threading(message))


class NextNextPing():
    def __init__(self):
        self.LOG_JSON = 'log.json'
        self.SETTING_JSON = 'setting.json'
        self.log = {}
        self.init = {}
        self.setting_text = ""
        self.log_text = ""
        self.tree = ""
        self.tool_tree = None
        self.my_thread = None
        self.root = None
        self.status_var = None
        self.result = None

    def next_next_load(self, file_name: str):
        setting = {}
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                setting = json.load(f)
        except FileNotFoundError:
            setting = {}
        return setting

    def next_next_save(self, file_name: str, data):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def next_text_load(self, file_name: str):
        data = ''
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = f.read()
        except FileNotFoundError:
            data = ''
        return data

    def next_text_save(self, file_name: str, data):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(data)

    def save_log(self):
        self.stop()
        self.next_next_save(self.LOG_JSON, self.log)

    def save_setting(self):
        setting = self.setting_text.get("1.0", tk.END)
        self.next_text_save(self.SETTING_JSON, setting)

    def system_exit(self):
        self.stop()
        sys.exit()

    def update_setting(self):
        #
        # pingを打っていたら止める
        self.stop()
        #
        # アイテムIDをすべて削除
        children = self.tree.get_children()
        for child in children:
            self.tree.delete(child)
        #
        # すべてのipを追加
        setting = self.setting_text.get("1.0", tk.END)
        lines = setting.splitlines()
        for line in lines:
            if line.startswith('\''):
                continue
            if line.startswith('#'):
                continue
            if line.startswith(';'):
                continue
            line = line.strip()
            if line == '':
                continue
            type = 'ping'
            result = re.match("^\\s*\\(([^\\)]+)\\)\\s*(.*)\\s*", line)
            if result:
                type = result.group(1).strip().lower()
                if "trace" in type:
                    type = "trace"
                if "show" in type:
                    type = "show"
                else:
                    a_flag = False
                    for data_list in self.init['data']:
                        if data_list['name'] == type:
                            a_flag = True
                    if not a_flag:
                        type = "ping"
                line = result.group(2).strip()
            date = '--'
            result = '--'
            if type in self.log:
                if line in self.log[type]:
                    if 'result' in self.log[type][line]:
                        result = self.log[type][line]['result']
                    if 'date' in self.log[type][line]:
                        date = self.log[type][line]['date']
            values = (result, type, date, line)
            self.tree.insert("", "end", values=values)

    def command_ping(self):
        #
        # logをクリアする
        self.log = {}
        #
        if self.my_thread is None:
            message = "Info", "Ping start!"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)
            #
            children = self.tree.get_children()
            values_values = []
            for child in children:
                values_values.append(list(self.tree.item(child, 'values')))
            #
            self.my_thread = MyThread()
            thread = threading.Thread(target=self.my_thread.start)
            self.my_thread.set_therad(self, thread, values_values)
            thread.start()
        else:
            message = "Ping already start!"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)
            self.stop()

    def command_stop(self):
        if self.my_thread is None:
            message = "Ping already stop!"
        else:
            message = "Ping stop!"
            self.stop()
        self.command_status_threading(message)
        messagebox.showinfo("Info", message)

    def stop(self):
        my_thread = self.my_thread
        self.my_thread = None
        if my_thread is not None:
            my_thread.stop()

    def command_debug(self):
        if self.init['debug']:
            self.init['debug'] = False
            message = "Change to debug=False"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)
        else:
            self.init['debug'] = True
            message = "Change to debug=True"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)

    def command_loop(self):
        if self.init['loop']:
            self.init['loop'] = False
            message = "Change to loop=False"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)
        else:
            self.init['loop'] = True
            message = "Change to loop=True"
            self.command_status_threading(message)
            messagebox.showinfo("Info", message)

    def command_ping_threading(self, result, type, date, command):
        """ 戻り処理 """
        children = self.tree.get_children()
        for child in children:
            values = list(self.tree.item(child, 'values'))
            if (values[1] == type) and (values[3] == command):
                values[0] = result
                values[2] = date
            self.tree.item(child, values=values)

    def command_status_threading(self, data: str):
        """ 戻り処理 """
        message = ''
        if self.init['loop']:
            message = 'L(True) '
        else:
            message = 'L(False) '
        if self.init['debug']:
            message = message + "D(True) "
        else:
            message = message + "D(False) "
        if isinstance(data, str):
            message = message + data
        elif isinstance(data, list) or isinstance(data, tuple):
            for d in data:
                message = message + str(d)
        self.status_var.set(message)

    def on_select(self, _):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        type = values[1]
        command = values[3]
        string = "empty"
        self.command_status_threading(f"touch t={type} c=/{command}/")
        if type not in self.log:
            self.log[type] = {}
        if command not in self.log[type]:
            self.log[type][command] = {}
        result = "--"
        if 'result' in self.log[type][command]:
            result = self.log[type][command]['result']
        date = "--"
        if 'date' in self.log[type][command]:
            date = self.log[type][command]['date']
        stdout = "--"
        if 'stdout' in self.log[type][command]:
            stdout = self.log[type][command]['stdout']
        string = f"t={type} c={command}\r\n"
        string = string + f"result={result}\r\n"
        string = string + f"date={date}\r\n"
        string = string + "stdout=\r\n"
        string = string + stdout
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(1.0, string)

    def next_next_ping(self):
        self.log = self.next_next_load(self.LOG_JSON)
        self.init = self.next_next_load('init.json')
        if 'wait_time' not in self.init:
            self.init['wait_time'] = 3
        if 'title' not in self.init:
            self.init['title'] = "nextnextping"
        if 'loop' not in self.init:
            self.init['loop'] = True
        if 'debug' not in self.init:
            self.init['debug'] = False
        if 'timeout' not in self.init:
            self.init['timeout'] = 1
        if 'data' not in self.init:
            self.init['data'] = {}
        self.setting = self.next_text_load(self.SETTING_JSON)
        #
        #
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.system_exit)
        self.root.title(self.init['title'])
        self.root.geometry("800x400")
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        # ファイルメニュー
        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save setting", command=self.save_setting)
        file_menu.add_command(label="Save log", command=self.save_log)
        file_menu.add_command(label="Exit", command=self.system_exit)
        # goメニュー
        go_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Go", menu=go_menu)
        go_menu.add_command(label="Update", command=self.update_setting)
        go_menu.add_command(label="Ping", command=self.command_ping)
        go_menu.add_command(label="Stop", command=self.command_stop)
        go_menu.add_command(label="Toggle debug", command=self.command_debug)
        go_menu.add_command(label="Toggle loop", command=self.command_loop)
        # ツールメニュー
        tool_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Tool", menu=tool_menu)
        tool_menu.add_command(label="Sheet", command=self.tool_sheet)
        #
        notebook = ttk.Notebook(self.root)
        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="setting")
        #
        self.setting_text = tk.Text(tab1)
        self.setting_text.insert(1.0, self.setting)
        self.setting_text.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        #
        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="result")
        column = ('OK/NG', 'Type', 'Date', 'IP')
        #
        # フレームでTreeviewとScrollbarをまとめる
        frame = ttk.Frame(tab2)
        frame.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(frame, columns=column)
        self.tree.column('#0', width=0, stretch='no')
        self.tree.column(column[0], anchor=tk.CENTER, width=20)
        self.tree.column(column[1], anchor=tk.W, width=40)
        self.tree.column(column[2], anchor=tk.W, width=40)
        self.tree.column(column[3], anchor=tk.W)
        for var in column:
            self.tree.heading(var, text=var)
        self.tree.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        # スクロールバーの設定
        vsb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        #
        self.update_setting()
        #
        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="log")
        #
        self.log_text = tk.Text(tab3)
        self.log_text.insert(1.0, "Please attache table for result tag.")
        self.log_text.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        #
        self.status_var = tk.StringVar()
        self.command_status_threading("This is status bar")
        # ステータスバー（Label）を下部に配置
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        #
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.root.mainloop()
        #

    def setTitle(self, title: str):
        """ タイトルの設定 """
        self.init['title'] = title
        self.root.title(title)

    def show_password_dialog(self, event, p1, p2):
        # print(f"show_password_dialog {p1} / {p2}")
        dialog = PasswordDialog(self.root, message=p1, title=p2)
        self.result = None
        if dialog.result:
            # 成功した！
            self.result = dialog.result
        #
        # イベントを進ませる
        event.set()

    def show_inputdialog(self, event, p1, p2):
        user_input = simpledialog.askstring(p2, p1)
        self.result = None
        if user_input:
            # 成功した！
            self.result = user_input
        #
        # イベントを進ませる
        event.set()

    def show_dirdialog(self, event, p1):
        dialog_path = filedialog.askdirectory(
            title=p1,
            initialdir=os.getcwd()  # 現在の作業ディレクトリを初期値とする
        )
        self.result = None
        if dialog_path:
            # 成功した！
            self.result = dialog_path
        #
        # イベントを進ませる
        event.set()

    def show_filedialog(self, event, p1):
        dialog_path = filedialog.askopenfilename(
            title=p1,
            initialdir=os.getcwd()  # 現在の作業ディレクトリを初期値とする
        )
        if dialog_path:
            # 成功した！
            self.result = dialog_path
        #
        # イベントを進ませる
        event.set()

    def show_listbox_dialog(self, event, message, title, options):
        dialog = ListboxDialog(self.root, title, options, message=message)
        self.result = None
        if dialog.selection:
            # 成功した！
            self.result = dialog.selection
            # print(f"ListboxDialog {str(self.result)}")
        #
        # イベントを進ませる
        event.set()

    def show_messagebox_dialog(self, event, message, title):
        messagebox.showinfo(title, message)
        event.set()

    def show_yesnobox_dialog(self, event, message, title):
        answer = messagebox.askyesno(title=title, message=message)
        self.result = None
        # 入力結果の処理
        if answer:
            self.result = "OK"
        #
        # イベントを進ませる
        event.set()

    def tool_sheet(self):
        # モーダルダイアログ
        dialog = tk.Toplevel(self.root)
        dialog.title("tool_sheet")
        dialog.geometry("1024x400")
        #
        menu_bar = tk.Menu(dialog)
        dialog.config(menu=menu_bar)
        # ファイルメニュー
        file_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save csv", command=self.save_csv)
        file_menu.add_command(label="Load csv", command=self.load_csv)
        file_menu.add_command(label="Close", command=dialog.destroy)
        # goメニュー
        go_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Go", menu=go_menu)
        go_menu.add_command(label="Create ttl", command=self.create_ttl)
        #
        top_frame = tk.Frame(dialog)
        top_frame.pack(side=tk.TOP)
        #
        close_button = tk.Button(top_frame, text="Create", command=self.create_tool)
        close_button.pack(side=tk.LEFT)
        close_button = tk.Button(top_frame, text="Modify", command=self.modify_tool)
        close_button.pack(side=tk.LEFT)
        close_button = tk.Button(top_frame, text="Delete", command=self.delete_tooly)
        close_button.pack(side=tk.LEFT)
        #
        column = []
        for target in NextNextPing.TARGET_PARAM:
            var = target[0]
            column.append(var)
        # フレームでTreeviewとScrollbarをまとめる
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True)
        # 表を作成
        self.tool_tree = ttk.Treeview(frame, columns=column)
        self.tool_tree.column('#0', width=0, stretch='no')
        for var in column:
            self.tool_tree.column(var, anchor=tk.CENTER, width=20)
            self.tool_tree.heading(var, text=var)
        self.tool_tree.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        # スクロールバーの設定
        vsb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tool_tree.yview)
        self.tool_tree.configure(yscrollcommand=vsb.set)
        self.tool_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # ダイアログが閉じられるまで待つ
        dialog.grab_set()
        self.root.wait_window(dialog)

    def create_tool(self):
        values = []
        selected = self.tool_tree.selection()
        if selected:
            item_id = selected[0]
            values = self.tool_tree.item(item_id)["values"]
        else:
            for x in NextNextPing.TARGET_PARAM:
                values.append(str(x[2]))
        item_id = self.tool_tree.insert("", "end", values=values)
        self.update_tool(item_id, values)

    def modify_tool(self):
        selected = self.tool_tree.selection()
        if not selected:
            return
        item_id = selected[0]
        values = self.tool_tree.item(item_id)["values"]
        # print(f"values {values}")
        self.update_tool(item_id, values)

    TARGET_PARAM = [
        ["file_name", "ファイル名", "dummy.ttl", ()],
        ["target_display", "pingを打つ装置の表示名", "target_display", ()],
        ["target_ip", "pingを打つIP", "127.0.0.1", ()],
        ["target_type", "設定する種別", 1, ("1=ping", "2=traceroute", "3=show run")],
        ["next_ssh", "踏台先有無", 0, ("0=Windows", "1=SSH login", "2=SSH->SSH login")],
        ["base_type", "SSH先の種別", 2, ("1=cisco", "2=linux", "3=qx-s")],
        ["base_display", "SSH接続する表示名", "base_display", ()],
        ["base_ip", "SSH接続するIP", "localhost:2200", ()],
        ["base_account", "SSH接続するアカウント", "admin", ()],
        ["next_type", "踏み台先種別", 1, ("1=cisco", "2=linux", "3=qx-s")],
        ["next_display", "SSHからさらに接続する装置", "next_display", ()],
        ["next_ip", "踏み台SSHのIPアドレス", "dummy", ()],
        ["next_account", "踏み台先のアカウント", "admin", ()]]

    def get_japanese_flag(self) -> bool:
        current_locale = locale.getlocale()
        # 戻り値のタプルの最初の要素（言語コード）を取得
        lang_code = current_locale[0]
        # 日本語かどうかを判定
        if lang_code:
            lang_code = lang_code.lower()
            # print(f"get_japanese_flag {lang_code}")
            return lang_code.startswith('ja') or lang_code.startswith('japanese')
        return False

    def get_target_filename(self, row_index: int, values: list) -> str:
        """ ファイル名を取得する """
        row_index = str(1000 + row_index)
        #
        ans = ''
        target_ip = values[2]
        target_type = int(values[3])
        next_ssh = int(values[4])
        base_type = int(values[5])
        base_ip = values[7]
        next_ip = values[11]
        if base_type == 1:
            base_type = 'c1'
        elif base_type == 3:
            base_type = 'qx'
        else:
            base_type = ''
        action_name = self.get_target_type_to_action_name(target_type)
        if next_ssh == 0:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
            ans = f"{row_index}{base_type}_ok_{action_name}_{target_ip}"
        elif next_ssh == 1:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
            ans = f"{row_index}{base_type}_ok_{base_ip}_{action_name}_{target_ip}"
        elif next_ssh == 2:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
            ans = f"{row_index}{base_type}_ok_{next_ip}_{action_name}_{target_ip}"
        else:
            ans = "unkown_next_ssh"
        #
        ans = ans.replace(":", "_")  # ipv6
        ans = ans.replace(".", "_")  # ipv4
        ans = ans.replace("/", "_")  # folder
        ans = ans.replace("@", "_")  # account
        ans = ans.replace("\"", "")  # vs SQL injection
        ans = ans.replace("\'", "")  # vs SQL injection
        return ans + ".ttl"

    def update_tool(self, item_id, values: list) -> list:
        # モーダルダイアログ
        dialog = tk.Toplevel(self.root)
        dialog.title("tool_sheet_line")
        dialog.geometry("400x450")
        #
        # 不正対策
        while len(values) < len(NextNextPing.TARGET_PARAM):
            values.append('')
        #
        japanese_flag = self.get_japanese_flag()
        #
        name_var_list = []
        widget = []

        def on_combo_select(event):
            """ コンボ選択処理 """
            target_type = int(name_var_list[3].get()[0])
            if target_type == 3:  # 1=ping , 2=traceroute , 3=show run
                widget[2].config(state="disabled")
            else:
                widget[2].config(state="normal")
            #
            next_ssh = int(name_var_list[4].get()[0])
            if next_ssh == 0:  # ("0=Windows", "1=SSH login", "2=sSSH step")
                for entry in widget[5:]:
                    entry.config(state="disabled")
            elif next_ssh == 1:
                for entry in widget[5:]:
                    entry.config(state="normal")
                for entry in widget[9:]:
                    entry.config(state="disabled")
            else:
                for entry in widget[5:]:
                    entry.config(state="normal")
        #
        for i, target_param in enumerate(NextNextPing.TARGET_PARAM):
            label_text = target_param[0]
            if japanese_flag:
                label_text = target_param[1]
            tk.Label(dialog, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            if 0 < len(target_param[3]):
                combo_list = target_param[3]  # target_type
                selected_value = tk.StringVar()
                selected_value.set(values[i])
                name_var_list.append(selected_value)
                combo = ttk.Combobox(dialog, textvariable=selected_value)
                widget.append(combo)
                combo["values"] = combo_list
                if i == 3 or i == 4:  # target_type, ssh_type
                    combo.bind("<<ComboboxSelected>>", on_combo_select)
                value_item = 0
                j = 0
                for combo_str in combo_list:
                    if str(values[i]) == combo_str[0]:  # 最初の一文字がマッチするか？
                        # print(f"hit! {j}")
                        value_item = j
                        break
                    j = j + 1
                combo.current(value_item)  # 初期選択（インデックス）
                combo.grid(row=i, column=1, padx=10, pady=5)
            else:
                name_var = tk.StringVar()
                name_var.set(values[i])
                name_var_list.append(name_var)
                entry = tk.Entry(dialog, textvariable=name_var)
                widget.append(entry)
                entry.grid(row=i, column=1, padx=10, pady=5)
                if i == 0:
                    entry.config(state="disabled")
            #
        #
        # コンボ選択の繁栄
        on_combo_select(None)

        def submit():
            """ 入力値を取得する関数 """
            values = []
            for i, name_var in enumerate(name_var_list):
                val = name_var.get()
                if NextNextPing.TARGET_PARAM[i][0] in ["target_type", "next_ssh", "base_type", "next_type"]:
                    if 0 < len(val):
                        val = val[0]  # 先頭一文字を抽出する
                    else:
                        val = str(NextNextPing.TARGET_PARAM[i][2])  # 初期値を入れる
                values.append(val)
            #
            # 表の行数を得る
            row_index = self.tool_tree.get_children().index(item_id)
            #
            values[0] = self.get_target_filename(row_index, values)
            #
            self.tool_tree.item(item_id, values=values)
            dialog.destroy()

        bottom_frame = tk.Frame(dialog)
        bottom_frame.grid(row=len(NextNextPing.TARGET_PARAM), column=0, columnspan=2, pady=10)
        # 送信ボタン
        tk.Button(bottom_frame, text="Update", command=submit).pack(side=tk.LEFT)

        # ダイアログが閉じられるまで待つ
        dialog.grab_set()
        self.root.wait_window(dialog)

        return values

    def delete_tooly(self):
        selected_items = self.tool_tree.selection()
        for item in selected_items:
            self.tool_tree.delete(item)

    def load_csv(self):
        """ 保存ダイアログを表示 """
        file_path = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Load csv"
        )
        if file_path:
            current_encoding = ""
            if self.get_japanese_flag():
                current_encoding = "cp932"
            else:
                current_encoding = locale.getpreferredencoding(False)
            #
            # ロード
            values = []
            with open(file_path, newline='', encoding=current_encoding) as f:
                reader = csv.reader(f)
                values = [row for row in reader]
            #
            # 表を一度クリア
            for item in self.tool_tree.get_children():
                self.tool_tree.delete(item)
            #
            for i, value in enumerate(values):
                # 表への詰み込み
                while len(value) < len(NextNextPing.TARGET_PARAM):
                    value.append('')
                if value[0].strip() == "":  # 先頭が空行なら無視する
                    continue
                target_values = []
                for value_one in value:
                    target_values.append(str(value_one))  # int避け
                target_values[0] = self.get_target_filename(i, target_values)
                self.tool_tree.insert("", "end", values=target_values)
            #
            messagebox.showinfo("Info", "load_csv is ok")
            self.tool_tree.focus_set()

    def save_csv(self):
        """ 保存ダイアログを表示 """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save csv"
        )
        #
        all_items = self.tool_tree.get_children()
        values_list = []
        for item_id in all_items:
            values = self.tool_tree.item(item_id)["values"]
            values_list.append(values)
        #
        if file_path:
            current_encoding = ""
            if self.get_japanese_flag():
                current_encoding = "cp932"
            else:
                current_encoding = locale.getpreferredencoding(False)
            #
            with open(file_path, "w", encoding=current_encoding) as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(values_list)
            #
            messagebox.showinfo("Info", "save_csv is ok")
            self.tool_tree.focus_set()

    def get_target_type_to_action_name(self, target_type: int) -> str:
        """ target_type を 1=ping , 2=trace , 3=show に変える """
        if target_type == 1:
            return 'ping'
        elif target_type == 2:
            return 'trace'
        elif target_type == 3:
            return 'show'
        #
        return str(target_type)

    def create_ttl(self):
        """ リストを抽出してttlを作る """
        new_text = ''
        all_items = self.tool_tree.get_children()
        for item_id in all_items:
            values = self.tool_tree.item(item_id)["values"]
            #
            file_name = values[0]
            target_display = values[1]
            target_ip = values[2]
            target_type = int(values[3])
            next_ssh = int(values[4])
            base_ip = values[7]
            base_display = values[6]
            next_display = values[10]
            next_ip = values[11]
            #
            file_head_data = ''
            action_name = self.get_target_type_to_action_name(target_type)
            if next_ssh == 0:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
                file_head_data = f"; {action_name}  {target_display}({target_ip})\n"
            elif next_ssh == 1:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
                file_head_data = f"; {base_display}({base_ip}) {action_name} {target_display}({target_ip})\n"
            elif next_ssh == 2:  # 0=Windows , 1=SSH login , 2=SSH->SSH login
                file_head_data = f"; {base_display}({base_ip})->{next_display}({next_ip}) {action_name} {target_display}({target_ip})\n"
            else:
                file_head_data = "; \n"
            #
            new_text = new_text + file_head_data
            #
            if next_ssh == 0:
                if target_type == 1:  # "1=ping", "2=traceroute", "3=show run"
                    new_text = new_text + target_ip + "\n"
                elif target_type == 2:
                    new_text = new_text + "(traceroute)" + target_ip + "\n"
                else:
                    new_text = new_text + "(show)" + target_ip + "\n"
                new_text = new_text + "\n"
            else:
                new_text = new_text + "(ttl)" + file_name + "\n"
                new_text = new_text + "\n"
                # 
                file_head_data = ';\n' + file_head_data + ";\n\n"
                #
                # ファイルを書き込む
                for i, value in enumerate(values):
                    file_head_data = file_head_data + NextNextPing.TARGET_PARAM[i][0]
                    file_head_data = file_head_data + " = "
                    if isinstance(NextNextPing.TARGET_PARAM[i][2], int):
                        file_head_data = file_head_data + str(value)
                    else:
                        file_head_data = file_head_data + f"\"{str(value)}\""
                    if 0 < len(NextNextPing.TARGET_PARAM[i][3]):
                        file_head_data = file_head_data + "  ; "
                        flag = False
                        for data in NextNextPing.TARGET_PARAM[i][3]:
                            if flag:
                                file_head_data = file_head_data + " , "
                            else:
                                flag = True
                            file_head_data = file_head_data + data
                        #
                    file_head_data = file_head_data + "\n"
                base_file = 'base.ttl'
                file_head_data = file_head_data + "\n\n"
                file_head_data = file_head_data + f"include \"{base_file}\""
                file_head_data = file_head_data + "\n\n"
                if not os.path.exists(base_file):  # ベースファイルが存在しなければ作る
                    with open(base_file, 'w', encoding='utf-8') as f:
                        f.write(SAMPLE_TTL)
                #
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(file_head_data)
                #
        # 設定シートを書き換える
        self.setting_text.delete('1.0', 'end')  # 既存のテキストを削除
        self.setting_text.insert('1.0', new_text)  # 新しいテキストを挿入
        #
        # 設定シートを保存する
        self.save_setting()
        #
        # resultシートを更新する
        self.update_setting()
        #
        messagebox.showinfo("Info", "ttl is ok")
        self.tool_tree.focus_set()


class PasswordDialog(simpledialog.Dialog):
    def __init__(self, parent, title="PasswordDialog", message="Enter Password"):
        self.message = message
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.message).grid(row=0, column=0, padx=10, pady=10)
        self.entry = tk.Entry(master, show="*")
        self.entry.grid(row=1, column=0, padx=10)
        return self.entry  # 初期フォーカス

    def apply(self):
        self.result = self.entry.get()


class ListboxDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options, message="Plrease select"):
        self.options = options
        self.selection = None
        self.message = message
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.message).pack(padx=10, pady=5)
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        for item in self.options:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(padx=10, pady=5)
        return self.listbox

    def apply(self):
        selected = self.listbox.curselection()
        # print("apply")
        if selected:
            self.selection = self.listbox.get(selected[0])
            # print(f"選択されている {self.selection}")


if __name__ == "__main__":
    #
    next_next_ping = NextNextPing()
    next_next_ping.next_next_ping()
    #

#

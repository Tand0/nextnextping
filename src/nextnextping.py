
#
# pyinstaller --noconsole --noconfirm nextnextping.py
#
import json
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
import time
from datetime import datetime
import subprocess
import re
from grammer.TtlParserWorker import TtlPaserWolker


class MyTtlPaserWolker(TtlPaserWolker):
    def __init__(self, log_type_param, init):
        super().__init__()
        self.log_type_param = log_type_param
        self.log_type_param['stdout'] = ""
        self.init = init

    def setLog(self, strvar):
        self.log_type_param['stdout'] = self.log_type_param['stdout'] + strvar

    def commandContext(self, name, line, data_list):
        # 未実装のコマンド表示
        if self.init['debug']:
            self.setLog(f"\t### command value={name} line={line}\r\n")
            for data in data_list:
                data = self.getData(data)
                self.setLog(f"\t### debug value={data}\r\n")
        #

    def setValue(self, x, y):
        if self.init['debug']:
            self.log_type_param['stdout'] = self.log_type_param['stdout'] + f"### x={x} value={y}\r\n"
        super().setValue(x, y)


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
                self.next_next_ping.log[type][command]['result'] = result
                self.next_next_ping.log[type][command]['date'] = date
                #
                self.next_next_ping.root.after(
                    0, lambda: self.next_next_ping.command_ping_threading(result, type, date, command))
                #
                if not self.stop_flag:
                    break
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
            self.myTtlPaserWolker = MyTtlPaserWolker(self.next_next_ping.log[type][param], self.next_next_ping.init)
            self.myTtlPaserWolker.execute(filename, param_list_next)
        except TypeError:
            if self.myTtlPaserWolker is not None:
                self.myTtlPaserWolker.stop()
            return 0  # this is NG!
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
        i = 1
        for command_data in command_list:
            key = '%' + str(i)
            value = command_data.strip()
            command_next = command_next.replace(key, value)
            i = i + 1
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


class NextNextPing():
    def __init__(self):
        self.LOG_JSON = 'log.json'
        self.SETTING_JSON = 'setting.json'
        self.log = {}
        self.init = {}
        self.setting_text = ""
        self.log_text = ""
        self.tree = ""
        self.my_thread = None
        self.root = None

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
            messagebox.showinfo("Info", "Ping start!")
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
            messagebox.showinfo("Info", "Ping already start!")
            self.stop()

    def command_stop(self):
        if self.my_thread is None:
            messagebox.showinfo("Info", "Ping already stop!")
        else:
            messagebox.showinfo("Info", "Ping stop!")
            self.stop()

    def stop(self):
        my_thread = self.my_thread
        self.my_thread = None
        if my_thread is not None:
            my_thread.stop()

    def command_debug(self):
        if self.init['debug']:
            self.init['debug'] = False
            messagebox.showinfo("Info", "Change to debug=False")
        else:
            self.init['debug'] = True
            messagebox.showinfo("Info", "Change to debug=True")

    def command_loop(self):
        if self.init['loop']:
            self.init['loop'] = False
            messagebox.showinfo("Info", "Change to loop=False")
        else:
            self.init['loop'] = True
            messagebox.showinfo("Info", "Change to loop=True")

    def command_ping_threading(self, result, type, date, command):
        """ 戻り処理 """
        children = self.tree.get_children()
        for child in children:
            values = list(self.tree.item(child, 'values'))
            if (values[1] == type) and (values[3] == command):
                values[0] = result
                values[2] = date
            self.tree.item(child, values=values)

    def on_select(self, _):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        type = values[1]
        command = values[3]
        string = "empty"
        # print(f"t={type} c=/{command}/")
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
        if 'loop' not in self.init:
            self.init['loop'] = True
        if 'debug' not in self.init:
            self.init['debug'] = False
        if 'timeout' not in self.init:
            self.init['timeout'] = 30
        if 'data' not in self.init:
            self.init['data'] = {}
        self.setting = self.next_text_load(self.SETTING_JSON)
        #
        #
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.system_exit)
        self.root.title("next_next_ping")
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
        self.tree = ttk.Treeview(tab2, columns=column)
        self.tree.column('#0', width=0, stretch='no')
        self.tree.column(column[0], anchor=tk.CENTER, width=20)
        self.tree.column(column[1], anchor=tk.W, width=40)
        self.tree.column(column[2], anchor=tk.W, width=40)
        self.tree.column(column[3], anchor=tk.W)
        self.tree.heading(column[0], text=column[0])
        self.tree.heading(column[1], text=column[1])
        self.tree.heading(column[2], text=column[2])
        self.tree.heading(column[3], text=column[3])
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        #
        self.update_setting()
        self.tree.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        #
        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="log")
        #
        self.log_text = tk.Text(tab3)
        self.log_text.insert(1.0, self.log)
        self.log_text.pack(pady=2, padx=2, fill=tk.BOTH, expand=True)
        #
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        #
        self.root.mainloop()
        #


if __name__ == "__main__":
    #
    next_next_ping = NextNextPing()
    next_next_ping.next_next_ping()
    #

#

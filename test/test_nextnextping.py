import time
import os
import socket
import threading
import paramiko
import sys
import re
import random
import pathlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../nextnextping")))
# from grammer.TtlParserWorker import TtlPaserWolker
from ttlmacro import ttlmacro


class Server(paramiko.ServerInterface):
    """ SSHサーバの実装 """

    def __init__(self):
        """ コンストラクタ """
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        """ セッションの許可 """
        print(f"test check_channel_request kind={kind} ")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        """ パスワードチェック """
        # print(f"test username={username}  password={password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        """ 認証の許可 """
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_with_mic(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        """ 認証の許可 """
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        """ 認証の許可 """
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        """ 認証の許可 """
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        """ shellの許可 """
        # print("test check_channel_shell_request")
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        """ ptyの許可 """
        return True

    def check_channel_subsystem_request(self, channel, name):
        """ サブシステム要求の処理 """
        print(f"test check_channel_subsystem_request {name}")
        return False

    def get_subsystem(self, name):
        """ サブシステム名を返す """
        print(f"test get_subsystem {name}")
        return None


class ServerStarter():
    """ 実際のサーバ起動部分 """

    KEY_FILE = "test_rsa.key"  # キーファイルの位置

    SHOW_RUNNING_CONFIG = """Building configuration...

Current configuration : 1234 bytes
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname SW-Floor-1
!
!
boot-start-marker
boot-end-marker
!
!
no aaa new-model
!
!
interface GigabitEthernet0/1
 description "Uplink to Core Router"
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 description "Server Port 1"
 switchport mode access
 switchport access vlan 10
 no shutdown
!
interface GigabitEthernet0/3
 description "Access Point"
 no shutdown
!
!
line con 0
line vty 0 4
 login local
!
!
end
""".replace('\n', '\r\n')

    PING = """PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.070 ms

--- localhost ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.070/0.070/0.070/0.000 ms
""".replace('\n', '\r\n')

    PING_CISCO = """
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/3/5 ms
""".replace('\n', '\r\n')

    TRACERT = """
Tracing route to t-ando [::1]
over a maximum of 30 hops:

  1    <1 ms    <1 ms    <1 ms  t-ando [::1]

Trace complete.

""".replace('\n', '\r\n')

    TRACEROUTE = """traceroute to localhost (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1)  0.099 ms  0.075 ms  0.071 ms
"""

    TRACEPATH = """traceroute to localhost (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1)  0.099 ms  0.075 ms  0.071 ms
""".replace('\n', '\r\n')

    DISPLAY_CURRENT_CONFIGURATION = """#
sysname QX-S3526
#
vlan 1
 name default
#
interface GigabitEthernet0/1
 port access vlan 10
#
interface GigabitEthernet0/2
 port access vlan 20
""".replace('\n', '\r\n')

    DISPLAY_CURRENT_CONFIGURATION_MORE = """#
interface Vlan-interface1
 ip address 192.168.1.1 255.255.255.0
#
user-interface console 0
 authentication-mode password
 set authentication password cipher ********
#
""".replace('\n', '\r\n')

    IFCONFIG = """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1440
        inet xx.xx.209.61  netmask 255.255.240.0  broadcast xx.xx.223.255
        inet6 xx::xx:5dff:feae:24d3  prefixlen 64  scopeid 0x20<link>
        ether xx:xx:5d:ae:24:d3  txqueuelen 1000  (Ethernet)
        RX packets 114  bytes 212332 (212.3 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 112  bytes 7731 (7.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 14  bytes 1710 (1.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 14  bytes 1710 (1.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

""".replace('\n', '\r\n')

    def __init__(self, port: int):
        """ コンストラクタ """
        if os.path.isfile(ServerStarter.KEY_FILE):
            self.host_key = paramiko.RSAKey(filename=ServerStarter.KEY_FILE)
        else:
            self.host_key = paramiko.RSAKey.generate(2048)
            self.host_key.write_private_key_file(ServerStarter.KEY_FILE)
        #
        self.DoGSSAPIKeyExchange = True
        self.port = port
        self.stop_flag = False
        self.chan = None
        self.client = None
        self.t = None
        self.sock = None
        self.state = []
        self.prompt = None
        self.set_state('$')

    def set_state(self, state: str):
        """ 外部から状態を更新する """
        self.state = []
        self.push_state(state)

    def push_state(self, state_base: str):
        state_base = state_base.lower()
        # print(f"push_state {state_base}")
        if 'cisco1' in state_base or 'c1' in state_base:
            state_base = 'c1'
        elif 'cisco2' in state_base or 'c2' in state_base:
            state_base = 'c2'
        elif 'qx-s' in state_base or 'qx' in state_base:
            state_base = 'qx'
        elif 'linux' in state_base or 'ubuntu' in state_base:
            state_base = '$'
        elif 'user' in state_base:
            state_base = 'user'
        elif 'pass' in state_base:
            state_base = 'pass'
        elif 'y/n' in state_base:
            state_base = 'y/n'
        elif 'more' in state_base:
            state_base = 'more'
        else:
            state_base = "$"
        self.state.append(state_base)
        self.update_prompt()
        # print(f"test push_state {state_base} // {self.state} // {self.prompt}")

    def peek_state(self) -> str:
        return self.state[-1]

    def pop_state(self) -> bool:
        if len(self.state) <= 1:
            return False
        self.state.pop()
        self.update_prompt()
        return True

    def update_prompt(self):
        """ ステートを使ってプロンプトを更新する """
        state = self.state[-1]
        # print(f"update_prompt {state}")
        if 'c1' == state:
            self.prompt = 'xxx>'  # for cisco not enable
        elif 'c2' == state:
            self.prompt = 'xxx#'  # for cisco enable
        elif 'qx' == state:
            self.prompt = '<xx>'  # for qx-s
        elif '$' == state:
            self.prompt = 'xxx$ '  # for linux
        elif 'user' == state:
            self.prompt = 'User:'
        elif 'pass' == state:
            self.prompt = 'Password:'
        elif 'y/n' == state:
            self.prompt = 'Are you sure you want to continue connecting (yes/no)?'
        elif 'more' == state:
            self.prompt = '-- More --'
        else:
            self.prompt = 'XXX$ '  # for linux

    def cleint_close(self):
        """ この処理が呼ばれたらクライアントをクローズする """
        print("test clinet close!")
        #
        local_t = self.t
        self.t = None
        if local_t is not None:
            try:
                local_t.close()
            except Exception:
                pass
        #
        local_chan = self.chan
        self.chan = None
        if local_chan is not None:
            try:
                local_chan.close()
            except Exception:
                pass
        #
        local_client = self.client
        self.client = None
        if local_client is not None:
            try:
                local_client.close()
            except Exception:
                pass

    def close(self):
        """ この処理が呼ばれたらクローズする """
        #
        print("test close start!")
        #
        self.stop()
        self.cleint_close()
        #
        local_sock = self.sock
        self.sock = None
        if local_sock is not None:
            try:
                local_sock.close()
            except Exception:
                pass

    def stop(self):
        """ この処理が呼ばれたら停止する """
        self.stop_flag = True

    def start(self):
        """ 実処理 """
        # now connect
        try:
            print(f"test bind p={self.port}")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", self.port))
            #
            if self.sock is None:
                return paramiko.SSHException("self.sock is None")
            #
            print("test Listen start ...")
            self.sock.listen(100)
            #
            while not self.stop_flag:
                print("test while loop start!")
                #
                sock = self.sock
                if sock is None:
                    return paramiko.SSHException("self.sock is None")
                self.client, _ = sock.accept()
                #
                self.invoke_accept()
                #
        except OSError as e:
            print(f"test *** Caught OSError: {str(e.__class__)} : {str(e)}")
            return 1
        except paramiko.SSHException as e:
            print(f"test *** Caught SSHException: {str(e.__class__)} : {str(e)}")
            return 1
        finally:
            self.close()
        return 0

    def invoke_accept(self):
        """ self.sock.accept()後の処理。本来であればスレッド化すべき個所 """
        print("test invoke_accept")
        try:
            #
            print("test Got a connection!")
            self.t = paramiko.Transport(self.client, gss_kex=self.DoGSSAPIKeyExchange)
            self.t.set_gss_host(socket.getfqdn(""))
            self.t.load_server_moduli()
            self.t.add_server_key(self.host_key)
            #
            print("test Server start!")
            server = Server()
            self.t.start_server(server=server)
            #
            # wait for auth
            self.chan = self.t.accept()
            if self.chan is None:
                print("test *** No channel.")
                return
            #
            # サブシステムが開始されるまで待機
            server.event.wait()
            #
            # client処理
            print("test invoke_client")
            self.invoke_client(server)
            #
        except OSError as e:
            print(f"test *** Client OSError: {str(e.__class__)} : {str(e)}")
        except paramiko.SSHException as e:
            print(f"test *** Client SSHException: {str(e.__class__)} : {str(e)}")
        finally:
            self.cleint_close()
        return

    def invoke_client(self, server):
        """ shellの実装 """
        #
        if not server.event.is_set():
            print("test *** Client never asked for a shell.")
            return
            #
        print("test is_set() OK!")
        #
        self.chan.send(f"{self.prompt}")
        message = ''
        while not self.stop_flag:
            if self.chan is None or not self.chan.active:
                break
            elif self.chan.recv_ready():
                output = self.chan.recv(1).decode("utf-8")
                if "\r" == output:
                    self.chan.send("\r\n")
                elif "\n" == output:
                    self.chan.send("\r\n")
                else:
                    if self.peek_state() != 'pass':
                        self.chan.send(output)
                    message = message + output
                    continue
                #
                if self.peek_state() in ['y/n', 'pass', 'user']:
                    # print(f"test peek={self.peek_state()}")
                    self.pop_state()
                elif 'more' == self.peek_state():
                    self.chan.send(ServerStarter.DISPLAY_CURRENT_CONFIGURATION_MORE)
                    self.pop_state()
                else:
                    result1 = re.search("^\\s*exit", message)
                    result2 = re.search("^\\s*ping", message)
                    result3 = re.search("^\\s*ssh\\s+([-a-zA-Z0-9@]+)", message)
                    result4 = re.search("^\\s*enable", message)
                    result5 = re.search("^\\s*show\\s+running-config", message)
                    result6 = re.search("^\\s*tracert", message)
                    result7 = re.search("^\\s*traceroute", message)
                    result8 = re.search("^\\s*tracepath", message)
                    result9 = re.search("^\\s*display\\s+current-configuration", message)
                    result10 = re.search("^\\s*ifconfig", message)
                    if result1:
                        if not self.pop_state():
                            self.cleint_close()
                            return
                    elif result2:
                        if self.peek_state() in ['c1', 'c2']:
                            self.chan.send(ServerStarter.PING_CISCO)
                        else:
                            self.chan.send(ServerStarter.PING)
                    elif result3:
                        # 新しい状態を積む
                        self.push_state(result3.group(1))
                        self.push_state('pass')
                        #
                        if random.randint(0, 1):
                            # ランダムにy/nを聞く
                            self.push_state('y/n')
                        #
                    elif result4:
                        # 新しい状態を積む
                        self.push_state('c2')
                        # パスワードを聞く
                        self.push_state('pass')
                    elif result5:
                        self.chan.send(ServerStarter.SHOW_RUNNING_CONFIG)
                    elif result6:
                        self.chan.send(ServerStarter.TRACERT)
                    elif result7:
                        self.chan.send(ServerStarter.TRACEROUTE)
                    elif result8:
                        self.chan.send(ServerStarter.TRACEPATH)
                    elif result9:
                        self.chan.send(ServerStarter.DISPLAY_CURRENT_CONFIGURATION)
                        # 新しい状態を積む
                        self.push_state('more')
                    elif result10:
                        self.chan.send(ServerStarter.IFCONFIG)
                #
                # プロンプトを渡す
                self.chan.send(f'{self.prompt}')
                message = ''
            elif self.chan.exit_status_ready():
                print("test Session ended")
                break
            else:
                time.sleep(0.1)
        print("test recv_ready end!")
        return


class TTLLoader():
    """ TTLを読み込む """

    def __init__(self):
        """ ttl のテストをするためのフォルダ """

    def start(self, files=None):
        """ 実処理をする """
        #
        serverStarter = ServerStarter(2200)
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start)
        # スレッドを開始
        th.start()
        #
        # カレントフォルダを保持する
        current_folder = os.getcwd()
        #
        target_result = re.search("test$", current_folder)
        if not target_result:
            # もしテストフォルダでなかったらテストフォルダに移動
            test_folder = os.path.join(current_folder, 'test')
            os.chdir(test_folder)
        #
        # テストデータ保存用のフォルダを作る
        os.makedirs("build", exist_ok=True)
        #
        try:
            if files is None:
                # ファイルがいなかったらリストを取ってくる
                files = os.listdir('.')
            for file in files:
                #
                if '.ttl' not in file:
                    continue
                #
                #
                ok_flag = False
                if '_ok_' in file:
                    ok_flag = True
                #
                print()
                print(f"test file={file}")
                #
                result = re.search("^[0-9]+([a-zA-Z][a-zA-Z0-9]*)_", os.path.basename(file))
                if result:
                    g1 = result.group(1)
                    print(f"test state={g1} file={file}")
                    serverStarter.set_state(g1)
                else:
                    print(f"test state=linux file={file}")
                    serverStarter.set_state('$')
                #
                dummy_argv = ["python", file, 'param1', 'param2', 'param3']
                try:
                    ttlPaserWolker = ttlmacro(dummy_argv)
                except Exception as e:
                    if not ok_flag:
                        continue  # OKフラグがFalseなら正常
                    else:
                        assert False, str(e)
                result = int(ttlPaserWolker.getValue('result'))
                error_data = ttlPaserWolker.getValue('error')
                if ok_flag:
                    result_flag = result != 0
                    assert result_flag, f"test OK f={file} e=/{error_data}/"
                else:
                    result_flag = result == 0
                    assert result_flag, f"test NG f={file} e=/{error_data}/"
                #
        finally:
            # フォルダをもとに戻す
            os.chdir(current_folder)
            #
            # サーバをクローズする
            print("test_load_ttl finally")
            serverStarter.close()


def test_load_ttl():
    """ ttlファイルが動作するか確認する """
    tTLLoader = TTLLoader()
    tTLLoader.start()
    #


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # スレッドだけ立てる(teratermでの評価用)
        serverStarter = ServerStarter(2200)
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start)
        # スレッドを開始
        th.start()
        #
        try:
            print("test command#", end="")
            while True:
                cmd = input()
                if cmd == "exit":
                    break
                print("test command#", end="")
        finally:
            print("test start finally")
            serverStarter.close()
            sys.exit(-1)
    else:
        # ファイル名を指定してテストを実施する
        file_name = sys.argv[1]
        file_name = pathlib.Path(file_name)
        if not file_name.is_absolute():
            # 相対パスなら絶対パスに書き換える
            file_name = pathlib.Path.cwd() / file_name
        file_name = str(file_name)
        tTLLoader = TTLLoader()
        tTLLoader.start(files=[file_name])
    #
#

import time
import os
import socket
import threading
import paramiko
import sys
import re
import random
import pathlib
from paramiko import SFTPServerInterface, SFTPServer, SFTPAttributes, SFTPHandle, SFTP_OK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../nextnextping")))
# from grammer.TtlParserWorker import TtlPaserWolker
from ttlmacro import ttlmacro


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

ENABLE_ERROR = "% Uncrecognized Command\r\n"

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

SHOW_IP_INTERFACE_BRIEF = """Interface        IP-Address      OK? Method Status                Protocol
GigabitEthernet0/1 192.168.1.1     YES manual up                    up
GigabitEthernet0/2 192.168.2.1     YES manual up                    down
GigabitEthernet0/3 unassigned      YES manual administratively down down
""".replace('\n', '\r\n')


class Server(paramiko.ServerInterface):
    """ SSHサーバの実装 """

    def __init__(self):
        """ コンストラクタ """
        self.event = threading.Event()
        self.sftp_flag = False

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
        return "password,publickey"

    def check_channel_shell_request(self, channel):
        """ shellの許可 """
        print("test check_channel_shell_request")
        self.sftp_flag = False
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        """ ptyの許可 """
        return True

    def check_channel_subsystem_request(self, channel, name):
        """ サブシステム要求の処理 """
        print(f"test check_channel_subsystem_request {name}")
        self.sftp_flag = True
        self.event.set()
        return super().check_channel_subsystem_request(channel, name)

    def is_sftp_flag(self):
        """ sftpかどうかチェックする """
        return self.sftp_flag


class StubSFTPServer (SFTPServerInterface):
    ROOT = os.getcwd()

    def _realpath(self, path):
        return self.ROOT + self.canonicalize(path)

    def list_folder(self, path):
        path = self._realpath(path)
        try:
            out = []
            flist = os.listdir(path)
            for fname in flist:
                attr = SFTPAttributes.from_stat(os.stat(os.path.join(path, fname)))
                attr.filename = fname
                out.append(attr)
            return out
        except OSError as e:
            print("test list_folder OSError")
            return SFTPServer.convert_errno(e.errno)

    def stat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.stat(path))
        except OSError as e:
            print("test stat OSError")
            return SFTPServer.convert_errno(e.errno)

    def lstat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.lstat(path))
        except OSError as e:
            print("test lstat OSError")
            return SFTPServer.convert_errno(e.errno)

    def open(self, path, flags, attr):
        path = self._realpath(path)
        try:
            binary_flag = getattr(os, 'O_BINARY', 0)
            flags |= binary_flag
            mode = getattr(attr, 'st_mode', None)
            if mode is not None:
                fd = os.open(path, flags, mode)
            else:
                # os.open() defaults to 0777 which is
                # an odd default mode for files
                fd = os.open(path, flags, 0o666)
        except OSError as e:
            print("test open/0o666 OSError")
            return SFTPServer.convert_errno(e.errno)
        if (flags & os.O_CREAT) and (attr is not None):
            attr._flags &= ~attr.FLAG_PERMISSIONS
            SFTPServer.set_file_attr(path, attr)
        if flags & os.O_WRONLY:
            if flags & os.O_APPEND:
                fstr = 'ab'
            else:
                fstr = 'wb'
        elif flags & os.O_RDWR:
            if flags & os.O_APPEND:
                fstr = 'a+b'
            else:
                fstr = 'r+b'
        else:
            # O_RDONLY (== 0)
            fstr = 'rb'
        try:
            f = os.fdopen(fd, fstr)
        except OSError as e:
            print("test open/fdopen OSError")
            return SFTPServer.convert_errno(e.errno)
        fobj = StubSFTPHandle(flags)
        fobj.filename = path
        fobj.readfile = f
        fobj.writefile = f
        return fobj

    def remove(self, path):
        path = self._realpath(path)
        try:
            os.remove(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def rename(self, oldpath, newpath):
        oldpath = self._realpath(oldpath)
        newpath = self._realpath(newpath)
        try:
            os.rename(oldpath, newpath)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def mkdir(self, path, attr):
        path = self._realpath(path)
        try:
            os.mkdir(path)
            if attr is not None:
                SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def rmdir(self, path):
        path = self._realpath(path)
        try:
            os.rmdir(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def chattr(self, path, attr):
        path = self._realpath(path)
        try:
            SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def symlink(self, target_path, path):
        path = self._realpath(path)
        if (len(target_path) > 0) and (target_path[0] == '/'):
            # absolute symlink
            target_path = os.path.join(self.ROOT, target_path[1:])
            if target_path[:2] == '//':
                # bug in os.path.join
                target_path = target_path[1:]
        else:
            # compute relative to path
            abspath = os.path.join(os.path.dirname(path), target_path)
            if abspath[:len(self.ROOT)] != self.ROOT:
                # this symlink isn't going to work anyway -- just break it immediately
                target_path = '<error>'
        try:
            os.symlink(target_path, path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        return SFTP_OK

    def readlink(self, path):
        path = self._realpath(path)
        try:
            symlink = os.readlink(path)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        # if it's absolute, remove the root
        if os.path.isabs(symlink):
            if symlink[:len(self.ROOT)] == self.ROOT:
                symlink = symlink[len(self.ROOT):]
                if (len(symlink) == 0) or (symlink[0] != '/'):
                    symlink = '/' + symlink
            else:
                symlink = '<error>'
        return symlink


class StubSFTPHandle (SFTPHandle):
    def stat(self):
        try:
            return SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def chattr(self, attr):
        # python doesn't have equivalents to fchown or fchmod, so we have to
        # use the stored filename
        try:
            SFTPServer.set_file_attr(self.filename, attr)
            return SFTP_OK
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)


class ServerStarter():
    """ 実際のサーバ起動部分 """

    KEY_FILE = "test_rsa.key"  # キーファイルの位置

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
        self.channel = None
        self.client = None
        self.transport = None
        self.server_socket = None
        self.state = []
        self.password_ng_flag = False
        self.prompt = None
        self.set_state('$')

    def set_state(self, state: str):
        """ 外部から状態を更新する """
        # パスワードNGフラグの解放
        self.password_ng_flag = False
        # 状態の初期化
        self.state = []
        # 状態更新
        self.push_state(state)

    def push_state(self, state_base: str):
        state_base = state_base.lower()
        # print(f"test push_state ({state_base})")
        #
        trigger_flag = False
        for trigger in ServerStarter.TRIGGER:
            if state_base == "":
                continue
            if trigger[0] == state_base or trigger[2] == state_base:
                trigger_flag = True
                break
        if trigger_flag:
            pass
        elif 'cisco1' in state_base or 'c1' in state_base:
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
        elif 'vm' in state_base:  # vmware
            state_base = 'vm'
        else:
            state_base = "$"
        self.state.append(state_base)
        self.update_prompt()
        # print(f"test push_state {state_base} // {self.state} // {self.prompt}")

    def peek_state(self) -> str:
        # print(f"test peek_state ({self.state[-1]})")
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
        trigger_flag = False
        for trigger in ServerStarter.TRIGGER:
            if trigger[2] == '':
                continue
            if trigger[2] == state:
                self.prompt = trigger[3]
                trigger_flag = True
                break
        if trigger_flag:
            pass
        elif 'c1' == state:
            self.prompt = 'Router>'  # for cisco not enable
        elif 'c2' == state:
            self.prompt = 'Router# '  # for cisco enable
        elif 'qx' == state:
            self.prompt = '<Switch> '  # for qx-s
        elif '$' == state:
            self.prompt = 'root@localhost:~$ '  # for linux
        elif 'user' == state:
            self.prompt = 'User:'
        elif 'pass' == state:
            self.prompt = 'Password:'
        elif 'y/n' == state:
            self.prompt = 'Are you sure you want to continue connecting (yes/no)?'
        elif 'vm' == state:
            self.prompt = '[root@localhost:~] '
        else:
            self.prompt = 'root@localhost:~$ '  # for linux
        # print(f"update_prompt s={state} p={self.prompt}")

    def cleint_close(self):
        """ この処理が呼ばれたらクライアントをクローズする """
        print("test clinet close!")
        #
        local_transport = self.transport
        self.transport = None
        if local_transport is not None:
            try:
                local_transport.close()
            except Exception:
                pass
        #
        local_chan = self.channel
        self.channel = None
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
        local_sock = self.server_socket
        self.server_socket = None
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
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", self.port))
            #
            if self.server_socket is None:
                return paramiko.SSHException("self.server_socket is None")
            #
            print("test Listen start ...")
            self.server_socket.listen(100)
            #
            while not self.stop_flag:
                print("test while loop start!")
                #
                local_socket = self.server_socket
                if local_socket is None:
                    return paramiko.SSHException("self.server_socket is None")
                self.client, _ = local_socket.accept()
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
            print("test finally self.close()")
            self.close()
        return 0

    def invoke_accept(self):
        """ self.server_socket.accept()後の処理。本来であればスレッド化すべき個所 """
        print("test invoke_accept")
        try:
            #
            print("test Got a connection!")
            self.transport = paramiko.Transport(self.client, gss_kex=self.DoGSSAPIKeyExchange)
            # self.transport.set_gss_host(socket.getfqdn(""))
            # self.transport.load_server_moduli()
            self.transport.add_server_key(self.host_key)
            self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer, StubSFTPServer)
            #
            print("test Server start!")
            server = Server()
            self.transport.start_server(server=server)
            #
            # wait for auth
            self.channel = self.transport.accept()
            if self.channel is None:
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
            print("test finally self.cleint_close()")
            self.cleint_close()
        return

    TRIGGER = [
        ["", "^\\s*ping\\s+", '', '', PING],
        ["", "^\\s*tracert", '', '', TRACERT],
        ["", "^\\s*traceroute", '', '', TRACEROUTE],
        ["", "^\\s*tracepath", '', '', TRACEPATH],
        ["", "^\\s*ifconfig", '', '', IFCONFIG],
        ["c1", "^\\s*ping\\s+", '', '', PING_CISCO],
        ["c2", "^\\s*show\\s+ip\\s+interface\\s+brief", '', '', SHOW_IP_INTERFACE_BRIEF],
        ["c2", "^\\s*config(ure)?\\s+terminal", "config", 'Router(config)# ', ''],
        ["c2", "^\\s*ping\\s+", '', '', PING_CISCO],
        ["c2", "^\\s*show\\s+running-config", '', '', SHOW_RUNNING_CONFIG],
        ["config", "^\\s*vlan\\s+", "config-vlan", 'Router(config-vlan)# ', ''],
        ["config", "^\\s*interface\\s+", "config-if", 'Router(config-if)# ', ''],
        ["config", "^\\s*class-map\\s+", "config-cmap", 'Router(config-cmap)# ', ''],
        ["config", "^\\s*policy-map\\s+", "config-pmap", 'Router(config-pmap)# ', ''],
        ["config-pmap", "^\\s*class\\s+", "config-pmap-c", 'Router(config-pmap-c)# ', ''],
        ["qx", "^\\s*display\\s+current-configuration", 'more', '-- More --', DISPLAY_CURRENT_CONFIGURATION],
        ["qx", "^\\s*system-view", "qx-config", '[Switch] ', ''],
        ["qx-config", "^\\s*interface\\s+gigabitethernet", "qx-gbe", '[Switch-GigabitEthernet] ', ''],
        ["qx-config", "^\\s*interface\\s+vlan", "qx-Vlan", '[Switch-Vlan-interface] ', ''],
        ["qx-config", "^\\s*traffic\\s+classifier", "qx-classifier", '[Switch-classifier] ', ''],
        ["qx-config", "^\\s*qos\\s+policy", "qx-qospolicy", '[Switch-qospolicy] ', ''],
        ["qx-config", "^\\s*traffic\\s+behavior", "qx-behavior", '[Switch-behavior] ', '']
    ]

    def invoke_client(self, server: Server):
        """ shellの実装 """
        #
        if not server.event.is_set():
            print("test *** Client never asked for a shell.")
            return

        print(f"test is_set() OK! f={server.is_sftp_flag()}")
        if server.is_sftp_flag():
            # SFTpのときはこちらで無限待ちをする
            try:
                while self.transport is not None and self.transport.is_active():
                    time.sleep(1)
            finally:
                print("test finally (sftp)")
                return
        #
        self.channel.send(f"{self.prompt}")
        message = ''
        while not self.stop_flag:
            #
            if self.channel is None or not self.channel.active:
                break
            elif self.channel.recv_ready():
                output = self.channel.recv(1).decode("utf-8")
                if "\r" == output:
                    self.channel.send("\r\n")
                elif "\n" == output:
                    self.channel.send("\r\n")
                else:
                    if self.peek_state() != 'pass':
                        self.channel.send(output)
                    message = message + output
                    continue
                #
                trigger_flag = False
                for trigger in ServerStarter.TRIGGER:
                    if self.peek_state() != trigger[0] and '' != trigger[0]:
                        continue
                    resultX = re.search(trigger[1], message)
                    if resultX:
                        if '' != trigger[4]:
                            self.channel.send(trigger[4])
                        if '' != trigger[2]:
                            self.push_state(trigger[2])
                        trigger_flag = True
                        break
                result3 = re.search("^\\s*ssh\\s+([-_a-zA-Z0-9@]+)", message)
                if trigger_flag:
                    pass
                elif self.peek_state() in ['y/n', 'user']:
                    # print(f"test peek={self.peek_state()}")
                    self.pop_state()
                elif 'pass' in self.peek_state():
                    if not self.password_ng_flag:
                        self.pop_state()
                elif 'more' == self.peek_state():
                    self.channel.send(DISPLAY_CURRENT_CONFIGURATION_MORE)
                    self.pop_state()
                elif result3:
                    # 新しい状態を積む
                    ssh_state_flag = result3.group(1)
                    if 'password_ng' in ssh_state_flag:
                        self.password_ng_flag = True
                    else:
                        self.password_ng_flag = False
                    self.push_state(ssh_state_flag)
                    self.push_state('pass')
                    #
                    if random.randint(0, 1):
                        # ランダムにy/nを聞く
                        self.push_state('y/n')
                    #
                elif re.search("^\\s*(exit|quit)", message):
                    if not self.pop_state():
                        self.cleint_close()
                        return
                elif re.search("^\\s*enable", message):
                    if self.peek_state() == 'c1':
                        # 新しい状態を積む
                        self.push_state('c2')
                        # パスワードを聞く
                        self.push_state('pass')
                    else:
                        self.channel.send(ENABLE_ERROR)
                #
                # プロンプトを渡す
                self.channel.send(f'{self.prompt}')
                message = ''
            elif self.channel.exit_status_ready():
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
        th = threading.Thread(target=serverStarter.start, daemon=True)
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
                if 'base.ttl' in file:
                    continue
                if 'base1.ttl' in file:
                    continue
                if 'base2.ttl' in file:
                    continue
                #
                #
                ok_flag = False
                if '_ok_' in file:
                    print("test is OK test")
                    ok_flag = True
                else:
                    print("test is NG test")
                    ok_flag = False
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
                    print(f"test OK result_flag={str(result_flag)}")
                    assert result_flag, f"test OK f={file} e=/{error_data}/"
                else:
                    result_flag = result == 0
                    print(f"test NG result_flag={str(result_flag)}")
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
        #
        # スレッドだけ立てる(teratermでの評価用)
        serverStarter = ServerStarter(2200)
        #
        # カレントフォルダを保持する
        current_folder = os.getcwd()
        #
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start, daemon=True)
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
        except AssertionError as e:
            print(f"AssertionError happen: {e}")
        finally:
            print("test start finally")
            serverStarter.close()
            sys.exit(-1)
        #
        # カレントフォルダを元に戻す
        os.chdir(current_folder)
        #
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
#

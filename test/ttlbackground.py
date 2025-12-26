#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import socket
import threading
import paramiko
import sys
import re
import random
import subprocess
import platform
import typing
from serial.serialutil import SerialException
from abc import ABC, abstractmethod
from paramiko import SFTPServerInterface, SFTPServer, SFTPAttributes, SFTPHandle, SFTP_OK
try:
    from nextnextping.grammer.ttl_parser_worker import MyAbstractShell
    from nextnextping.grammer.ttl_parser_worker import MySerial
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT0
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT1
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from nextnextping.grammer.ttl_parser_worker import MyAbstractShell
    from nextnextping.grammer.ttl_parser_worker import MySerial
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT0
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT1


PING = '''PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.070 ms

--- localhost ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.070/0.070/0.070/0.000 ms
'''.replace('\n', '\r\n')

PING_CISCO = '''
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/3/5 ms
'''.replace('\n', '\r\n')

SHOW_RUNNING_CONFIG = '''Building configuration...

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
'''.replace('\n', '\r\n')

ENABLE_ERROR = "% Uncrecognized Command\r\n"

TRACERT = '''
Tracing route to t-ando [::1]
over a maximum of 30 hops:

  1    <1 ms    <1 ms    <1 ms  t-ando [::1]

Trace complete.

'''.replace('\n', '\r\n')

TRACEROUTE = '''traceroute to localhost (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1)  0.099 ms  0.075 ms  0.071 ms
'''

TRACEPATH = '''traceroute to localhost (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1)  0.099 ms  0.075 ms  0.071 ms
'''.replace('\n', '\r\n')

DISPLAY_CURRENT_CONFIGURATION = '''#
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
'''.replace('\n', '\r\n')

DISPLAY_CURRENT_CONFIGURATION_MORE = '''#
interface Vlan-interface1
 ip address 192.168.1.1 255.255.255.0
#
user-interface console 0
 authentication-mode password
 set authentication password cipher ********
#
'''.replace('\n', '\r\n')

IFCONFIG = '''eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1440
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

'''.replace('\n', '\r\n')

SHOW_IP_INTERFACE_BRIEF = '''Interface        IP-Address      OK? Method Status                Protocol
GigabitEthernet0/1 192.168.1.1     YES manual up                    up
GigabitEthernet0/2 192.168.2.1     YES manual up                    down
GigabitEthernet0/3 unassigned      YES manual administratively down down
'''.replace('\n', '\r\n')

IP_ADDR_SHOW = '''
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.255.255.254/32 brd 10.255.255.254 scope global lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:12:4a:cd brd ff:ff:ff:ff:ff:ff
    inet 172.xx.xx.xx/20 brd 172.xx.xx.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:cafe:babe:4acd/64 scope link
       valid_lft forever preferred_lft forever
'''.replace('\n', '\r\n')

IP_6_ADDR_SHOW = '''
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP qlen 1000
    inet6 fe80::215:cafe:babe:4acd/64 scope link
       valid_lft forever preferred_lft forever
'''.replace('\n', '\r\n')

IP_LINK_SHOW = '''
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:ca:fe:ba:be:cd brd ff:ff:ff:ff:ff:ff
'''.replace('\n', '\r\n')

IP_ROUTE_SHOW = '''
default via 172.xx.xx.1 dev eth0 proto kernel
172.xx.xx.0/20 dev eth0 proto kernel scope link src 172.xx.xx.xx
'''.replace('\n', '\r\n')

IP_6_ROUTE_SHOW = '''
default via 172.29.208.1 dev eth0 proto kernel
172.29.208.0/20 dev eth0 proto kernel scope link src 172.29.209.61
'''.replace('\n', '\r\n')

SS = '''
Netid State   Recv-Q Send-Q                                            Local Address:Port        Peer Address:Port      Process
u_dgr ESTAB   0      0                                                             * 16443                  * 11312     
u_str ESTAB   0      0                                   /run/systemd/journal/stdout 172                    * 6668      
u_str ESTAB   0      0                                                             * 10256                  * 10257     
u_dgr ESTAB   0      0                                                             * 22548                  * 11310     
u_dgr ESTAB   0      0                                                             * 16445                  * 16446 
'''.replace('\n', '\r\n')


class MyTelnetT1Server(MyTelnetT1):
    @typing.override
    def init_sender(self):
        ''' server '''
        self.echo = True
        self.print('test res IAC DO ECHO')
        self.send_binary(MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO)
        self.send('''Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Ubuntu 22.04.5 LTS
'''.replace('\n', '\r\n'))

    @typing.override
    def print(self, text):
        ''' print for server '''
        print(text)

    @typing.override
    def get_echo(self):
        return self.echo

    @typing.override
    def do_iac_will_echo(self, char_data):
        ''' クライアントが echo にはなりたくない '''
        self.do_iac_will_any(char_data)

    @typing.override
    def do_iac_do_echo(self, char_data):
        ''' サーバが echo になることは受け入れる '''
        self.send_binary(MyTelnetT1._IAC + MyTelnetT1._WILL + char_data)
        self.print('test res IAC DO ECHO')

    @typing.override
    def do_iac_do_NAWS(self, char_data):
        ''' サーバ側では DONT を返す '''
        self.do_iac_do_any(char_data)

    @typing.override
    def do_iac_do_Terminal_Type(self, char_data):
        ''' サーバ側では WONT を返す '''
        self.do_iac_do_any(char_data)


class StubServer(paramiko.ServerInterface):
    ''' SSHサーバの実装 '''

    def __init__(self):
        ''' コンストラクタ '''
        self.event = threading.Event()
        self.sftp_flag = False
        self.username = 'anonymouse'

    def check_channel_request(self, kind, chanid):
        ''' セッションの許可 '''
        # print(f"test check_channel_request kind={kind} ")
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        ''' パスワードチェック '''
        print(f"test username={username}  password=*****")
        self.username = username
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        ''' 認証の許可 '''
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_with_mic(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        ''' 認証の許可 '''
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        ''' 認証の許可 '''
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        ''' 認証の許可 '''
        return 'password,publickey'

    def check_channel_shell_request(self, channel):
        ''' shellの許可 '''
        print('test check_channel_shell_request')
        self.sftp_flag = False
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        ''' ptyの許可 '''
        return True

    def check_channel_subsystem_request(self, channel, name):
        ''' サブシステム要求の処理 '''
        print(f"test check_channel_subsystem_request {name}")
        self.sftp_flag = True
        self.event.set()
        return super().check_channel_subsystem_request(channel, name)

    def is_sftp_flag(self) -> bool:
        ''' sftpかどうかチェックする '''
        return self.sftp_flag

    def get_username(self) -> str:
        ''' sftpかどうかチェックする '''
        return self.username


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
            print('test list_folder OSError')
            return SFTPServer.convert_errno(e.errno)

    def stat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.stat(path))
        except OSError as e:
            print('test stat OSError')
            return SFTPServer.convert_errno(e.errno)

    def lstat(self, path):
        path = self._realpath(path)
        try:
            return SFTPAttributes.from_stat(os.lstat(path))
        except OSError as e:
            print('test lstat OSError')
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
            print('test open/0o666 OSError')
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
            print('test open/fdopen OSError')
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


class SSHServerStarter():
    ''' 実際のサーバ起動部分 '''

    KEY_FILE = 'test_rsa.key'  # キーファイルの位置

    def __init__(self, port: int):
        ''' コンストラクタ '''
        if os.path.isfile(SSHServerStarter.KEY_FILE):
            self.host_key = paramiko.RSAKey(filename=SSHServerStarter.KEY_FILE)
        else:
            self.host_key = paramiko.RSAKey.generate(2048)
            self.host_key.write_private_key_file(SSHServerStarter.KEY_FILE)
        #
        self.ttlClient = None
        self.DoGSSAPIKeyExchange = True
        self.port = port
        self.stop_flag = False
        self.channel = None
        self.client = None
        self.transport = None
        self.server_socket = None
        self.state = []
        self.prompt = None
        self.state = '$'

    def set_state(self, state: str):
        # stateの設定
        self.state = state

    def cleint_close(self):
        ''' この処理が呼ばれたらクライアントをクローズする '''
        print('test clinet close!')
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
        local_ttlClient = self.ttlClient
        self.ttlClient = None
        if local_ttlClient is not None:
            try:
                local_ttlClient.close()
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
        ''' close all '''
        #
        print('test close start!')
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
        ''' この処理が呼ばれたら停止する '''
        self.stop_flag = True

    def start(self):
        ''' 実処理 '''
        # now connect
        try:
            print(f"test bind port={self.port}")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.port))
            #
            if self.server_socket is None:
                raise paramiko.SSHException('self.server_socket is None')
            #
            # print('test Listen start ...')
            self.server_socket.listen(100)
            #
            while not self.stop_flag:
                print(f"test while loop start! port={self.port}")
                #
                local_socket = self.server_socket
                if local_socket is None:
                    raise paramiko.SSHException('self.server_socket is None')
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
            print('test finally self.close()')
            self.close()
        return 0

    def invoke_accept(self):
        ''' self.server_socket.accept()後の処理。本来であればスレッド化すべき個所 '''
        print(f"test invoke_accept port={self.port}")
        try:
            #
            self.transport = paramiko.Transport(self.client, gss_kex=self.DoGSSAPIKeyExchange)
            # self.transport.set_gss_host(socket.getfqdn(''))
            # self.transport.load_server_moduli()
            self.transport.add_server_key(self.host_key)
            self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer, StubSFTPServer)
            #
            print('test Server start!')
            server = StubServer()
            self.transport.start_server(server=server)
            #
            # wait for auth
            self.channel = self.transport.accept()
            if self.channel is None:
                print('test *** No channel.')
                return
            #
            # サブシステムが開始されるまで待機
            server.event.wait()
            #
            # client処理
            print(f"test invoke_client port={self.port}")
            self.invoke_client(server)
            #
        except OSError as e:
            print(f"test *** Client OSError: {str(e.__class__)} : {str(e)}")
        except paramiko.SSHException as e:
            print(f"test *** Client SSHException: {str(e.__class__)} : {str(e)}")
        finally:
            print(f"test finally self.cleint_close() port={self.port}")
            self.cleint_close()
        return

    def invoke_client(self, server: StubServer):
        ''' shellの実装 '''
        #
        if not server.event.is_set():
            print('test *** Client never asked for a shell.')
            return

        # print(f"test is_set() OK! f={server.is_sftp_flag()}")
        if server.is_sftp_flag():
            # SFTpのときはこちらで無限待ちをする
            try:
                while self.transport is not None and self.transport.is_active():
                    time.sleep(1)
            finally:
                print('test finally (sftp)')
                return
        #
        username = server.get_username()
        self.set_state(username)
        # print(f"test username={username} state={self.peek_state()} p={self.prompt}")
        #
        try:
            self.ttlClient = TtlClient()
            self.ttlClient.set_state(self.state)
            self.ttlClient.invoke_client_main(self.channel)
        except EOFError as e:
            print(f"test EOFError {e}")
        finally:
            if self.ttlClient is not None:
                self.ttlClient.close()
                self.ttlClient = None
        #


class TelnetServerStarter(ABC):
    ''' abstract telnet server '''

    def __init__(self, port: int):
        ''' __init__ '''
        #
        self.port = port
        self.state = '$'
        self.stop_flag = False
        self.client = None
        self.channel = None

    def set_state(self, state: str):
        self.state = state

    def cleint_close(self):
        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                pass
        self.client = None
        if self.channel is not None:
            try:
                self.channel.close()
            except Exception:
                pass
        self.channel = None

    def close(self):
        self.stop_flag = True
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except Exception:
                pass

    def start(self):
        ''' starter '''
        # now connect
        try:
            print(f"test telnet bind port={self.port}")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('localhost', self.port))
            self.server_socket.listen(1)
            #
            if self.server_socket is None:
                raise OSError('self.server_socket is None')
            #
            #
            while not self.stop_flag:
                print(f"test telnet while loop start! port={self.port}")
                #
                # print('test Listen start ...')
                self.client, _ = self.server_socket.accept()
                if self.client is None:
                    raise OSError('test telnet self.client is None')
                #
                try:
                    self.channel = self.channelFactory()
                    self.ttlClient = TtlClient()
                    self.ttlClient.set_state(self.state)
                    self.ttlClient.invoke_client_main(self.channel)
                except EOFError as e:
                    print(f"test EOFError {e}")
                finally:
                    self.cleint_close()
                #
        except OSError as e:
            print(f"test OS ERROR {e}")
        finally:
            print(f"test telnet finally self.close() port={self.port}")
            self.close()
        return 0

    @abstractmethod
    def channelFactory(self) -> MyTelnetT0:
        return None


class TelnetServerStarterT0(TelnetServerStarter):
    def __init__(self, port: int):
        ''' __init__ '''
        super().__init__(port)

    @typing.override
    def channelFactory(self) -> MyTelnetT0:
        return MyTelnetT0(self.client)


class TelnetServerStarterT1(TelnetServerStarter):
    def __init__(self, port: int):
        ''' __init__ '''
        super().__init__(port)

    @typing.override
    def channelFactory(self) -> MyTelnetT0:
        return MyTelnetT1Server(self.client)


class TtlClient():
    ''' 実際のサーバ起動部分 '''

    TRIGGER = [
        ['', '^\\s*ping\\s+', '', '', PING],
        ['', '^\\s*tracert', '', '', TRACERT],
        ['', '^\\s*traceroute', '', '', TRACEROUTE],
        ['', '^\\s*tracepath', '', '', TRACEPATH],
        ['', '^\\s*ifconfig', '', '', IFCONFIG],
        ['', '^\\s*pwd\\s*$', '', '', "/mnt/d/gitwork/nextnextping/test\n"],
        ['', '^\\s*ls', '', '', "xxxx\n"],
        ['', '^ip\\s+addr\\s+show\\s*$', '', '', IP_ADDR_SHOW],
        ['', '^ip\\s+6\\s+addr\\s+show\\s*$', '', '', IP_6_ADDR_SHOW],
        ['', '^ip\\s+link\\s+show\\s*$', '', '', IP_LINK_SHOW],
        ['', '^ip\\s+-6\\s+link\\s+show\\s*$', '', '', IP_LINK_SHOW],
        ['', '^ip\\s+route\\s+show\\s*$', '', '', IP_ROUTE_SHOW],
        ['', '^ip\\s+-6\\s+route\\s+show\\s*$', '', '', IP_6_ROUTE_SHOW],
        ['', '^ss\\s*$', '', '', SS],
        ['c1', '^\\s*ping\\s+', '', '', PING_CISCO],
        ['c2', '^\\s*show\\s+ip\\s+interface\\s+brief', '', '', SHOW_IP_INTERFACE_BRIEF],
        ['c2', '^\\s*config(ure)?\\s+terminal', 'config', 'Router(config)# ', ''],
        ['c2', '^\\s*ping\\s+', '', '', PING_CISCO],
        ['c2', '^\\s*show\\s+running-config', '', '', SHOW_RUNNING_CONFIG],
        ['config', '^\\s*vlan\\s+', 'config-vlan', 'Router(config-vlan)# ', ''],
        ['config', '^\\s*interface\\s+', 'config-if', 'Router(config-if)# ', ''],
        ['config', '^\\s*class-map\\s+', 'config-cmap', 'Router(config-cmap)# ', ''],
        ['config', '^\\s*policy-map\\s+', 'config-pmap', 'Router(config-pmap)# ', ''],
        ['config-pmap', '^\\s*class\\s+', 'config-pmap-c', 'Router(config-pmap-c)# ', ''],
        ['qx', '^\\s*display\\s+current-configuration', 'more', '-- More --', DISPLAY_CURRENT_CONFIGURATION],
        ['qx', '^\\s*system-view', 'qx-config', '[Switch]', ''],
        ['qx-config', '^\\s*interface\\s+gigabitethernet', 'qx-gbe', '[Switch-GigabitEthernet] ', ''],
        ['qx-config', '^\\s*interface\\s+vlan', 'qx-Vlan', '[Switch-Vlan-interface] ', ''],
        ['qx-config', '^\\s*traffic\\s+classifier', 'qx-classifier', '[Switch-classifier] ', ''],
        ['qx-config', '^\\s*qos\\s+policy', 'qx-qospolicy', '[Switch-qospolicy] ', ''],
        ['qx-config', '^\\s*traffic\\s+behavior', 'qx-behavior', '[Switch-behavior] ', '']
    ]

    def __init__(self, state='$'):
        self.prompt = None
        self.stop_flag = False
        self.set_state(state)
        self.password_ng_flag = False

    def set_state(self, state: str):
        ''' 外部から状態を更新する '''
        # 状態の初期化
        self.state = []
        # 状態更新
        self.push_state(state)
        #
        # パスワードNGフラグの解放
        self.password_ng_flag = False

    def push_state(self, state_base: str):
        state_base = state_base.lower()
        # print(f"test push_state ({state_base})")
        #
        trigger_flag = False
        for trigger in TtlClient.TRIGGER:
            if state_base == '':
                continue
            if trigger[0] == state_base or trigger[2] == state_base:
                trigger_flag = True
                break
        if trigger_flag:
            pass
        elif 'sudo' in state_base:
            state_base = 'sudo'
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
            state_base = '$'
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
        ''' ステートを使ってプロンプトを更新する '''
        state = self.state[-1]
        # print(f"update_prompt {state}")
        trigger_flag = False
        for trigger in TtlClient.TRIGGER:
            if trigger[2] == '':
                continue
            if trigger[2] == state:
                self.prompt = trigger[3]
                trigger_flag = True
                break
        if trigger_flag:
            pass
        elif 'sudo' == state:
            self.prompt = '[sudo] password for user_name:'
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
            if random.randint(0, 1):
                self.prompt = 'Are you sure you want to continue connecting (yes/no)?'
            else:
                self.prompt = 'Are you sure you want to continue connecting (yes/no/[fingerprint])?'
        elif 'vm' == state:
            self.prompt = '[root@localhost:~] '
        else:
            self.prompt = 'root@localhost:~$ '  # for linux
        # print(f"update_prompt s={state} p={self.prompt}")

    def close(self):
        #
        print('test close start!')
        self.stop_flag = True

    def invoke_client_main(self, channel):
        ''' client main '''
        print(f"test invoke_client_main start! {channel.__class__.__name__}")
        message = ''
        channel.send(f"{self.prompt}")
        output = ''
        while (not self.stop_flag):
            #
            if channel is None:
                print('test channel is None')
                break
            if channel.exit_status_ready():
                print('test Session ended')
                break
            if len(output) <= 0:
                if not channel.recv_ready():
                    time.sleep(0.1)
                    continue
                output = channel.recv(1024)
                if output is None:
                    break
                output = output.decode('utf-8')
            #
            # 一文字筒処理する
            index1 = output.find("\r")
            index2 = output.find("\n")
            if (index1 < 0) or ((0 <= index2) and (index2 < index1)):
                index1 = index2
            if index1 < 0:
                # 改行が存在しない
                if (self.peek_state() != 'pass') and (self.peek_state() != 'sudo'):
                    if not isinstance(channel, MyAbstractShell) or channel.get_echo():
                        time.sleep(0.1)
                        channel.send(output)
                message = message + output
                output = ''
                continue
            # 改行が存在する
            remain = output[0:index1]
            message = message + remain
            channel.send(f"{remain}\r\n")
            output = output[index1 + 1:]
            #
            message = message.strip()
            #
            # 行単位の処理をする
            #

            result3 = re.search('^ssh\\s+([-_a-zA-Z0-9@]+)', message)
            result4 = re.search('^(exit|quit)', message)
            if self.peek_state() in ['y/n', 'user', 'sudo']:
                # print(f"test peek={self.peek_state()}")
                self.pop_state()
            elif 'pass' in self.peek_state():
                if not self.password_ng_flag:
                    self.pop_state()
            elif 'more' == self.peek_state():
                channel.send(DISPLAY_CURRENT_CONFIGURATION_MORE)
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
            elif result4:
                # print(f"test exit {self.state}")
                if not self.pop_state():
                    break
            elif re.search('^\\s*sudo\\s+.*', message):
                if self.peek_state() == '$':
                    if random.randint(0, 1):
                        # ランダムでパスワードを聞く
                        self.push_state('sudo')
            elif re.search('^\\s*enable', message):
                if self.peek_state() == 'c1':
                    # 新しい状態を積む
                    self.push_state('c2')
                    # パスワードを聞く
                    self.push_state('pass')
                else:
                    channel.send(ENABLE_ERROR)
            else:
                for trigger in TtlClient.TRIGGER:
                    if self.peek_state() != trigger[0] and '' != trigger[0]:
                        continue
                    resultX = re.search(trigger[1], message)
                    if resultX:
                        if '' != trigger[4]:
                            channel.send(trigger[4])
                        if '' != trigger[2]:
                            self.push_state(trigger[2])
                        break
            #
            # プロンプトを渡す
            channel.send(f'{self.prompt}')
            message = ''

        print('test invoke_client_main end!')
        return


class TtlSerial():
    PTY_FILE = 'test_pty.key'  # キーファイルの位置

    def __init__(self):
        print('test TtlSerial start')
        self.proc = None
        self.channel = None
        self.ttlClient = None
        #
        cmd = 'socat -d -d PTY,raw,echo=0 PTY,raw,echo=0'
        cmd = cmd.split()
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.pty = []
        for line in self.proc.stdout:
            line = line.decode('utf-8').strip()
            result = re.search(r'PTY\s+is\s+(/dev/pts/.*)', line)
            if result:
                self.pty.append(result.group(1))
                if 2 <= len(self.pty):
                    break
        print(f'test get pty {self.pty[0]}')
        print(f'test get pty {self.pty[1]}')
        #
        # ttlを保存して外部から呼べるようにする
        with open(TtlSerial.PTY_FILE, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self.pty[0])
            f.write("\n")

    def start(self):
        ''' main loop '''
        try:
            while True:
                #
                self.channel = MySerial(self.pty[1], 9600)
                self.ttlClient = TtlClient()
                self.ttlClient.invoke_client_main(self.channel)
        except EOFError as e:
            print(f"test EOFError {e}")
        except SerialException as e:
            print(f"test SerialException {e}")
        finally:
            try:
                if self.channel is not None:
                    self.channel.close()
            except Exception:
                pass
            try:
                if self.ttlClient is not None:
                    self.ttlClient.close()
            except Exception:
                pass
            try:
                self.close()
            except Exception:
                pass
            print('test finally self.close()')

    def close(self):
        try:
            if self.channel is not None:
                self.channel.close()
        except Exception:
            pass
        try:
            if self.proc is not None:
                self.proc.terminate()
        except Exception:
            pass
        try:
            if self.ttlClient is not None:
                self.ttlClient = None
        except Exception:
            pass


class TTLLoaderBase():
    ''' TTLを読み込む '''

    def __init__(self):
        ''' ttl のテストをするためのフォルダ '''
        self.closeFlag = False

    def close(self):
        ''' 終了する '''
        self.closeFlag = True

    def start(self, files=None):
        ''' 実処理をする '''
        #
        #
        # カレントフォルダを保持する
        current_folder = os.getcwd()
        #
        serverStarter = SSHServerStarter(2200)
        ttlSerial = None
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start, daemon=True)
        # スレッドを開始
        th.start()
        #
        serverStarter = TelnetServerStarterT0(2201)
        ttlSerial = None
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start, daemon=True)
        # スレッドを開始
        th.start()
        #
        serverStarter = TelnetServerStarterT1(2202)
        ttlSerial = None
        # スレッドオブジェクトを作成
        th = threading.Thread(target=serverStarter.start, daemon=True)
        # スレッドを開始
        th.start()
        #
        #
        if platform.system().lower() == 'linux':
            #
            # シリアル起動
            ttlSerial = TtlSerial()
            # スレッドオブジェクトを作成
            th = threading.Thread(target=ttlSerial.start, daemon=True)
            # スレッドを開始
            th.start()
        #
        try:
            self.start_main(files)
        finally:
            # フォルダをもとに戻す
            os.chdir(current_folder)
            #
            if serverStarter is not None:
                serverStarter.close()
            if ttlSerial is not None:
                ttlSerial.close()
            #
            print('test start finally')

    def start_main(self, files=None):
        pass


class TTLLoaderSingle(TTLLoaderBase):
    def __init__(self):
        super().__init__()

    def start_main(self, files=None):
        print('test command#', end='')
        while True:
            cmd = input()
            if cmd == 'exit':
                break
            print('test command#', end='')


def main():
    tTLLoaderSingle = TTLLoaderSingle()
    tTLLoaderSingle.start()
    #
    sys.exit(-1)


if __name__ == '__main__':
    main()
#

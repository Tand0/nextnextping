import time
import os
import socket
import threading
import paramiko
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from grammer.TtlParserWorker import TtlPaserWolker


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

    def __init__(self, port: int, prompt='$'):
        """ コンストラクタ """
        if os.path.isfile(ServerStarter.KEY_FILE):
            self.host_key = paramiko.RSAKey(filename="test_rsa.key")
        else:
            self.host_key = paramiko.RSAKey.generate(2048)
            self.host_key.write_private_key_file("test_rsa.key")
        #
        self.DoGSSAPIKeyExchange = True
        self.port = port
        self.prompt = prompt
        self.stop_flag = False
        self.chan = None
        self.client = None
        self.t = None
        self.sock = None

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
                    self.chan.send(output)
                    message = message + output
                    continue
                if len(message) <= 0:
                    self.chan.send(f'{self.prompt}')
                    continue
                if 'exit' in message:
                    self.cleint_close()
                    return
                elif 'ping' in message:
                    self.chan.send("\r\n")
                    self.chan.send("Pinging t-ando [::1] with 32 bytes of data:\r\n")
                    self.chan.send("Reply from ::1: time<1ms\r\n")
                    self.chan.send("Reply from ::1: time<1ms\r\n")
                    self.chan.send("Reply from ::1: time<1ms\r\n")
                    self.chan.send("Reply from ::1: time<1ms\r\n")
                    self.chan.send("\r\n")
                    self.chan.send("Ping statistics for ::1:\r\n")
                    self.chan.send("    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\r\n")
                    self.chan.send("Approximate round trip times in milli-seconds:\r\n")
                    self.chan.send("    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n")
                    self.chan.send("\r\n")
                    self.chan.send(f'{self.prompt}')
                    message = ''
                else:
                    self.chan.send(f'{self.prompt}')
                    message = ''
            elif self.chan.exit_status_ready():
                print("test Session ended")
                break
            else:
                time.sleep(0.1)
        print("test recv_ready end!")
        return


def test_mkdir():
    """ フォルダが作れるか確認する """
    os.makedirs("test/build", exist_ok=True)


def test_load_ttl():
    """ ttlファイルが動作するか確認する """
    serverStarter = ServerStarter(2200, prompt="#")
    # スレッドオブジェクトを作成
    th = threading.Thread(target=serverStarter.start)
    # スレッドを開始
    th.start()
    try:
        files = os.listdir('test')
        for file in files:
            #
            #
            if '.ttl' not in file:
                continue
            #
            ok_flag = False
            if 'ok' in file:
                ok_flag = True
            #
            file = 'test/' + file
            print()
            print(f"test file={file}")
            #
            ttlPaserWolker = TtlPaserWolker()
            ttlPaserWolker.execute(file, [])
            result = ttlPaserWolker.getValue('result')
            error_data = ttlPaserWolker.getValue('error')
            print(f"test result={result}")
            if '' != error_data:
                print(f"test error={error_data}")
            if ok_flag:
                assert int(result) != 0, f"f={file}"
            else:
                assert int(result) == 0, f"f={file}"
            #
    finally:
        print("test_load_ttl finally")
        serverStarter.close()
    #


if __name__ == "__main__":
    serverStarter = ServerStarter(2200, prompt="#")
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
    #

#

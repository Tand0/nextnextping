import time
import os
import socket
import threading
import paramiko
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from grammer.TtlParserWorker import TtlPaserWolker


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        # print(f"test check_channel_request kind={kind} ")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # print(f"test username={username}  password={password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_with_mic(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        # print("test check_channel_shell_request")
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


class ServerStarter():
    KEY_FILE = "test_rsa.key"

    def __init__(self, port: int, prompt='$'):
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
        print("test clinet close!")
        #
        local_chan = self.chan
        self.chan = None
        if local_chan is not None:
            try:
                local_chan.close()
            except Exception:
                pass
        #
        local_t = self.t
        self.t = None
        if local_t is not None:
            try:
                local_t.close()
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
        #
        print("test close start!")
        #
        self.exit_flag = True
        #
        self.stop()
        self.cleint_close()
        #
        local_sock = self.sock
        self.chan = None
        self.sock = None
        if local_sock is not None:
            try:
                local_sock.close()
            except Exception:
                pass

    def stop(self):
        self.stop_flag = True

    def start(self):
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
            exit_flag = False
            while not exit_flag:
                print("test while loop start!")
                #
                print("test Accept start ...")
                #
                if self.sock is None:
                    return paramiko.SSHException("self.sock is None")
                else:
                    self.client, _ = self.sock.accept()
                #
                try:
                    print("test Got a connection!")
                    self.t = None
                    self.chan = None
                    #
                    self.t = paramiko.Transport(self.client, gss_kex=self.DoGSSAPIKeyExchange)
                    self.t.set_gss_host(socket.getfqdn(""))
                    self.t.load_server_moduli()
                    self.t.add_server_key(self.host_key)
                    #
                    server = Server()
                    #
                    self.t.start_server(server=server)
                    #
                    # wait for auth
                    self.chan = self.t.accept()
                    if self.chan is None:
                        print("test *** No channel.")
                        continue
                    #
                    print("test Authenticated!")
                    #
                    server.event.wait(10)
                    if not server.event.is_set():
                        print("test *** Client never asked for a shell.")
                        continue
                    #
                    print("test is_set() OK!")
                    #
                    self.chan.send(f"{self.prompt}")
                    message = ''
                    while not self.stop_flag and not exit_flag:
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
                                break
                            else:
                                self.chan.send(f'{self.prompt}')
                                message = ''
                        elif self.chan.exit_status_ready():
                            print("test Session ended")
                            break
                        else:
                            time.sleep(0.1)
                    print("test recv_ready end!")
                except Exception as e:
                    print("test *** Client exception: " + str(e.__class__))
                finally:
                    self.cleint_close()
        except Exception as e:
            print("test *** Caught exception: " + str(e.__class__) + ": " + str(e))
            return 1
        finally:
            self.close()
        return 0


def test_load_ttl():
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
        while True:
            cmd = input()
            if cmd == "exit":
                break
            print(f"test command c={cmd}")
    finally:
        print("test start finally")
        serverStarter.close()
        sys.exit(-1)
    #

#

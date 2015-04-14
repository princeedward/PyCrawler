# request serialization definition
# the first one character decides
# wehter it is a submit[s], request[r] or quit[q]
# the next two char are digit ranging from 0~99 mark the length of the domain
# the following is the domain name string, the length is specified by digits
# The last is the type of the dns resolving request, which includes:
#   A: rr.A
# If the string is not recognized, then send A request
import adns
import SocketServer
import threading
from multiprocessing import Process
import socket
import sys


# This is the handler of the request
# This implemented the persistence connection
# A manual shutdown signal has to be sent to the socket
class ThreadedRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        while True:
            try:
                data = self.rfile.readline().strip()
            except Exception as e:
                print e  # log exception to terminal
                break
            request_type = data[0]
            if request_type == "s":
                self._subHandle(data)
            elif request_type == "r":
                response = self._reqHandle(data)
                try:
                    self.wfile.write(response)
                except Exception:
                    break
            elif request_type == "q":
                break
            else:
                # TODO: Think about this situation
                break
        try:
            self.wfile.write("q\n")
        except Exception:
            pass

    def _subHandle(self, data):
        digit = int(data[1:3])
        domain = data[3:3+digit]
        record_type = data[3+digit:]
        if record_type == "CNAME":
            query = self.server.c.submit(domain, adns.rr.CNAME)
        else:
            query = self.server.c.submit(domain, adns.rr.A)
        self.server.host_cache[query] = domain

    def _reqHandle(self, data):
        digit = int(data[1:3])
        domain = data[3:3+digit]
        if domain in self.server.ip_cache:
            ip = self.server.ip_cache[domain]
        else:
            ip = ""
        digit_length = str(len(ip))
        if len(digit_length) == 1:
            response = "".join(["0", digit_length, ip, '\n'])
        else:
            response = "".join([digit_length, ip, '\n'])
        return response


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, others):
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)
        self.c = others[0]
        self.ip_cache = others[1]
        self.host_cache = others[2]


class DnsChecker(Process):

    def __init__(self, host, port):
        Process.__init__(self)
        self.adns_state = adns.init()
        self.ip_cache = {}
        self.host_cache = {}
        self.server = ThreadedTCPServer((host, port),
                                        ThreadedRequestHandler,
                                        (self.adns_state, self.ip_cache,
                                         self.host_cache))
        self.host, self.port = self.server.server_address

        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self._stop = threading.Event()

    def close(self):
        self._stop.set()

    def run(self):
        print "DNS cache server is running at: %s:%d" % (self.host, self.port)
        print "This server uses BIND9 and GNU adns library to resolve dns"
        print "To submit queries," \
            " please use DnsBuffer() function to create a query object"
        self.server_thread.start()
        while not self._stop.isSet():
            for query in self.adns_state.completed():
                ip = query.check()
                host = self.host_cache[query]
                del self.host_cache[query]
                if len(ip[3]) >= 1:
                    self.ip_cache[host] = ip[3][0]
        self.server.shutdown()

    def __del__(self):
        self.server.shutdown()
        self.close()


def DnsCacher(host="localhost", port=5436):
    dns_checker = DnsChecker(host, port)
    dns_checker.daemon = False
    dns_checker.start()
    return dns_checker


class DnsRequirer:

    def __init__(self, host, port, restart=False):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._restart_flag = restart

    def submit(self, domain, rtype="A"):
        if len(domain) > 100:
            return False
        digit = str(len(domain))
        if len(digit) == 1:
            request = "".join(["s0", digit, domain, rtype, '\n'])
        else:
            request = "".join(["s", digit, domain, rtype, '\n'])
        try:
            self.socket.sendall(request)
        except socket.error:
            if self._restart_flag:
                self.restart()
                self.socket.sendall(request)
                return True
            else:
                raise
        else:
            return True

    def require(self, domain):
        if len(domain) > 100:
            return None
        digit = str(len(domain))
        if len(digit) == 1:
            request = "".join(["r0", digit, domain, '\n'])
        else:
            request = "".join(["r", digit, domain, '\n'])
        try:
            return self._requireIP(request)
        except socket.error:
            if self._restart_flag:
                self.restart()
                return self._requireIP(request)
            else:
                raise
                return None

    def _requireIP(self, request):
        self.socket.sendall(request)
        response = self.socket.recv(1024).strip()
        digit = int(response[0:2])
        ip = response[2:2+digit]
        return ip

    def restart(self):
        try:
            self.socket.sendall("q\n")
        except Exception:
            pass
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def __del__(self):
        try:
            self.socket.sendall("q\n")
        except Exception:
            pass
        finally:
            self.socket.close()


def DnsBuffer(host="localhost", port=5436):
    dns_request = DnsRequirer(host, port)
    return dns_request

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        dns_checker = DnsChecker(args[0], args[1])
    else:
        dns_checker = DnsChecker(host="localhost", port=5436)
    dns_checker.daemon = True
    dns_checker.start()
    dns_checker.join()

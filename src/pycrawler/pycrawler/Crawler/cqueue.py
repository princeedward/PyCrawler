# This is a queue data structure wrapper
# The cQueue class in this module will be used to store the jobs
# And manage the politeness of the crawler
# This module later will provide a independent sockectserver which will run on a
# single process to provide memmory usage efficiency
import multiprocessing
import multiprocessing.queues as mltq
from time import gmtime, mktime
from reppy.cache import RobotsCache
from pycrawler.Store.NoSQL import NoSQLDict
from pycrawler.Crawler.fetcher import Job
# -- for daemon interface --
import SocketServer
import socket
import threading
import pycrawler.Crawler.job_pb2 as job_pb2

MAX_MESSAGE_SIZE = 3500000


class RobotsCacheCheckpoint(RobotsCache):
    """ A customized RobotsCache object to store robot.txt into databse
    """

    def __init__(self, store, *args, **kwargs):
        RobotsCache.__init__(self, *args, **kwargs)
        self._store = store
        self._cache = NoSQLDict(dbtype=self._store["engine"],
                                param={'host': self._store['host'],
                                       'port': self._store['port'],
                                       'db': self._store['db']['robot']})

    def clear(self):
        self._cache = NoSQLDict(dbtype=self._store["engine"],
                                param={'host': self._store['host'],
                                       'port': self._store['port'],
                                       'db': self._store['db']['robot']})

class cQueue(mltq.Queue):

    def __init__(self, param):
        mltq.Queue.__init__(self)
        self._cached_domain = {}
        #  self._robot_cache = RobotsCache()
        self._robot_cache = RobotsCacheCheckpoint(param["database"])
        self._default_delay = param["crawldelay"] if "crawldelay" in param \
            else 1
        self._agent_name = param["agentname"] if "agentname" in param \
            else "PyBot/0.1"

    def put(self, obj, block=True, timeout=None):
        mltq.Queue.put(self, obj, block, timeout)

    def get(self, block=True, timeout=None):
        # this is a naive queue implmentation
        # Check the domain crawling record
        # If the politeness constraints are not satisfied
        # Put the job at the end of the queue

        # TODO: Performance needs to be measured
        # This may cause uneccessary block
        # Thread safe needs to be guaranteed
        while True:
            job = mltq.Queue.get(self, block, timeout)
            if not self._robot_cache.allowed(job.url, self._agent_name):
                continue  # If the url is not allowed to crawl, then disgard
            domain = job.host
            current_time = gmtime()
            if not domain or domain not in self._cached_domain:
                self._cached_domain[domain] = current_time
                return job
            last_visit = self._cached_domain[domain]
            time_diff = mktime(current_time) - mktime(last_visit)
            crawl_delay = self._robot_cache.delay(job.url, self._agent_name) \
                if self._robot_cache.delay(job.url, self._agent_name) else \
                self._default_delay
            if time_diff >= crawl_delay:
                self._cached_domain[domain] = current_time
                return job
            else:
                self.put(job, timeout=timeout)


# -- This following is a daemon interface --
class cQueueThreadRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # persistent connection
        while not self.server.stop.isSet():
            try:
                data = self.rfile.readline().strip()
            except Exception as e:
                print e
                break
            request_type = data[0]  # request type: a: add; g: get; q: quit
            if request_type == "a":
                self._addHandle(data)
            elif request_type == "g":
                response = self._getHandle(data)
                try:
                    self.wfile.write(response)
                except:
                    break
            elif request_type == "q":
                break
            else:
                print "Unrecoginized request from %s" % (
                    self.request.getpeername())  # TODO: not support on some sys
            try:
                self.wfile.write("q\n")
            except:
                pass

    def _addHandle(self, data):
        length = int(data[1:5], 16)
        content = data[5:5+length]
        new_job_ms = job_pb2.Job()
        new_job_ms.ParseFromString(content)
        new_job = MessageToJob(new_job_ms)
        self.server.job_queue.put(new_job)

    def _getHandle(self, data):
        job = self.server.job_queue.get()
        job_ms = JobToMessage(job)
        content = job_ms.SerializeToString()
        if len(content) > MAX_MESSAGE_SIZE:
            print "Serialized job size is too big"
            # Job is too big and has been disgarded, please re-request
            return "d\n"
        length = hex(len(content))
        length = length[2:]
        length = "0"*(4-len(length)) + length
        return "".join(["r", length, content, "\n"])


class cQueueTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, others):
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)
        self.job_queue = others[0]
        self.stop = others[1]


class cQueueProcess(multiprocessing.Process):

    def __init__(self, host, port):
        multiprocessing.Process.__init__(self)
        self._job_queue = cQueue()
        self._stop = threading.Event()
        self._server = cQueueTCPServer((host, port),
                                       cQueueThreadRequestHandler,
                                       (self._job_queue, self._stop))
        self.host, self.port = self._server.server_address
        self._server_thread = threading.Thread(
            target=self._server.serve_forever)
        self._server_thread.daemon = True

    def close(self):
        self._stop.set()
        self._server.shutdown()

    def run(self):
        self._server_thread.start()
        self._server_thread.join()

    def __del__(self):
        self.close()


def cQueueBuilder(host="localhost", port="0"):
    new_cqueue = cQueueProcess(host, port)
    new_cqueue.daemon = False
    new_cqueue.start()
    return new_cqueue.host, new_cqueue.port, new_cqueue


def MessageToJob(msg):
    url = str(msg.url)
    param = {}
    param["host"] = str(msg.host)
    if msg.HasField("host_ip"):
        param["host_ip"] = str(msg.host_ip)
    return Job(url, param)


def JobToMessage(job):
    job_msg = job_pb2.Job()
    job_msg.url = job.url
    job_msg.host = job.host
    if job.host_ip:
        job_msg.host_ip = job.host_ip
    return job_msg


class cQueueMessager:

    def __init__(self, host, port, restart=False):
        self.host = host
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
        self._restart_flag = restart

    def put(self, job):
        job_msg = JobToMessage(job)
        job_msg_str = job_msg.SerializeToString()
        if len(job_msg_str) > MAX_MESSAGE_SIZE:
            return False
        length = hex(len(job_msg_str))[2:]
        length = "0"*(4-len(length)) + length
        msg = "".join(["a", length, job_msg_str, "\n"])
        try:
            self._socket.sendall(msg)
        except socket.error:
            if self._restart_flag:  # retry once
                self.restart()
                self.socket.sendall(msg)
                return True
            else:
                raise
        return True

    def get(self):
        try:
            self._socket.sendall("g\n")
            response = self._readResponse()
            new_job_msg = job_pb2.Job()
            new_job_msg.ParseFromString(response)
            return MessageToJob(new_job_msg)
        except socket.error:
            if self._restart_flag:
                self.restart()
                self._socket.sendall("g\n")
                response = self._readResponse()
                new_job_msg = job_pb2.Job()
                new_job_msg.ParseFromString(response)
                return MessageToJob(new_job_msg)
            else:
                raise
        return None

    def _readResponse(self):
        response = self._socket.recv(1024)
        resp_type = response[0]
        if resp_type == "q":
            return "q"
        elif resp_type == "r":
            length = int(response[1:5], 16)
            results = [response[5:]]
            remianing = length - 1024
            while remianing > 0:
                response = self._socket.recv(1024)
                results.append(response)
                remianing -= 1024
            combined = "".join(results)
            return combined.strip()
        else:
            return None

    def restart(self):
        try:
            self._socket.sendall("q\n")
        except Exception:
            pass
        self._socket.close()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

    def __del__(self):
        try:
            self._socket.sendall("q\n")
        except Exception:
            pass
        finally:
            self._socket.close()


def cQueueQuerier(host, port):
    return cQueueMessager(host, port)

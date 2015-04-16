import unittest
from NoSQL import NoSQL
import redis
import multiprocessing
from test_data import  BIG_LIST

class test_nosql(unittest.TestCase):

    def test_database_type(self):
        param = {}
        # test wrong database type
        with self.assertRaises(ValueError):
            db = NoSQL("rdeis", param)
            db = NoSQL("Redis", param)
            db = NoSQL("BDb", param)
        # test right database type
        try:
            db = NoSQL("redis", param)
            db = NoSQL("bdb", param)
        except Exception:
            self.fail("Correct database names, unexpected exceptions")

    def test_redis_init(self):
        # test bad init parameters
        param = {"host": "localhost", "port":6379, "db":0}
        try:
            db = NoSQL("redis", param)
            db.set("foo","bar")
        except Exception: #TODO: Change this to dictionary no key exception
            self.fail("Unexpected redis NoSQL instance init exception")
        param = {"host": "localhost", "port":"6379", "db":0}
        try:
            db = NoSQL("redis", param)
            db.set("foo", "bar")
        except Exception:
            self.fail("Unexpected redis NoSQL instance init exception")
        with self.assertRaises(redis.ConnectionError):
            # Port number cannot be string
            param = {"host": "localhost", "port":"6379", "db":"0"}
            db = NoSQL("redis", param)
            db.set("foo", "bar")
            param = {"host": "big", "port":"6379", "db":0}
            db = NoSQL("redis", param)
            db.set("foo", "bar")
            param = {"host": "localhost", "port":"dog", "db":0}
            db = NoSQL("redis", param)
            db.set("foo", "bar")
            param = {"host": "localhost", "port":"6379", "db":"5f"}
            db = NoSQL("redis", param)
            db.set("foo", "bar")
            param = {"host": "localhost", "port":"6d379", "db":0}
            db = NoSQL("redis", param)
            db.set("foo", "bar")


    def test_redis_set_value(self):
        # ---- test set key value pairs -------
        # test no string type key and values
        # test concurrent set and get(different keys and same key)
        p = multiprocessing.Pool(100)
        # -- concurrent set
        BIG_PAIRS = [(str(i), BIG_LIST[i]) for i in xrange(len(BIG_LIST))]
        def worker(pairs):
            param = {}
            db = NoSQL("redis", param)
            db.set(pairs[0], pairs[1])
        try:
            p.map(worker, BIG_PAIRS)
        except:
            self.fail("Concurrent writing fail, different keys")
        def worker2(value):
            param = {}
            db = NoSQL("redis", param)
            db.set("foo", value)
        try:
            p.map(worker2, BIG_LIST)
        except:
            self.fail("Concurrent writing fail, same keys")
        # -- concurrent get
        def worker(pairs):
            param = {}
            db = NoSQL("redis", param)
            db.get(pairs[0])
        try:
            p.map(worker, BIG_PAIRS)
        except:
            self.fail("Concurrent getting fail, different keys")
        def worker2(value):
            param = {}
            db = NoSQL("redis", param)
            db.get("foo")
        try:
            p.map(worker2, BIG_LIST)
        except:
            self.fail("Concurrent getting fail, same keys")
        # test fast serialized set and get
        # test different database concurrent write
        dbnum = range(10)
        def worker3(value):
            param["db"] = value
            db = NoSQL("redis", param)
            db.set("foo", "bar")
        try:
            p.map(worker3, dbnum)
        except:
            self.fail("Concurrent writing fail, different dbs")
        def worker3(value):
            param["db"] = value
            db = NoSQL("redis", param)
            db.get("foo")
        try:
            p.map(worker3, dbnum)
        except:
            self.fail("Concurrent getting fail, different dbs")

    def test_redis_set_dict(self):
        # ---- test set key dict pairs
        # test bad input data types
        # test concurrent set and get
        # test fast serialized set and get
        # test different database concurrent write
        pass

    def test_redis_destruct(self):
        # destruct should not raise error
        pass

def main():
    unittest.main()

if __name__ == "__main__":
    main()

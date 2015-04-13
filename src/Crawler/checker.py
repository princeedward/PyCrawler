from Store.NoSQL import NoSQL


def UrlChecker(job):
    db = NoSQL("redis", {"host": "localhost", "port": 6379, "db": 1})
    result = db.get(job.identifier)
    if result is None:
        return False, None
    return True, result

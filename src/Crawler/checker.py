from ..Store.NoSQL import NoSQL
import cPickle as pk
import email.utils as eut
from time import gmtime, strftime, mktime


def UrlChecker(job, param, headers):
    if "last-modified" in headers:
        last_update = eut.parsedate(headers["last-modified"])
    else:
        last_update = eut.parsedate(strftime("%a, %d %b %Y %H:%M:%S GMT",
                                             gmtime()))
    db = NoSQL(param["database"]["engine"],
               {"host": param["database"]["host"],
                "port": param["database"]["port"],
                "db": param["database"]["db"]["urlcache"]})
    result_str = db.get(job.identifier)
    # For the url that has never been cached before or deleted by LRU
    if result_str is None:
        result = {
            "last-modified": last_update,
            "url": job.url,
        }
        # TODO: shouldn't pickle at this levl
        db.set(job.identifier, pk.dumps(result))
        return False, result
    result = pk.loads(result_str)
    # For the urls that is not cached but has the same identifer
    if result["url"] != job.url:
        result["url"] = job.url
        result["last-modified"] = last_update
        db.set(job.identifier, pk.dumps(result))
        return False, result
    cached_date = result["last-modified"]
    hour_diff = (mktime(last_update) - mktime(cached_date))/3600
    if hour_diff >= param["crawlperiod"]:
        result["last-modified"] = last_update
        db.set(job.identifier, pk.dumps(result))
        return False, result
    return True, result

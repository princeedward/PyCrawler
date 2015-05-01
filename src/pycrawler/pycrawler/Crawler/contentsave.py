from setting import PARAM
import os
os.sys.path.append(PARAM["basedir"])
from Store.NoSQL import NoSQL


def SaveAndStatistics(job, content, param, **args):
    db = NoSQL(param["database"]["engine"],
               {"host": param["database"]["host"],
                "port": param["database"]["port"],
                "db": param["database"]["db"]["content"]})
    saves = {}
    saves["content"] = content
    saves["url"] = job.url
    saves["doctype"] = args["response_header"]["content-type"]
    saves["last-update"] = args["url_cache"]["last-modified"]
    db.dictset(job.identifier, saves)
    # do statistics below

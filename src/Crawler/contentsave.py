from Store.NoSQL import NoSQL


def SaveAndStatistics(job, content, **args):
    db = NoSQL(param["database"]["engine"],
               {"host": param["database"]["host"],
                "port": param["database"]["port"],
                "db": param["database"]["db"]["content"]})
    saves = {}
    save["content"] = content
    save["url"] = job.url
    save["doctype"] = args["response_header"]["content-type"]
    save["last-update"] = args["url_cache"]["last-modified"]
    db.dictset(job.identifier, saves)
    # do statistics below

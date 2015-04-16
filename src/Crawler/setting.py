import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Parallelization type:
# 0. single process
# 1. multithreading
# 2. multiprocessing
PARALLEL = 2

PROCESSNUM = 100

CRAWLDELAY = 1

# Minimum update period, unit: Hours
RECRAWL_FREQUENCY = 12

CHECKPOINT_FREQUENCY = 2

FILETYPES = set(["text/html",
                 "text/xml",
                 "text/plain",
                 "application/xhtml+xml",
                 "application/xml",
                 "application/atom+xml",
                 "application/rss+xml",
                 ])

MAXFILESIZE = 20000000

LANGUAGE = set(["en",
                "en-US",
                "en-gb",
                ])
DATABASE = {
    "default": {
        "engine": "redis",
        "host": "localhost",
        "port": 6379,
        "db": {"urlcache": 1, "content": 2, "meta": 3, "robot": 4},
        "username": "",
        "password": "",
    }
}

# pack the parameters into a single dictionary
PARAM = {
    "parallel": PARALLEL,
    "processnum": PROCESSNUM,
    "crawldelay": CRAWLDELAY,
    "crawlperiod": RECRAWL_FREQUENCY,
    "filetypes": FILETYPES,
    "language": LANGUAGE,
    "maxsize": MAXFILESIZE,
    "checkpoint_frequency": CHECKPOINT_FREQUENCY,
    "database": DATABASE["default"],
}

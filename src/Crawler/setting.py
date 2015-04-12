import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Parallelization type:
# 0. single process
# 1. multithreading
# 2. multiprocessing
PARALLEL = 2

PROCESSNUM = 100

CRAWLDELAY = 1

FILETYPES = set(["text/html", "text/xml", "text/plain"])

CHECKPOINT_FREQUENCY = 2

DATABASE = {
    "default": {
        "engine": "",
        "host": "",
        "port": 20,
        "username": "",
        "password": "",
    }
}

# pack the parameters into a single dictionary
PARAM = {
    "parallel": PARALLEL,
    "processnum": PROCESSNUM,
    "crawldelay": CRAWLDELAY,
    "filetypes": FILETYPES,
    "checkpoint_frequency": CHECKPOINT_FREQUENCY,
    "database": DATABASE["default"],
}

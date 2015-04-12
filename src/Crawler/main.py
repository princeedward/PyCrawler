import sys
import getopt
from setting import *


# option lists:
# -p int number of processes/threads used in crawling. default: 100
# -i int crawling delay. default: 1 s
# -f str faile types(multiple). default: text/html, text/xml, text/plain
# -c int chekcing point prequency. default: 2
# -d str database config name
def main(args):
    optlist, args = getopt.getopt(args, 'p:i:f:c:d:')
    options = {}
    for each in optlist:
        if each[0] in options:
            options[each[0]].append(each[1])
        else:
            options[each[0]] = [each[1]]
    # Set parameters
    if "-p" in options:
        try:
            PARAM["processnum"] = int(options["-p"][0])
        except ValueError:
            raise
    if "-i" in options:
        try:
            PARAM["crawldelay"] = float(options["-i"][0])
        except ValueError:
            raise
    if "-f" in options:
        PARAM["filetypes"] = set(options["-f"])
    if "-c" in options:
        try:
            PARAM["checkpoint_frequency"] = int(options["-c"][0])
        except ValueError:
            raise
    if "-d" in options:
        if options["-d"][0] in DATABASE:
            PARAM["database"] = DATABASE[options["-d"][0]]


if __name__ == "__main__":
    main(sys.argv[1:])

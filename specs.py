import pandas
import datetime
import logging
import logging.handlers
import sys

GITHUB_TOKENS = []

SPIDER_TRAP = 0.05

data = pandas.read_csv("top-repos.csv", header=0)

TOP_REPOS = data["repo_name"]
TOP_REPO_IDS = data["repo_id"]

STATS_TIMEOUT = 300
QUERY_INTERVAL = 30

MAX_CYCLE = 3
MAX_SEEN_QUEUE = 15

# Logging
now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(message)s')
fh = logging.handlers.RotatingFileHandler('logs/crawler'+now, mode='a', maxBytes=5*1024*1024)
sh = logging.StreamHandler(sys.stdout)
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

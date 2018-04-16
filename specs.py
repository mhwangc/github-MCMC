import pandas
import datetime
import logging
import logging.handlers
import sys

GITHUB_TOKENS = ["f36afb0b87470fe88c420a1da27c265bb2caab81", "8b748f83e389d682bce5584282f276c9596a3bc1", "74cb3a4715aea3274dff2119e9fccb5786849e17", "953d33b4353aa4bd60451127471e138bc36a46b2", "c374cc504b704b72b1e0bfa95f8479d0d7f810ed", "8a488574501e7637116f033cf3caa5a35e496a21"]

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

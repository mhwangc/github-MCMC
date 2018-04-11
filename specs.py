import pandas

GITHUB_TOKENS = []

SPIDER_TRAP = 0.1

data = pandas.read_csv("top-repos.csv", header=0)

TOP_REPOS = data["repo_name"]
TOP_REPO_IDS = data["repo_id"]

print(TOP_REPOS)
print(TOP_REPO_IDS)

# Logging
now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(message)s')
fh = logging.FileHandler('logs/crawler'+now)
sh = logging.StreamHandler(sys.stdout)
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
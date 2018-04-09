from github import Github
from store import Store
import random
import os
import json
import numpy as np

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

# TODO: Test out new code
# TODO: Implement stack, look for loops, logging etc

class GitHubCrawler:

    spider_trap = .01

    def __init__(self, token):
        self.g = Github(token)
        self.seen_users = Store("/users") # {ID: count}
        self.seen_repos = Store("/repos") # {ID: int}
        self.contributors_cache = Store("/cache") #([userID], [score])
        self.top_repos = ['kubernetes/kubernetes'] # repos to pick from

    # Takes in Repository object and returns User object or None
    def get_random_contributor(self, repository):
        if self.contributors_cache.read(repository.id) is None:
            contributors = list(repository.get_contributors())
            if len(contributors) == 0:
                return None
            contributors, scores = self.generate_commit_scores(contributors, repository)
            self.contributors_cache.write(repository.id, json.dumps((contributors,scores)), ttl=len(scores)*50)
            logger.info("Cached contributors and scores for %s", repository.full_name)
        else:
            contributors, scores = json.loads(self.contributors_cache.read(repository.id))
        random_contributor_id = np.random.choice(contributors, 1, p=scores)[0] 
        return self.g.get_user(random_contributor_id)

    # Takes in a Repository object and returns a list of contributor ids and a list of their percentage contributed 
    def generate_commit_scores(self, contributors, repo):
        contributor_ids = []
        scores = []
        total = 0
        for u in contributors:
            x = len(repo.get_commits(author=u))
            total += x
            contributor_ids.append(str(u.id))
            scores.append(x)
        scores = [float(score)/total for score in scores]
        return contributor_ids, scores

    # Takes in NamedUser object and returns Repository object or empty string
    def get_random_starred_repo(self, user):
        starred_repos = list(user.get_starred()) # Needed to fully paginate
        if not starred_repos:
            return None
        random_repo = random.choice(starred_repos)
        return random_repo

    # start can be a full name "user/repo" or an ID
    def crawl(self, start, iterations=-1):
        curr_repo = self.g.get_repo(start)
        logger.info("Starting at repository: %s (%s)", curr_repo.full_name, curr_repo.id)
        while iterations > 0:
            if random.random() < self.spider_trap:
                logger.info("Spider trap")
                break

            curr_user = self.get_random_contributor(curr_repo)
            if not curr_user:
                logger.info("User %s (%s) has no starred repositories", curr_user.login, curr_user.id)
                break

            self.seen_users.increment(curr_user.id)
            logger.info("Crawled to user: %s (%s)", curr_user.login, curr_user.id)

            curr_repo = self.get_random_starred_repo(curr_user)
            if not curr_repo:
                logger.info("Repository %s (%s) has no contributors", curr_repo.full_name, curr_repo.id)
                break

            self.seen_repos.increment(curr_repo.id)
            logger.info("Crawled to repository: %s (%s)", curr_repo.full_name, curr_repo.id)

            iterations -= 1
        if iterations != 0: # Spider trap
            self.crawl(random.choice(self.top_repos), iterations)

def main():
    g = GitHubCrawler(os.getenv('github-mcmc-token'), per_page=100)
    g.crawl('kubernetes/kubernetes', 10)

if __name__ == '__main__':
    main()





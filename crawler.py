import random
import os
import json
import numpy as np
import datetime
import logging
import socket

from github import Github
from store import Store
from specs import GITHUB_TOKENS, SPIDER_TRAP, TOP_REPOS, logger, STATS_TIMEOUT, QUERY_INTERVAL, MAX_CYCLE, MAX_SEEN_QUEUE
import time
import collections

# TODO: Test out new code
# TODO: Implement stack, look for loops, logging etc


class GitHubCrawler:

    def __init__(self, tokens):
        self.g_arr = [Github(token, per_page=100) for token in tokens]
        self.seen_users = Store("/users")  # {ID: count}
        self.seen_repos = Store("/repos")  # {ID: int}
        self.contributors_cache = Store("/cache")  # ([userID], [score])
        self.token_num = 0
        self.last_users = collections.deque([-1 for _ in range(MAX_SEEN_QUEUE)], MAX_SEEN_QUEUE)
        self.last_repos = collections.deque([-1 for _ in range(MAX_SEEN_QUEUE)], MAX_SEEN_QUEUE)

    # Rotates keys
    @property
    def g(self):
        self.token_num = (self.token_num+1)%len(self.g_arr)
        g = self.g_arr[self.token_num]
        return g
	

    # Takes in Repository object and returns User object or None
    def get_random_contributor(self, repository):
        read = self.contributors_cache.read(repository.id)
        if read is None:
            contributors, scores = self.generate_commit_scores(repository)
            if contributors is None:
                logger.info("Stats for %s timed out", repository.full_name)
                return None
            self.contributors_cache.write(repository.id, json.dumps((contributors,scores)), ttl=len(scores)*50)
            if len(contributors) == 0:
                return None
            logger.info("Cached contributors and scores for %s", repository.full_name)
        else:
            contributors, scores = json.loads(read)
        random_contributor_login = np.random.choice(contributors, 1, p=scores)[0] 
        return self.g.get_user(random_contributor_login)

    # Takes in a Repository object and returns a list of contributor ids and a list of their percentage contributed
    def generate_commit_scores(self, repo):
        contributors = list(repo.get_contributors())
        contributor_logins = []
        contributor_stats = repo.get_stats_contributors()
        scores = []
        total = 0
        if not contributor_stats and len(contributors) < 100:
            for u in contributors:
                x = len(list(repo.get_commits(author=u)))
                total += x
                contributor_logins.append(str(u.login))
                scores.append(x)
        else:
            timeout = 0
            while not contributor_stats and timeout <= STATS_TIMEOUT:
                time.sleep(QUERY_INTERVAL)
                timeout += QUERY_INTERVAL
                contributor_stats = repo.get_stats_contributors()
            if contributor_stats is None:
                return None, None
            for u in contributor_stats:
                total += u.total
                contributor_logins.append(str(u.author.login))
                scores.append(u.total)
        if len(contributor_logins) == 0 or total == 0:
            return None, None
        scores = [float(score)/total for score in scores]
        return contributor_logins, scores

    # Takes in NamedUser object and returns Repository object or empty string
    def get_random_starred_repo(self, user):
        starred_repos = list(user.get_starred()) # Needed to fully paginate
        if not starred_repos:
            return None
        random_repo = random.choice(starred_repos)
        return random_repo

    # start can be a full name "user/repo" or an ID
    def crawl(self, iterations=-1): 
        try:   
            while iterations != 0:
                curr_repo = self.g.get_repo(random.choice(TOP_REPOS))
                logger.info("Starting at repository: %s (%s)", curr_repo.full_name, curr_repo.id)
                while iterations != 0:
                    if random.random() < SPIDER_TRAP:
                        logger.info("Spider trap")
                        break

                    curr_user = self.get_random_contributor(curr_repo)
                    if not curr_user:
                        logger.info("Repository %s (%s) has no contributors", curr_repo.full_name, curr_repo.id)
                        break
                    if self.last_users.count(curr_user.id) >= MAX_CYCLE - 1:
                        logger.info("Seen user %s (%s) too many times", curr_user.login, curr_user.id)
                        break
                    self.last_users.appendleft(curr_user.id)

                    self.seen_users.increment(curr_user.id)
                    logger.info("Crawled to user: %s (%s)", curr_user.login, curr_user.id)
                    if random.random() < SPIDER_TRAP:
                        logger.info("Spider trap")
                        break

                    curr_repo = self.get_random_starred_repo(curr_user)
                    if not curr_repo:
                        logger.info("User %s (%s) has no starred repositories", curr_user.login, curr_user.id)
                        break
                    if self.last_repos.count(curr_repo.id) >= MAX_CYCLE - 1:
                        logger.info("Seen repo %s (%s) too many times", curr_repo.full_name, curr_repo.id)
                        break
                    self.last_repos.appendleft(curr_repo.id)

                    self.seen_repos.increment(curr_repo.full_name)
                    logger.info("Crawled to repository: %s (%s)", curr_repo.full_name, curr_repo.id)

                    iterations -= 1
            return iterations
        except socket.timeout:
            return iterations


def main():
    g = GitHubCrawler(GITHUB_TOKENS)
    iterations_left = -1
    while iterations_left:
        iterations_left = g.crawl(iterations_left)

if __name__ == '__main__':
    main()





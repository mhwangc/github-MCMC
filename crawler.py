from github import Github
from store import Store
import random
import os
import json

# TODO: Test out new code
# TODO: Implement stack, look for loops, logging etc

class GitHubCrawler:

    spider_trap = .01

    def __init__(self, token):
        self.g = Github(token)
        self.seen_users = Store("/users") # {ID: count}
        self.seen_repos = Store("/repos") # {ID: int}
        self.contributors_cache = Store("/cache") #{repoID: [userlogin]}
        self.top_repos = ['kubernetes/kubernetes'] # repos to pick from

    # Takes in Repository object and returns User object or None
    def get_random_contributor(self, repository):
        if self.contributors_cache.read(repository.id) is None:
            if len(repository.get_contributors()) == 0:
                return None
            scores, total = self.generate_commit_scores(repository)
            self.contributors_cache.write(repository.id, json.dumps(scores), ttl=len(scores)*50)
        else:
            scores = json.loads(self.contributors_cache.read(repository))
            total = 0
            for x, y in scores:
                total += y
        # TODO: Binary search w/ lottery
        random_contributor_login = random.choice(scores)[0]
        return self.g.get_user(random_contributor_login)

    # Takes in a Repository object and returns a mapping of users IDs to commit scores and the total score
    def generate_commit_scores(self, repo):
        scores = []
        total = 0
        for u in repo.get_contributors():
            x = len(repo.get_commits(author=u))
            total += x
            scores.append((u.id, x))
        return scores, total

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

        while iterations > 0:
            if random.random() < self.spider_trap:
                break

            curr_user = self.get_random_contributor(curr_repo)
            if not curr_user:
                break

            self.seen_users.increment(curr_user.id)
            print(curr_user.login)

            curr_repo = self.get_random_starred_repo(curr_user)
            if not curr_repo:
                break

            self.seen_repos.increment(curr_repo.id)
            print(curr_repo.name)

            iterations -= 1
        if iterations != 0: # Spider trap
            self.crawl(random.choice(self.top_repos), iterations)

def main():
    g = GitHubCrawler(os.getenv('github-mcmc-token'))
    g.crawl('kubernetes/kubernetes', 10)

if __name__ == '__main__':
    main()





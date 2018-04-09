from github import Github
import random
import os

class GitHubCrawler:

    spider_trap = .01

    def __init__(self, token):
        self.g = Github(token)
        self.seen_users = {} # {ID: count}
        self.seen_repos = {} # {ID: int}
        self.contributors_cache = {} #{repoID: [userlogin]}
        self.top_repos = ['kubernetes/kubernetes'] # repos to pick from

    # Takes in Repository object and returns User object or empty string
    def get_random_contributor(self, repository):
        if repository.id not in self.contributors_cache:
            contributors = list([user.login for user in repository.get_contributors()]) # Needed to fully paginate
            self.contributors_cache[repository.id] = contributors
        if not self.contributors_cache[repository.id]:
            return ""
        random_contributor_login = random.choice(self.contributors_cache[repository.id])
        return self.g.get_user(random_contributor_login)

    # Takes in NamedUser object and returns Repository object or empty string
    def get_random_starred_repo(self, user):
        starred_repos = list(user.get_starred()) # Needed to fully paginate
        if not starred_repos:
            return ""
        random_repo = random.choice(starred_repos)
        return random_repo


    # start can be a full name "user/repo" or an ID
    def crawl(self, start, iterations=-1):
        curr_repo = self.g.get_repo(start)
        while iterations !=0 :
            if random.random() < self.spider_trap:
                break
            curr_user = self.get_random_contributor(curr_repo)
            if not curr_user:
                break;
            if curr_user.id not in self.seen_users:
                self.seen_users[curr_user.id] = 0    
            self.seen_users[curr_user.id] += 1
            print(curr_user.login)
            curr_repo = self.get_random_starred_repo(curr_user)
            if not curr_repo:
                break
            if curr_repo.id not in self.seen_repos:
                self.seen_repos[curr_repo.id] = 0    
            self.seen_repos[curr_repo.id] += 1
            print(curr_repo.name)
            iterations -= 1
        if iterations != 0: # Spider trap
            self.crawl(random.choice(self.top_repos), iterations)

def main():
    g = GitHubCrawler(os.getenv('github-mcmc-token'))
    g.crawl('kubernetes/kubernetes', 10)



if __name__ == '__main__':
    main()





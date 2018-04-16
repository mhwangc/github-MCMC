from github import Github
import requests
import json
GITHUB_TOKENS = ["f36afb0b87470fe88c420a1da27c265bb2caab81", "8b748f83e389d682bce5584282f276c9596a3bc1", "74cb3a4715aea3274dff2119e9fccb5786849e17", "953d33b4353aa4bd60451127471e138bc36a46b2", "c374cc504b704b72b1e0bfa95f8479d0d7f810ed", "8a488574501e7637116f033cf3caa5a35e496a21"]

g_arr = [Github(token, per_page=100) for token in GITHUB_TOKENS]

def get_user_data(uid, github_token):
    headers = {'Authorization': 'token ' + github_token}
    url = "https://api.github.com/user/" + uid
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    return data["login"], data["followers"], data["following"], data["public_repos"]

# writes file of user ids, logins, followers, followeing, number public repos
def dump_users():
    curr = 0
    with open("results/userids.txt", "w+") as f:
        f.write("id, login, followers, following, public_repos,")
        with open("results/users2018-04-16-04-19", "r") as uids:
            for line in uids.readlines():
                uid = line.split(",")[0][7:]
                curr = (curr + 1) % len(GITHUB_TOKENS)
                login, followers, following, public_repos = get_user_data(uid, GITHUB_TOKENS[curr])
                data = [uid, login, followers, following, public_repos]
                data = [str(x) for x in data]
                string = ",".join(data) + ",\n"
                f.write(string)
                print(string)
    print("done")


def get_repo_data(name, github_token):
    headers = {'Authorization': 'token ' + github_token}
    url = "https://api.github.com/repos/" + name
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    return data["full_name"], data["stargazers_count"], data["language"], data["forks_count"]

# returns repo name, stars, language, number forks
def dump_repos():
    curr = 0
    start = False
    with open("results/repostats.txt", "a") as f:
        f.write("full_name,stargazers_count,language,forks_count,")
        with open("results/repos2018-04-16-04-19", "r") as repos:
            for line in repos.readlines():
                repo_name = line.split(",")[0][7:]
                curr = (curr + 1) % len(GITHUB_TOKENS)
                full_name, stargazers_count, language, forks_count = get_repo_data(repo_name, GITHUB_TOKENS[curr])
                data = [full_name, stargazers_count, language, forks_count]
                data = [str(x) for x in data]
                string = ",".join(data) + ",\n"
                f.write(string)
                print(string)
    print("done")




if __name__ == "__main__":
    dump_repos()

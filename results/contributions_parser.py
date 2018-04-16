import json

# Parser for data pulled from here: https://gist.github.com/paulmillr/2657075/

data = json.load(open("github-users-stats-contributions.json", encoding='utf-8'))
with open("contributions.txt", "w+") as f:
    for user in data:
        login = user["login"]
        contributions = user["contributions"]
        f.write(login+","+str(contributions)+",\n")

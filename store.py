import etcd
import os, sys, random

portnum = int(os.getenv("etcdport", "2379"))

hostname = []
for h in os.getenv("etcdhosts", "localhost").split(","):
    if h != "":
        hostname.append((h, portnum))

print("Connected to:", hostname)
client = etcd.Client(host=tuple(hostname), allow_reconnect=True)


class Store:

    def __init__(self, path):
        self.path = path

    # Returns the value stored at path/key
    def read(self, key):
        try:
            return client.read(self.path + "/" + str(key)).value
        except etcd.EtcdKeyNotFound:
            return None

    # Writes value to key at path/key
    def write(self, key, value, append=False, ttl=None):
        client.write(self.path + "/" + str(key), str(value), append=append, ttl=ttl)

    # Increments the value of key by 1, if it exists, or sets to 1 if not.
    def increment(self, key):
        v = self.read(key)
        if v is None:
            self.write(key, 1)
        else:
            self.write(key, int(v) + 1)

    # Lists all children of a directory
    def list(self, key):
        try:
            direc = client.get(self.path + "/" + str(key))
            return [(r.key, r.value) for r in direc.children]
        except etcd.EtcdKeyNotFound:
            return None

# Helper functions to test, clear, and see data


def clear_db(path):
    try:
        client.delete(path, recursive=True)
    except etcd.EtcdKeyNotFound:
        print(path, "is not a valid path")


def get_top_results(path="/repos", n=100):
    leaders = []
    try:
        direc = client.get(path)
        users = [r.key for r in direc.children]
        for u in users:
             direc2 = client.get(u)
             leaders.extend([(r.key, r.value) for r in direc2.children])
        print("Total of {0} repos in db".format(len(leaders)))
        print("Average of {0} points per repo".format(sum([int(x[1]) for x in leaders]) / len(leaders)))
        return sorted(leaders, key=lambda x: int(x[1]), reverse=True)[:n]
    except etcd.EtcdKeyNotFound:
        print(path, "is not a valid path")
        return []


def test():
    s = Store("/test")
    trials = 50
    record = {}
    for i in range(trials+1):
        x = random.randint(0, 10000)
        s.write("key" + str(i), str(x))
        record["/test/key" + str(i)] = x
    for _ in range(trials * 10):
        i = random.randint(0, trials)
        s.increment("key" + str(i))
        record["/test/key" + str(i)] += 1
    expected = []
    for k, v in record.items():
        expected.append((k, str(v)))
    expected = sorted(expected)
    b = sorted(s.list("/")) == expected
    print("Test Passed:", b)
    for result in get_top_results("/test/", trials // 5):
        print(result[0], ":", result[1])
    client.delete('/test', recursive=True)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Run with argument {test, clear, leader}.")
    if sys.argv[1] == "test":
        test()
    elif sys.argv[1] == "clear":
        clear_db("/repos/")
        clear_db("/users/")
        clear_db("/cache/")
    elif sys.argv[1] == "leader":
        for result in get_top_results():
            print(result[0], ":", result[1])
    else:
        print(sys.argv[1], "is not a valid argument. Choose from {test, clear, leader}.")



import etcd
import os

portnum = int(os.getenv("etcdport", "2379"))

hostname = []
for h in os.getenv("etcdhosts", "localhost").split(","):
    if h != "":
        hostname.append((h, portnum))

print(hostname)
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

if __name__ == '__main__':
    s = Store("/test")
    s.write("key1", "value1")
    s.write("key2", "value2")
    s.write("key3", 1)
    s.increment("key3")
    print(s.list("/"))
    client.delete('/test', recursive=True)


const { Container, allow } = require('@quilt/quilt');

function Etcd(n) {
  this.containers = [];
  for (var i = 0; i < n; i += 1) {
    this.containers.push(new Container("etcd", "quay.io/coreos/etcd:v3.3"));
  }

  const initialCluster = this.containers.map((c) => {
    const host = c.getHostname();
    return `${host}=http://${host}:2380`;
  });
  const initialClusterStr = initialCluster.join(',');

  this.containers.forEach((c) => {
    const host = c.getHostname();
    /* eslint-disable no-param-reassign */
    c.env.ETCD_NAME = host;
    c.env.ETCD_LISTEN_PEER_URLS = 'http://0.0.0.0:2380';
    c.env.ETCD_LISTEN_CLIENT_URLS = 'http://0.0.0.0:2379';
    c.env.ETCD_INITIAL_ADVERTISE_PEER_URLS = `http://${host}:2380`;
    c.env.ETCD_INITIAL_CLUSTER = initialClusterStr;
    c.env.ETCD_INITIAL_CLUSTER_STATE = 'new';
    c.env.ETCD_ADVERTISE_CLIENT_URLS = `http://${host}:2379`;
    /* eslint-enable no-param-reassign */
  });

  // Used by the cluster members to communicate with each other.
  allow(this.containers, this.containers, 2380);

  // Used for client connections. While not strictly necessary, it's
  // convenient for the containers in the cluster to be able to create a client
  // for debugging.
  allow(this.containers, this.containers, 2379);

  this.deploy = function deploy(deployment) {
    this.containers.forEach(container => container.deploy(deployment));
  };
}

module.exports.Etcd = Etcd;

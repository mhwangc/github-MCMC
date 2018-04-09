const quilt = require("@quilt/quilt");
const etcd = require("./etcd.js");


var namespace = quilt.createDeployment({
  namespace: "mcmc"
});

var sshKeys = quilt.githubKeys("hantaowang") // YOUR NAME HERE

var masterMachine = new quilt.Machine({
    provider: "Amazon",
    region: "us-west-1",
    size: "t2.large",
    sshKeys: sshKeys
});

var baseMachine = new quilt.Machine({
    provider: "Amazon",
    region: "us-west-1",
    size: "m4.large",
    sshKeys: sshKeys
});

// Set up etcd
function getHostnames(c) {
    return c.getHostname();
}
var etcdservice = new etcd.Etcd(3);
var etcdhostnames = etcdservice.containers.map(getHostnames).join(',');

// Set up server
var main = new quilt.Container('main', 'ubuntu', {
    env: {
        'etcdhosts': etcdhostnames,
        'etcdport': "2379",
    }
    
});

quilt.allow(quilt.publicInternet, etcdservice.containers, 2379);
quilt.allow(etcdservice.containers, quilt.publicInternet, 2379);

// Deploy
namespace.deploy(masterMachine.asMaster());
namespace.deploy(baseMachine.asWorker().replicate(3));
// namespace.deploy(main);
namespace.deploy(etcdservice.containers);
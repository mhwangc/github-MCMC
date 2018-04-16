Quilt Change Log
================

Up Next
-------------
- Fix a bug where `quilt setup-tls` would fail when writing to a directory whose
parent does not exist.
- Auto-generate TLS credentials when starting the daemon if the credentials in
`~/.quilt/tls` don't already exist.
- Always encrypt communication with the daemon.
- Try using the Quilt-managed SSH key when connecting to machines. The
Quilt-managed SSH key should work most of the time because the
daemon automatically grants it access to the cluster.
- Fix a bug where floating IPs would not get properly assigned in GCE.
- Add Infrastructure class for deploying Quilt machines. createDeployment()
and the Deployment class are now deprecated, and users should transition
to using Infrastructure instead.

JavaScript API-breaking changes:
- Remove the Container.replicate() method. Users should create multiple
containers by looping.

Release 0.4.0
-------------

Release 0.4.0 makes some minor UX improvements.

- Check for unexpected keys in the optional argument passed to the Machine,
Container, and Deployment constructors.
- Rename StitchID to BlueprintID in the database. This is an internal
API-breaking change (it changes the API between internal Quilt components).
- Fix TLS encryption for GRPC connections to machines that use floating IPs.
- Support Node.js version 6 (previously, we had some code that failed unless
users were running version 7 or later).

Release 0.3.0
-------------

Release 0.3.0 changes the way that containers are deployed. `Container`s can now
be deployed directly without wrapping them in a `LoadBalancer` (previously known
as `Service`). Many of the methods previously defined on `Service` (such as
`allowFrom` and `placeOn`) have been migrated to `Container` methods.

- Don't use the image cache on the Quilt master when building custom
Dockerfiles. This is necessary to fetch updates when Dockerfiles are
non-deterministic and rely on pulling data from the network.
- Use the latest stable release of Docker Engine.
- Fixed a bug where `quilt inspect` would panic when given a relative path.
- Use the latest release of OVS (2.7.2).
- Remove support for invariants.
- Remove support for placement based on service groups.
- Simplify machine-service placement. For example, deploying a service to a
floating IP is now expressed as `myService.placeOn({floatingIp: '8.8.8.8'})`.
- Remove `Service.connect`. Only `Service.allowFrom` can be used from now on.
- Restart containers if their hostname changes.
- Fix a bug where containers might get assigned duplicate hostnames.
- Remove `Service.children`. Container hostnames should be used from now on.
- Change the container constructor syntax to take optional settings as the
last argument:
```javascript
new Container('imageName', {
  command: ['command', 'args'],
  env: { key: 'val' },
  filepathToContent: { path: 'content' },
});
```
- Require a hostname to be provided to the container constructor:
```javascript
new Container('hostname', 'imageName');
```
- Hostnames are now immutable after the container is constructed -- the
`Container.setHostname` method has been removed.
- Containers can now be `deploy`ed directly without wrapping them in a Service.
Deploying a Service does _not_ deploy the Containers behind it -- the Containers
must be explicitly deployed.

API Breaking Changes:
- Make `placeOn` a method of `Container` rather than `Service`.
- Allow containers to explicitly connect to each other (rather than requiring
all connections to occur by connecting services).
- Change Service.allowFrom so that it allows connections to the load balancer,
and not directly to the containers that get load balanced over.
- Describe services in terms of hostnames rather than container IDs.
- Rename `Service` to `LoadBalancer`.

Release 0.2.0
-------------

Release 0.2.0 introduces two big features: load balancing, and TLS-encrypted
communication for Quilt control traffic.

To use load balancing, simply create and deploy a `Service` -- the hostname
associated with that `Service` will now automatically load balance traffic
across its containers.

TLS is currently optional. If the `tls-dir` flag is omitted, Quilt control
traffic will remain insecure as before.

To enable TLS, run `quilt setup-tls ~/.quilt/tls`, and then start the daemon
with `quilt daemon -tls-dir ~/.quilt/tls` (you can place the TLS certificates
in a different directory if you'd like -- just make sure that the same
directory is use for `setup-tls` and `daemon`). After the daemon starts, all
the subcommands will work as before.

What's new:

- Package the OVS kernel module for the latest DigitalOcean image to speed up
boot times.
- Renamed specs to blueprints.
- Load balancing.
- Upgraded to the latest Docker engine version (17.05.0).
- Fixed bug in Google provider that caused ACLs to be repeatedly added.
- Fixed inbound connections on the Vagrant provider. In other words,
`myService.allowFrom(publicInternet, aPort)` now works.
- Only allocate one Google network per namespace, rather than one network for
each region within a namespace.
- Implement debugging counters accessible through `quilt counters`.
- Disallow IP allocation in subnets governed by routes in the host network. This
fixes a bug where containers would sometimes fail to resolve DNS on DigitalOcean.
- Fixed a bug where etcd would sometimes restart when the daemon connected to machines
that had already been booted. This most visibly resulted in containers restarting.
- Use an exponential backoff algorithm when waiting for cloud provider actions
to complete. This decreases the number of cloud provider API calls done by Quilt.
- `quilt ps` is now renamed to `quilt show`, though the original `quilt ps`
  still works as an alias to `quilt show`.
- `quilt show` now displays the image building status of custom Dockerfiles.
- Let blueprints write to stdout. Before, if blueprints used `console.log`, the
text printed to stdout would break the deployment object.
- `quilt show` now has more status options for machines (booting, connecting,
connected, and reconnecting).
- Allow an admin SSH key access to all machines deployed by the daemon. The key is
specified using the `admin-ssh-private-key` flag to the daemon.
- Support for TLS-encrypted communication between Quilt clients and servers.

Release 0.1.0
-------------

Release 0.1.0 most notably modifies `quilt run` to evaluate Quilt specs using
Node.js, rather than within a Javascript implementation written in Go. This
enables users to make use of many great Node features, such as package management,
versioning, unit testing, a rich ecosystem of modules, and `use
strict`. In order to facilitate this, we now require `node` version 7.10.0 or
greater as a dependency to `quilt run`.

What's new:

- Fix a bug where Amazon spot requests would get cancelled when there are
multiple Quilt daemons running in the same Amazon account.
- Improve the error message for misconfigured Amazon credentials.
- Fix a bug where inbound and outbound public traffic would get randomly
dropped.
- Support floating IP assignment in DigitalOcean.
- Support arbitrary GCE projects.
- Upgrade to OVS2.7.
- Fix a race condition where the minion boots before OVS is ready.
- Build the OVS kernel module at runtime if a pre-built version is not
available.
- Evaluate specs using Node.js.

Release 0.0.1
-------------

Release 0.0.1 is an experimental release targeted at students in the CS61B
class at UC Berkeley.

Release 0.0.0
-------------

We are proud to announce the initial release of [Quilt](http://quilt.io)!  This
release provides an alpha quality implementation which can deploy a whole [host
of distributed applications](http://github.com/quilt) to Amazon EC2, Google
Cloud Engine, or DigitalOcean.  We're excited to begin this journey with our
inaugural release!  Please try it out and [let us
know](http://quilt.io/#contact) what you think.

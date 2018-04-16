[![Build Status](https://travis-ci.org/kelda/kelda.svg?branch=master)](https://travis-ci.org/kelda/kelda)
[![Go Report Card](https://goreportcard.com/badge/github.com/kelda/kelda)](https://goreportcard.com/report/github.com/kelda/kelda)
[![Code Coverage](https://codecov.io/gh/kelda/kelda/branch/master/graph/badge.svg)](https://codecov.io/gh/kelda/kelda)

# Quilt

Deploying applications to the cloud can be painful. Booting virtual machines, configuring
networks, and setting up databases, requires massive amounts of specialized knowledge —
knowledge that’s scattered across documentation, blog posts, tutorials, and source code.

Quilt aims to make sharing this knowledge simple by encoding it in JavaScript.  Just as
developers package, share, and reuse application code, Quilt’s JavaScript framework makes
it possible to package, share, and reuse the knowledge necessary to run applications in
the cloud.

To take this knowledge into production, simply `quilt run` the JavaScript blueprint of
your application. Quilt will set up virtual machines, configure a secure network, install
containers, and whatever else is needed to get up and running smoothly on your favorite
cloud provider.

## Deploy Quickly on...

![providers](./docs/source/images/providers.png)

## Install

Install Quilt with npm:

```bash
$ npm install -g @quilt/install
```
Check out more in our [Getting Started Guide](http://docs.quilt.io/#getting-started).

## API

Run any container.

[//]: # (b1)
<!-- const {Container, LoadBalancer, Machine, allow, publicInternet} = require('@quilt/quilt'); -->
```javascript
let web = new Container('web', 'someNodejsImage');
```

Load balance traffic.

[//]: # (b1)
```javascript
let webContainers = [];
for (i = 0; i < 3; i += 1) {
  webContainers.push(new Container('web', 'someNodejsImage'));
}
let webLoadBalancer = new LoadBalancer('web-lb', webContainers); // A load balancer over 3 containers.
```

Share and import blueprints via npm.

[//]: # (b1)
```javascript
const Redis = require('@quilt/redis');
let redis = new Redis(2, 'AUTH_PASSWORD'); // 2 Redis database replicas.
```

Set up a secure network.

[//]: # (b1)
```javascript
allow(publicInternet, webContainers, 80); // Open the webservers' port 80 to the public internet.
redis.allowFrom(webContainers); // Let the web app communicate with Redis.
```

Deploy VMs on any [supported cloud provider](#deploy-quickly-on).

[//]: # (b1)
```javascript
let vm = new Machine({
  provider: 'Amazon',
  size: 't2.micro'
});
```

See [full example blueprints](https://github.com/quilt/) and [check out our docs](http://docs.quilt.io).

## Quilt CLI

```bash
# Deploy your application.
$ quilt run ./someBlueprint.js

# SSH into VMs and containers.
$ quilt ssh <ID>

# Check the status of your deployment.
$ quilt show
```

This is just a small sample of the Quilt CLI. [Check out more handy commands](http://docs.quilt.io/#quilt-cli) for managing your deployment.

## Get Started

* Get started with [our **tutorial**](http://docs.quilt.io/#getting-started)
* Check out [our **docs**](http://docs.quilt.io/)
* [**Contribute** to the project](http://docs.quilt.io/#developing-quilt)
* Learn more on our [**website**](http://quilt.io)
* [**Get in touch!**](http://quilt.io/#contact)

We would love to hear if you have any questions, suggestions, or other comments!

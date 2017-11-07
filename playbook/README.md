## Current infrastructure

kiskadee current infrastructure runs in University of São Paulo. We have two
machines which we use for our staging and continuous integration environments,
respectively.

### Staging

http://143.107.45.126:30121

### Continuous integration

http://143.107.45.126:30130

#### Setup

To make sure jenkins is running,

- run the initialize.sh script under `/var/lib/jenkins`
- start nginx
- make sure selinux allows nginx to forward jenkins port: `setsebool -P httpd_can_network_connect 1`

**This should go in our playbooks at some point**

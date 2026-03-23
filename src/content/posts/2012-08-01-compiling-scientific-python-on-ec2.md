---
title: "Compiling yourself a Scientific Python Paradise on EC2"
date: 2012-08-01 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

First start by following the Starcluster directions found here:

[http://starcluster.scripts.mit.edu/~starcluster/wiki/index.php?title=StarCluster\_AMI\_Cookbook\_Ubuntu\_10.04](https://web.archive.org/web/20160318073715/http://starcluster.scripts.mit.edu/~starcluster/wiki/index.php?title=StarCluster_AMI_Cookbook_Ubuntu_10.04)

Notes:

1. The AMI they reference no longer exist, I used the 64 bit Ubuntu Maverick from here: [http://alestic.com/](https://web.archive.org/web/20160318073715/http://alestic.com/)
2. There are much newer versions ipython, so leave that out of the apt-get install process. You can download that later at your leisure.
3. When you are reenabling the root login, removing prefix commands means everything before rsa- . . . .
4. Also, on the root login section, the line number 67 is no longer valid for current versions. I hit the one on line number 86, and haven't had problems.
5. Given the merge of Sun and Oracle, you will need to find the Sun (cough), sorry, Oracle Grid engine, which is highly hidden in the oracle website. Here are the keys you need to find it: Get to the downlod section, and look in the "Oracle Enterpries Manager" product pack. "Grid engine media pack." Thanks to their nazi download system, it is unlikely you can retrieve this to your ec2 instance, instead download it locally, then scp it over. . . . Weak. At 820 megs, this is more than a little bit annoying.
6. To get the SGE and drmaa v0.2 (why is this needed?) Just boot a starcluster instance and pirateer the /opt directory to your new instance. You can get the old version of drmaa this way too.
7. The ubuntu package libopenmpi-dev now points at openmpi. This is fine. It all works just like the directions say. I ignored the ubuntu patch for openmpi, looks like it fixes some obscure bugs.

---
title: "Developing the Hard(ware) Way — 2"
date: 2018-10-04 12:00:00 +0000
---

*Originally published on [Medium](https://medium.com/@meawoppl/developing-the-hard-ware-way-2-2f328e2e2ec1)*

### Developing the Hard(ware) Way — 2

An approach that many have taken in this route is the addition of a requirement to do a hardware test at some interval. This process has many names, but the one that people fear the most is [**integration testing**](https://en.wikipedia.org/wiki/Integration_testing)**.**

Hardware integration testing is a simple notion: Attach the hardware, run the software. The friction all comes from the [SOUL of the hardware](https://medium.com/3scan-engineering/developing-the-hard-ware-way-1-73ef2b07fc3a).

![Hardware architecture](/images/hardware-dev/hardware-testing.webp)

First up, the hardware has mass. Perhaps if your are lucky, the mass is small enough for your engineers to carry, in [3Scan](http://www.3scan.com)’s case, each instrument weighs about a metric ton, which makes WFH a little tricky. Next you might consider setting up a centralized testing rig of some sort. This process comes with one of two caveats:

1. Engineers must queue up changes and force them to individually run against the hardware integration test bed.
2. You must divide your code-world by adding specialized (possibly human) logic to determine if a change requires hardware testing.

Approach #1 comes with comes with a huge burden of needing at least one engineer to become responsible for keeping that rig powered, maintained, and internet connected for anyone to get work done. Additionally, this ties all of your developers to a rivalrous and potentially complicated/unreliable resource. The uptime of the test-bed will be immediately linked to the throughput of your whole team. Taking this approach with every code change is the best way possible to slow the pace of development of your organization.

Approach #2 is the surefire fastest way to discourage people from making hardware adjacent changes, or worse, deform the code-base around desire to avoid the hardware testing loop. Your code-base will gain a feel reminiscent of the [Winchester Mansion](https://en.wikipedia.org/wiki/Winchester_Mystery_House) with walled off rooms to help people avoid the evil spirits.

The alternative to these, **doing nothing**, will guarantee that every, even seemingly trivial release, is a hellish, customer impacting, bug-ridden grind. The person responsible for the breaking changes (if it can even be known) will almost certainly called in to triage the problem, possibly weeks later, and will be discouraged from ever making future changes.

**As a small hardware heavy company you MUST be able to make fearless changes to your interfacing software if your company to succeed.**

[Next, I will show you how.](https://medium.com/@meawoppl/developing-the-hard-ware-way-3-6315a66c6d2d)
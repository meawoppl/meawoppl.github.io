---
title: "Closed Source Specs — MIPI Madness"
date: 2019-12-19 12:00:00 +0000
---

*Originally published on [Medium](https://medium.com/@meawoppl/closed-source-specs-mipi-madness-f7922ae26d26)*

### Closed Source Specs — MIPI Madness

While much has been written about the [infectious nature](https://news.ycombinator.com/item?id=1011426) of the GPL and similar licenses in the software industry, the hardware industry suffers a hugely worse and virtually unpublicized friction.

**The hardware digital world is held together by closed standards that you have to pay thousands of dollars (per year) to read.**

Lets talk about one of the most high-impact standards out that there that you probably don’t know you are using: MIPI. [The MIPI alliance](https://www.mipi.org/) hosts specifications for electrical device communication. These standards and protocols are the mortar that hold together basically every modern digital device. If it has a screen, camera, or radio has one of these specifications likely appears inside its guts.

Do you want to read about how it works? **Sorry!**

> All materials contained herein are protected by copyright laws, and may not be reproduced, republished, distributed, transmitted, displayed, broadcast or otherwise exploited in any manner without the express prior written permission of MIPI Alliance. MIPI, MIPI Alliance and the dotted rainbow arch and all related trademarks, tradenames, and other intellectual property are the exclusive property of MIPI Alliance and cannot be used without its express prior written permission.

This is a really curious conundrum when you think about it, these devices appear everywhere and are used by everyone, but trying to make a device that uses these specs is purposefully hard? Well, lets see who is part of the MIPI consortium…

Well, that is basically the list of companies you would come up with searching for “silicon megacorp”. Oh well, so what is a startup trying to integrate a device to do in this environment?

Well, there are 3 options:

* Social — Hire someone who already understands the protocol. Occulted knowledge does have value here! An alternative is making a friend who lets you look at the spec (without copying it obviously), so you can get your work done.
* Technical — Reverse engineer the protocol by spending hours looking at fuzzy oscilloscope traces, [open source implementations](https://github.com/SymbioticEDA/MARLANN/blob/master/demo/camera/cameraif.v), schematics, and other devices. This is doable, [legal](https://www.eff.org/issues/coders/reverse-engineering-faq), but remarkably time consuming. :(
* Indirect — Somewhat curiously vendors who sell devices that utilize the MIPI protocols and standards routinely provide direct screenshots from the specification documents within their own standards.

The “Indirect” approach is one of the more interesting here, I won’t call out anyone specifically here, but I will say that having looked device specification sheets from several different vendors, its strange when they have the exact same timing diagram, typo’s included…

So this leads to the same viral issues as GPL features. Device manufacturers don’t make their datasheets public because they contain copyright information from another party. This makes it harder to understand what is available, and how to work with what you already have. On net, the whole industry suffers for this. For consumer devices this is just another barrier to entry for small companies, and reason that starting a hardware company is a headache.

MIPI being closed is annoying, but for a dose of scary recognize that [government mandated fire safety standards are closed the same way.](https://www.nfpa.org/Codes-and-Standards)

Happy hacking.
---
title: "Developing the Hard(ware) way —  4"
date: 2020-04-25 12:00:00 +0000
---

*Originally published on [Medium](https://medium.com/@meawoppl/developing-the-hard-ware-way-4-6724f3ad9a00)*

### [Developing the Hard(ware) way — 4](https://medium.com/@meawoppl/developing-the-hard-ware-way-3-6315a66c6d2d?source=your_stories_page---------------------------)

[In the last section we talked about a standard way of switching between our normal **Real** hardware implementation and a **Fake.**](https://medium.com/@meawoppl/developing-the-hard-ware-way-3-6315a66c6d2d)Its realization in the typical production configuration would be as in the following:

Typical application operation

Having this switch in place additionally permits us to test upstream application logic in a clear way, without the requirement for attached hardware.

Use of hardware take to test/simulate application logic.

Now this alone is valuable on its own, as it allows us to simulate, time and test the application itself, which is a huge boon. The rub is that is does not ensure that the Real and Fake hardware modules provide the same contract. Getting to this is where testing comes in:

Unit testing the fake hardware

Writing unit tests for our fake hardware provides some value and stability. After doing so, we can be sure that the Fakes function as designed, which brings us closer to our goal, but we still aren’t really running the same code, so how can we be sure?

The last permutation of this interconnect is what I call “testing promotion”. In this stage, we attach our tests to the real devices and exercise them:

There are many way to accomplish this. Most test frameworks have the ability to mark specific sets of tests (typically used for test discovery). These can be adapted into running your unit tests against a particular configuration of hardware that you wish to test quite simply.

**Exercising this configuration cements in that the Real and Fake hardware provide the same contract of execution. Additionally, it provides a systematic set of expectations expressed in code, for how you expect your hardware to function, and can help you isolate aberrant behaviors.**

This structure gives you the ability to **quickly test whether hardware changes, firmware upgrades, configuration options, or repairs are meeting the needs of the application uses them.** Similarly, it ensures that changes to the software are reflective of the know and tested behaviors of the hardware without hampering the cadence of deployment and upstream system changes.

No approach can completely eliminate bugs. Remember, [hardware has SOUL](https://medium.com/@meawoppl/developing-the-hard-ware-way-1-73ef2b07fc3a), and if the simulation there of was perfect, we wouldn’t have the hardware in the first place. With that disclaimer, I will say that when a bug does arise in a system so tested this approach allows us to trifurcate the surface of any bug:.

* If it happens in unit testing, then the driver/device is being used by that application code in an erroneous state. The bug is upstream of the hardware.
* If the bug arises in hardware testing, using the tests that usually run against the Fakes in CI, then the contract/expectations we set out in the test are not being met. We are not using the device correctly.
* If the bug arises in anywhere else, then the contract/promises presented by the driver mock are fundamentally wrong, ie the component is exhibiting a behavior that is **disjoint** with respect to our stated expectations, and you have **learned something new** about your hardware's SOUL, and when you bring it into sync, **the next person won’t have to.**
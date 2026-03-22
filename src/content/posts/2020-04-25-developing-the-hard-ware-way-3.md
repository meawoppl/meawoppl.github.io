---
title: "Developing the Hard(ware) way — 3"
date: 2020-04-25 12:00:00 +0000
---

*Originally published on [Medium](https://medium.com/@meawoppl/developing-the-hard-ware-way-3-6315a66c6d2d)*

### Developing the Hard(ware) way — 3

In the [previous section](https://medium.com/@meawoppl/developing-the-hard-ware-way-2-2f328e2e2ec1) we lamented integration testing, and its drag on our progress. Lets talk about two types of testing fixtures that help us escape this, “Mocks” and “Fakes”. There are a number of [great articles](https://blog.pragmatists.com/test-doubles-fakes-mocks-and-stubs-1a7491dfa3da) out there [about the differences](http://xunitpatterns.com/Test%20Double.html), but many also many that use the terms interchangeably. In this article, we are going to talk about **Fakes**, which specifically should be thought of as the following:

> A Fake object mimics the functionality of the object it replaces, and implements it a much simpler way. It is not used as an observation or control point in testing.

Implementation of these Fakes is the first step in decoupling your development process from the demands of the underlying hardware. Lets start with an example transformation that has come up several times in my experience, the transportation of imaging data off of a sensor:

This pattern arises naturally during the first stage of hardware development, but as it grows, it becomes difficult to test the the internal components (Image processing/transmission logic), as well as the upstream and downstream portions that rely on it.

Transforming this to use our newly implemented Fake is a standard technique in the industry to test database models or external services. This category of change is generally referred to as [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection), DI for short. After that transformation, lets see how things look:

At this point we have actually made huge progress in our testing narrative. Using our **Fake Camera API**, we can test the logic inside the Camera Manager, and even use the Camera Manager with the injected Fake Camera API as a fixture for testing the larger application.

Now, I have glossed over an important aspect here, the box labeled **Loader** on the above diagram. It will come up several more times in the following article, so lets talk a bit about its design.

The **Loader** has two key responsibilities:

1. Provide several different implementations of a device that obey the same functional contract. In our example above, this could be one **or more** real cameras, as well as the fake camera we implemented earlier.
2. Provided an interface for the caller (whether application or test fixture) to specify whether a Real or Fake device is to be used.

The best way to meet these requirements is highly dependent on language features available to you

* In languages that provide “implements / interface” checking (Typescript/Java/go) this is a pretty easy, simply make sure your **Real/Fake** objects implement the interface, and type the loader as returning an object with that interface.
* In languages with strong OOP and [method overrides](https://en.wikipedia.org/wiki/Method_overriding) (C++, C#), this can be accomplished by building an abstract base class that both **Real/Fake** inherit from.
* In more “permissive” languages (I’m looking at you Python/Javascript), having both **Real/Fake** implementations inherit from an exception raising default class is a reasonable option. Another option is test time inspection of the inherited classes for call equivalence to the parent. These provide weaker, but still valuable guarantees, and help provide traceability in failure if nothing else.

Using this loader **in both application and testing** grants us a few key abilities that I want make explicit:

1. The ability to test the logic of the application that previously depended on the hardware interfaces in a CI.
2. The ability to **test the Fake hardware** as part of your normal CI process.

The first is obviously useful, as it lets us test the larger application, the second is a key part of extending our testing into the hardware itself, which [we will see in the final section of this series.](https://medium.com/@meawoppl/developing-the-hard-ware-way-4-6724f3ad9a00)
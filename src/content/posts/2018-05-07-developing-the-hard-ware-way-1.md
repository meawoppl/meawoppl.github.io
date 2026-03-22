---
title: "Developing the Hard(ware) Way — 1"
date: 2018-05-07 12:00:00 +0000
---

*Originally published on [Medium](https://medium.com/@meawoppl/developing-the-hard-ware-way-1-73ef2b07fc3a)*

First, let’s define what “hardware” means. When we talk about hardware in this series of articles, we are discussing physical devices that are not capable of being virtualized. **Any object in which the behavior that can be completely described by a piece of software is not really what we are aiming to discuss here.**

Here are some important facets that describe the systems and devices we discuss in this series. They have SOUL:

1. **State** — They admit non-trivial state that cannot be altered. Typically, some of that state is reflected in the physical arrangement of atoms or motion of electrons. That state might be permanent, such as a serial-number, or a transient in time, such as a measurement.
2. **Outside** — There is no virtual (pure software) system that can substitute for them; they fundamentally exist with side effects outside the box. In general, we never make a hardware device that could be implemented in code. They must exist outside that sphere.
3. **Utility** — There is direct reason to entertain this complex state, physical mass, and burden of reality. It offers something of value.
4. **Liability** — It matters if they break. Utility and liability are the yin and yang of a hardware device. Value in function begets inconvenience in failure.

Enough philosophy! Lets talk about a physical device that we are all familiar with: cameras.

The cameras we use at 3Scan are not wholly dissimilar from those in your cell phone or laptop. They have **state** and parameters that determine their function and they measure input from the **outside** world, a feature from which their clear **utility** derives. What makes 3Scan’s arrangement a little different is that our cameras must acquire gigapixels per second (think > 100 selfies/second), and the imaging technique is fundamentally destructive.

If you don’t capture an image of the slice as it is taken, that data will be gone forever.

![Microscope slice](/images/hardware-dev/microscope-slice.gif)

The **liability** that comes with camera malfunction is very high, as the sliced portion of the sample is gone. There are no second shots in our game.

3Scan has supported 2 SDKs across 3 different hardware architectures to support 7 unique camera models in the face of innumerable versions of the supporting drivers and vendor provided software. Our initial approach to integrating these devices went something like this:

1. Read the API documentation — Typically ~500 pages of docs across a mishmash of pdf/html/chm resources. Not exactly light reading, but we could skim for the relevant bits and generally use it as a reference.
2. Run/Understand/Execute Example Code —One of our SDK’s came with turnkey example code. This was lucky, most hardware devices come with less.
3. Take the example code and permute it toward the desired use case, eventually converging on some demonstrable interaction between the device and the software you have written.

This approach has a tangible appeal. It is understandable, insofar as it presents a seemingly monotonic march of progress toward a “working” integration with the device. The problems with this approach are numerous, and, unfortunately, highly non-obvious:

1. By implementing the integration to the device, you have converged a working configuration. The code you create however, contains little expression of what a working configuration **acts like.** There are almost always settings on the device and host operating system that are essential.
2. Confirmation of the above working condition requires the presence of the hardware device. This means that any logic that surrounds the device interface becomes very hard to test in the absence of the device itself.
3. Changes or updates in the supporting environment can introduce subtle breakage that is **not correlated application code changes**. The same API might have slightly different semantic following a driver update, or worse, may have a ABI level change without appropriate API level docs.
4. Swapping of the device for one with a different state may break the expectations of your code. Cameras often come with persistent storage that durably saves settings in the face of a power-cycle and software reset. **Which parts of this state are durable or can be assumed stable across devices is not obvious.**

**In short, its easy to make a piece of hardware work once. It is much harder to keep it working considering the special flavors of crazy that come with external state.**

[In the next segment, we will talk about the pitfalls associated with the most common approach taken to battle these issues: integration testing.](https://medium.com/@meawoppl/developing-the-hard-ware-way-2-2f328e2e2ec1)
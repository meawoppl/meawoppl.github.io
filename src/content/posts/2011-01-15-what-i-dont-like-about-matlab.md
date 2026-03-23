---
title: "What I don't Like About MATLAB"
date: 2011-01-15 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

This is a place that I list the various things I come across in MATLAB that annoy me:

Major (Systematic Problems):

1. Functions must be separate files. This is not fundamentally a bad thing, but it discourages the declaration of small functions which make code clearer.
2. Lack of development headers. Python lets you tear down what you don't like and do as you please. This is mostly a bad idea, but I would rather have the freedom to blow off my own leg than live without the high-power firearms associated with messing with the interpreter. See IPython for beautiful examples, and for some bad ones see the awful [GOTO/COMEFROM module](https://web.archive.org/web/20160318073715/http://entrian.com/goto/ "GOTO and COMEFROM.  Do not use.").
3. Lack of a linked list class in the default install. This is really glaring. There are a ton of problems that are conducive extensible lists of objects.
4. Lack of clean integration with other languages. This process is simply a disaster. Ever tried making anything in c-linked matlab work properly between platforms/compilers? Don't. This problem is distinctly linked to problem #2.

Minor Annoyances:

1. The lack of a true outer product. There is no way to (in one step) project together the dimensions of arbitrary arrays with matching inner dimensions. AKA The product of a n-dimensional array A with shape (ExFxGx1) and B ( H ) to get outer(A, B) with shape (ExFxGxH). For something with such a strong linear algebra focus, this is just really weak sauce.
2. One based indexing. Fortran used 1 based indexing. Need I say more?
3. MATLAB complains (warnings) when you allocate temporary values. This leads to really, really, ugly syntax which has to create temporaries anyway . . . the warnings might as well say something like "Warning:Readable code ahead!"

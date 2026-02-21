---
layout: post
title: "Software Licensing Is Dead"
date: 2026-02-21 12:00:00 -0800
---

Software licensing had a good run. From the GPL's viral copyleft to MIT's
permissive elegance, licenses were the legal scaffolding of the software
world. They defined who could use code, how, and under what terms.
Entire careers were built around open source compliance.

None of it matters anymore.

## The Authorship Problem

Licensing assumes a clear author. Someone writes code, they own it, they
choose terms. That model made sense when humans wrote software by hand,
line by line, with intent and craft.

Now? A developer types a comment describing what they want, and an AI
produces fifty lines of working code. Who authored that? The developer
who wrote the prompt? The AI company? The millions of programmers whose
code trained the model? The answer is legally murky at best and
philosophically incoherent at worst.

You can't license what you don't own. And increasingly, nobody owns
anything.

## The Laundering Machine

Every major AI code model was trained on vast quantities of open source
code. GPL code. MIT code. Proprietary code that leaked. All of it fed
into a giant statistical blender that outputs something *new*—or at
least new enough that no license attaches to it.

This is the most effective license laundering operation in history, and
it's running in plain sight. Code goes in with restrictions. Code comes
out without them. The copyleft zealots and the proprietary vendors are
equally powerless to stop it.

Try enforcing the GPL against a transformer's weight matrix. Good luck.

## The Convergence Problem

Here's the deeper issue: as AI gets better at generating code,
independent implementations converge. Ask ten developers to implement a
binary search and you'll get ten variations. Ask ten AI models and
you'll get nearly identical output.

When the "obvious" implementation is the only implementation, the idea
of licensing it becomes absurd. You can't copyright the only reasonable
way to do something. As AI narrows the solution space, more and more
code falls into this category.

## The Compliance Theater

Companies still employ armies of lawyers to audit open source
dependencies. They run license scanners. They maintain approved-license
lists. They reject perfectly good libraries because of license
incompatibilities.

Meanwhile, their developers are generating thousands of lines of
AI-assisted code daily with zero provenance tracking. The compliance
infrastructure is guarding the front door while the back wall is missing.

This isn't a criticism of those companies—it's a statement about
reality. The tooling and legal frameworks haven't caught up, and they
probably never will. The pace of AI-assisted development has outrun the
pace of legal adaptation.

## What Actually Matters Now

If licensing doesn't protect software anymore, what does?

**Speed.** Ship faster than anyone can copy you. By the time someone
replicates your features, you've moved on.

**Data.** Your models, your user data, your domain expertise—these
can't be prompted out of an AI. Network effects and data moats are the
new IP.

**Execution.** The gap between "code that works" and "product that
people pay for" has never been wider. Code is table stakes. Everything
around it is the actual value.

**Taste.** When anyone can generate code, the differentiator is knowing
*what* to build. Product intuition becomes the scarce resource, not
engineering capacity.

## The GPL Is a Museum Piece

I say this with respect for what the GPL accomplished. It was a
brilliant hack—using copyright law to enforce sharing. It changed the
world. Linux, GCC, and countless other projects exist because of it.

But the GPL's power derived from copyright, and copyright assumes human
authorship. When the majority of new code is AI-generated or
AI-assisted, the legal foundation crumbles. The FSF can publish GPL v4,
v5, v100—it won't matter if the courts can't determine who holds the
copyright in the first place.

## So What Now?

We're entering an era where code is abundant, cheap, and authorless.
The scarce resources are taste, data, and the ability to ship. Licensing
regimes built for a world of scarcity don't survive contact with a
world of abundance.

The lawyers will keep lawyering. The compliance tools will keep scanning.
But the developers have already moved on. They're generating, iterating,
and shipping at a pace that makes license auditing a quaint relic.

Software licensing is dead. It just doesn't know it yet.

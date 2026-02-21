---
layout: post
title: "Software Licensing Is Dead"
date: 2026-02-21 17:00:00 -0800
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
out without them. The people who wrote that code—often brilliant, generous people who
shared their work to help others—are powerless to stop it.

Try enforcing the GPL against a transformer's weight matrix. The legal
tooling simply doesn't exist. And the GPL's power always derived from
copyright—the brilliant hack of using copyright law to enforce sharing.
But copyright assumes human authorship. When the majority of new code is
AI-generated or AI-assisted, that legal foundation crumbles. The FSF can
publish GPL v4, v5, v100—it won't matter if the courts can't determine
who holds the copyright in the first place.

And the courts are starting to agree. In mid-2025, two federal judges
in the Northern District of California ruled that training AI models on
copyrighted works constitutes
[transformative fair use](https://www.crowell.com/en/insights/client-alerts/ai-companies-prevail-in-path-breaking-decisions-on-fair-use).
One judge called it "spectacularly" transformative—the model doesn't
copy expression, it extracts statistical patterns to generate something
new. The U.S. Copyright Office's own
[guidance](https://www.wiley.law/alert-Copyright-Office-Issues-Key-Guidance-on-Fair-Use-in-Generative-AI-Training)
concluded that training on large, diverse datasets "will often be
transformative."

Meanwhile, the AI companies aren't waiting for the legal dust to settle.
They're putting their money where their models are. Microsoft's Copilot
Copyright Commitment promises to defend paying customers against
copyright claims from generated output. OpenAI's Copyright Shield does
the same for ChatGPT Enterprise and API users. Google and Anthropic
offer similar indemnification for their enterprise customers. These
companies are betting—with real legal liability—that the outputs of
their models are clean.

So the code goes in with licenses attached, comes out with corporate
indemnification attached instead, and the courts are calling the
transformation fair use. The old licensing regime isn't just
unenforceable in practice. It's being actively dismantled by case law
and corporate policy.

## The Convergence Problem

Here's the deeper issue: as AI gets better at generating code,
independent implementations converge. Ask ten developers to implement a
binary search and you'll get ten variations. Ask ten AI models and
you'll get nearly identical output.

When the "obvious" implementation is the only implementation, the idea
of licensing it becomes absurd. You can't copyright the only reasonable
way to do something. As AI narrows the solution space, more and more
code falls into this category.

I've seen this firsthand.

## Three Reimplementations

I've implemented a blind astrometry plate solver—the kind of software
that looks at an image of the night sky and figures out where the camera
was pointing, using nothing but the pattern of stars—three times now.

The first time, I wrote it by hand in Java for a closed-source project.
It took me a month. The second time, in Python, also closed-source.
Two weeks. Both times I was working from Dustin Lang's excellent
[thesis](https://arxiv.org/abs/0910.2233) and studying the
[astrometry.net](https://astrometry.net) reference implementation—a
genuinely impressive piece of software that I credit as the inspiration
for all three of my implementations. Same algorithm, same geometric
hashing, same kd-tree lookups, same Bayesian verification.

The third time, I built
[zodiacal](https://github.com/OrbitalCommons/zodiacal) in Rust. I
was drunk on a boat in the British Virgin Islands. I handed an AI the
reference thesis, Lang's implementation to study, a
[star catalog library](https://github.com/OrbitalCommons/starfield),
and 1,000 images with known correct answers. It did the rest. The
result solves 98.5% of test fields in about a second.

Three implementations. Same algorithm. Zero shared lines of code
between any of them. Zodiacal cites astrometry.net and Lang's paper
prominently—credit where it's due. But credit and licensing are
different things.

So what license governs zodiacal? Not astrometry.net's—I never copied
their code. Not whatever license covered my previous Java and Python
versions—those were clean-room rewrites too. Not the AI model's
training data—good luck tracing which weights contributed to which
function. The algorithms are published science, uncopyrightable by
design. And the latest implementation was generated by a machine while
I was sipping rum in the Caribbean.

Zodiacal's foundation library,
[starfield](https://github.com/OrbitalCommons/starfield), has a
similar origin story. It's a Rust port of Brandon Rhodes'
[Skyfield](https://rhodesmill.org/skyfield/)—a beautifully designed
Python library for positional astronomy. Coordinate transforms,
precession, nutation, star catalog management, the whole stack. Ported
in a couple of weeks. The testing strategy was beautifully simple: a
Python bridge that runs both libraries side by side and checks them
for agreement. Feed the same inputs to Skyfield and starfield, compare
outputs, iterate until they match.

The result is a library that produces identical results to Skyfield,
cites it as the direct inspiration, shares zero code with it, and was
largely written by a machine using the original as a behavioral
specification. Skyfield is MIT-licensed. Starfield is MIT-licensed.
But the choice of license is almost incidental—the code was derived
from behavior, not from source. No license can prevent someone from
reimplementing your observable outputs.

Then there's [pastebom.com](https://pastebom.com). I wanted a hosted
service for sharing interactive PCB bill-of-materials viewers. The
existing tool,
[InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom),
is a great project—I use it all the time and credit it as the direct
inspiration for pastebom. I
[contributed upstream](https://github.com/openscopeproject/InteractiveHtmlBom/pull/532)
to make it work headless, offered to port the format extractors to
Rust—the maintainer had different priorities, which is totally
reasonable. Their project, their call.

So I extracted the drastic subset I actually needed and added support
for more formats from Altium. I validate the extraction utilities against
a library of closed-source design files from my own projects—the same
pattern as zodiacal and starfield. Give an AI the file format spec,
a pile of real-world files with known correct outputs, and let it
iterate. I cite InteractiveHtmlBom on the site because it deserves the
credit. But the point stands: the formats are documented, the behavior
is observable, and an AI can reimplement a PCB file parser in an
afternoon if you point it at the spec. Attribution and gratitude are
the right thing to do. But a license couldn't have stopped any of this,
and it couldn't have compelled it either.

## The Real Currency: Ground Truth

Notice what all three projects have in common. Zodiacal had 1,000 images
with known correct sky coordinates. Starfield had a Python bridge
producing reference outputs from Skyfield. Pastebom had a library of
real PCB design files with known correct extractions. In every case,
the thing that made AI-driven reimplementation possible wasn't access
to the source code—it was access to **ground truth**.

Ground truth is the new source code.

An AI can't write a blind astrometry solver from a vague description.
But give it a spec and a thousand images where you already know the
answer? It'll converge on a working implementation. The same is true
for coordinate transforms, file format parsers, and practically
anything else where you can say "given this input, the correct output
is that."

This inverts the traditional value hierarchy. We used to think source
code was the valuable artifact and correctness was a supporting concern.
Now the code is the disposable part—regenerable on demand—and the
curated collection of known correct answers is the irreplaceable asset.
Ground truth is the specification, the oracle, and the training signal
all at once. Collecting it requires domain expertise, real-world data,
and the hard-won judgment to know what "correct" actually looks like.

If licensing doesn't protect software anymore, what does? Ground truth.
Domain expertise. Taste—knowing *what* to build when anyone can
generate the code. Speed—shipping before anyone can replicate you.
These are the new moats, and none of them are things a license file
can provide.

## So What Now?

We're entering an era where code is abundant, cheap, and authorless.
Licensing regimes built for a world of scarcity don't survive contact
with a world of abundance.

I still choose licenses for my projects. I still cite the people whose
work inspired mine. But I do these things out of respect and convention,
not because I believe they offer meaningful legal protection. The
cultural norms of open source—attribution, gratitude, building on each
other's work—are worth preserving. The legal fiction that a LICENSE file
controls what happens to your code is not.

Software licensing is dead. Long live ground truth.

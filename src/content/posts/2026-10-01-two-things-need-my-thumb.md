---
title: "Two Things Need My Thumb"
date: 2026-10-01 12:00:00 +0000
---

Agents write most of my code now. That part is boring.

The interesting question is the other one. What do you let them do to production?

My answer: everything reversible, nothing that mints a credential or widens the surface. Two things need a human. Everything else runs unattended.

## Secrets are not in git, and not on the host either

Committed env and compose files contain placeholders. Not encrypted secrets, not sealed blobs. Just a URI that names where a secret lives. That is safe to commit, because it is not a secret. It is a pointer.

At deploy time those pointers get resolved on my workstation, by a CLI that makes my device prove I am me. There is no service account. There is no master key sitting on a server waiting to be found.

What comes out is a concrete env file. It exists briefly on my machine, gets copied to the host owner-only at 0600, and gets handed to the container runtime. The host never sees the pointers and cannot re-derive anything. Walk off with the box and you get the resolved values for that one service, with no way to ask for more.

A nice property falls out for free. Resolution needs a live human-authenticated session, and sessions lapse. I know they lapse because mine does, constantly, which is mildly annoying and exactly correct. An unattended agent cannot mint secrets at 3am, because at 3am nobody has unlocked anything.

## The gate is on secret material, not on code

This is the part I think people get wrong.

Gate "deploys" and you gate everything, and now you are the bottleneck on a typo fix. Gate nothing and an agent can quietly hand your database password to a brand new container.

So the gate sits at secret resolution, and nowhere else. An agent can do all of it: edit the template, write the placeholder, stage the change, verify it, run every read-only check it likes. It produces a complete, reviewable deploy. The one thing it cannot produce is the file with real credentials in it.

Deploys split cleanly:

- Code or image changed, secrets unchanged. Ships on its own.
- An env value changed. Needs my thumb.

Most days nothing needs my thumb.

## Every change writes itself down

One human-readable changelog lives in the ops repo and records anything that touched a host. Deploys, config edits, manual pokes, incidents. Each entry is dated and says what changed, why, and how it was verified.

The rule that makes it work: the agent making the change appends the entry in the same step. Not afterward. Not batched up on Friday. Same step.

No tooling enforces this. It is a standing instruction, and it holds because the instruction is specific about *when*, not just *that*. "Keep a changelog" gets ignored. "Append the entry in the same step as the change" does not.

That log ends up being the only cross-cutting record of what actually reached production. Individual repos have their commit history. The ops log has the story.

## Something checks on all of it every six hours

Two layers watch the infrastructure.

A lightweight timer runs health checks on a short interval, doing threshold math. Dumb, fast, cheap.

On top of that, a scheduled Agent Portal agent sweeps every six hours and actually reasons about what it finds. It can escalate to my phone by SMS.

What it checks is the useful part. Not "is the container up," because containers lie. It checks failure classes:

- Is each public endpoint actually serving, as opposed to the container cheerfully reporting itself healthy. Those two diverge, and that divergence is the entire reason this exists.
- Did a destructive action execute and then sit there waiting for a human review that never came. That one is a tripwire.
- Is any work queue aging past its bound.
- Did a service quietly fall out of the auto-update set.
- Are the background pipelines still moving.

Any threshold crossing counts as weird, and weird goes to my phone. Deliberately my phone, not a team chat, because a team chat is where alerts go to die.

Each alert carries its own re-baseline instructions. When the weird thing turns out to be a legitimate change, I clear it, instead of getting nagged until I start ignoring the channel. An alert you learn to dismiss is worse than no alert.

## What runs without me

Free: read-only diagnosis across hosts and databases, staging config edits and verifying them, code deploys that do not touch secrets, docs, changelog, routine post-deploy verification. Risky migrations too, but only through a specific dance. Rehearse against an isolated throwaway copy of the data, back up, apply behind a crash-loop guard, roll back instantly if it sulks.

Needs me: resolving or changing a secret. Standing up a new public surface, a new public name, or its certificate. DNS. Irreversible operations on production data. Credential rotation.

And one social rule that turned out to matter more than I expected. When one agent relays "the user approved this," that is good enough for routine in-app work. It is not good enough for a new public surface or a destructive data change. Those get confirmed with me directly. Agents are agreeable, and a chain of agreeable intermediaries will happily converge on something I never said.

## The shape of it

The blast radius of an autonomous agent here is "reversible and rehearsable." A human device unlock sits on exactly two things: minting secrets, and widening what is public or destroying what is not.

Everything else, they can have. It turns out that is most of the work.

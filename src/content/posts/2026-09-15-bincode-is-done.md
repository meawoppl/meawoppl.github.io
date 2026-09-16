---
title: "Bincode Is Done"
date: 2026-09-15 12:00:00 +0000
---

Our security audit went red this week. Not because of bincode.

The actual failure was a real vulnerability in `rustls` (RUSTSEC-2026-0285), cleared with a lockfile bump. But while we were in there, reading the part of the `cargo audit` output everybody scrolls past, one of the six "allowed warnings" was this:

```
Crate:     bincode
Version:   1.3.3
Warning:   unmaintained
Title:     Bincode is unmaintained
Date:      2025-12-16
ID:        RUSTSEC-2025-0141
```

Bincode. The binary serializer with **318 million downloads** and 5,785 crates depending on it. Unmaintained. It had been sitting in our warnings list and nobody had looked.

## How It Got In

We don't use bincode. We use `cdshealpix`, the HEALPix sky-indexing crate from CDS Strasbourg, and it uses bincode in exactly one place: an external merge sort that spills chunks to disk. It's a non-optional dependency. We call two functions, `nested::hash` and `cone_coverage_approx_flat`. Neither one goes anywhere near the sort.

And the crate that pulls in `cdshealpix`? `starfield-gaia`. Which I wrote. Great job, me.

So: code we never execute, in a crate we barely use, pulled in by a crate I maintain. Turns out that's what most of a dependency tree is.

## What Happened

In August 2025 bincode left GitHub for sourcehut, in protest of GitHub's generative AI push. On the way out the git history was rewritten, and the GitHub copy was flattened to a single "Goodbye Github" commit, pushed by an account that didn't exist until six days later.

That looks a lot like a hostile takeover. Four months later somebody on r/rust noticed and asked, reasonably, whether it was a supply chain attack. Some of the replies were not reasonable. Per the maintainer, real names, family members, and home addresses got posted. The mods confirmed privately that it wasn't an attack, scrubbed the doxxing, and removed the thread. The next morning the maintainers ended the project permanently.

Then they shipped the best deprecation notice I have ever seen. Bincode 3.0.0 is a README and a `lib.rs` containing exactly one line:

```rust
compile_error!("https://xkcd.com/2347/");
```

crates.io has no way to mark a crate archived. So they published a version that refuses to compile and links you to the dependency comic. Perfect.

## Timeline

| Date (UTC) | What happened |
|---|---|
| 2021-04-10 | bincode 1.3.3 published. The last 1.x release. |
| 2025-03-06 | bincode 2.0.0 ships, after more than three years of alphas, betas, and release candidates. |
| 2025-08-15 | GitHub repo archived. History replaced by one "Goodbye Github" commit, README citing GitHub's generative AI. Development moves to sourcehut. |
| 2025-08-21 | The `stygianentity` GitHub account that pushed that commit is created. |
| 2025-12-15 02:27 | "What's going on with bincode?" posted to r/rust. Cross-posted to the Rust forum seven minutes later. |
| 2025-12-15 08:31 | r/rust mods confirm there's no supply chain attack, remove doxxing comments, and remove and lock the thread. |
| 2025-12-16 10:53 | "Bincode development has ceased permanently," citing doxxing and harassment. |
| 2025-12-16 19:31 | RustSec issue filed. The maintainer agrees an advisory makes sense. |
| 2025-12-16 21:34 | bincode 3.0.0 published: a README and a `compile_error!`. |
| 2025-12-17 | `virtue` and `unty`, bincode 2's own dependencies, archived by a former developer. |
| 2026-01-07 | RUSTSEC-2025-0141 merged, dated 2025-12-16, flagged as an unmaintained notice rather than a vulnerability. |
| 2026-09-14 | Our audit fails on `rustls`. Bincode is sitting in the warnings. |
| 2026-09-15 | We decide to keep it. |

## What We Did

Nothing, on purpose. With a reason attached:

```toml
[advisories]
ignore = [
    # bincode 1.3 via cdshealpix's HEALPix sort module (starfield-gaia).
    # Works, unmaintained notice only; decision 2026-09-15 to keep it.
    "RUSTSEC-2025-0141",
]
```

Unmaintained is not vulnerable. 1.3.3 hasn't changed since 2021, the maintainers consider it complete, and the code path in question never runs for us. The alternatives were feature-gating that sort module upstream or writing our own HEALPix nested hash. Both are more code than the risk. We revisit if a real advisory ever lands against it.

## The Uncomfortable Part

The maintainer left a line in the second thread that I keep coming back to: *"Your 'supply chain' is not the git repo. Your 'supply chain' is crates.io."*

They're right. Nothing guarantees a published crate matches its repo. A rewritten git history is weird, but it isn't where your risk lives. The tarball is.

Bincode still pulled **61 million downloads in the last 90 days**. Most of those are people like us: a few crates removed, never calling it, never reading the warnings. That's not a bincode problem. That's everybody's.

Go read your `cargo audit` warnings. The allowed ones.

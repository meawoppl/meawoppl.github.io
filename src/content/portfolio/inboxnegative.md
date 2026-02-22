---
date: 2024-08-28
name: InboxNegative
thumb: /images/inboxnegative/logo.svg
---

<img src="/images/inboxnegative/logo.svg" alt="InboxNegative logo" style="width: 128px; height: 128px; margin: 0 auto 1rem;">

[InboxNegative](https://inboxnegative.com) is a disposable email service built around data transience. Emails exist only while you're actively viewing them — close the tab and they're gone.

The core idea is simple: you get a randomized email address, and incoming messages stream to your browser in real-time via Server-Sent Events. There's no inbox to clean out, no data sitting on a server, and no archive to worry about. Attachments get a 5-minute TTL before cleanup.

It was also my first Rust project. The whole stack is Rust end-to-end:

* **Backend** — A custom SMTP server and HTTP API built on Hyper and Tokio. Incoming mail gets parsed, held in memory, and published over ZeroMQ to connected clients.
* **Frontend** — A Yew/WASM app compiled with Trunk. The UI connects via EventSource to receive emails as they arrive.

HTML content gets sanitized with ammonia to strip scripts and iframes while keeping formatting intact.

It's a fun project that sits at the intersection of systems programming, real-time web, and privacy engineering.

---
date: 2026-01-08
name: Claude Code Portal
thumb: /images/cc-proxy/logo.svg
---

[Claude Code Portal](https://github.com/meawoppl/cc-proxy) is a web-based proxy that extends Claude Code with remote access and session sharing. Run Claude Code on a powerful machine and access it from any browser — phone, tablet, or thin client.

The system intercepts Claude's terminal I/O via a lightweight CLI wrapper (`claude-portal`), forwards everything over WebSocket to a central server, and renders it in a browser-based terminal UI. Multiple clients can view the same session in real-time.

The whole stack is Rust:

* **Backend** — Axum 0.7 with Diesel/PostgreSQL for session persistence, WebSocket endpoints for real-time sync, and Google OAuth for authentication.
* **Frontend** — A Yew/WASM app with a terminal-style interface, voice input via browser speech recognition, and live cost tracking.
* **Proxy CLI** — A native binary that wraps Claude Code, transparently capturing stdin/stdout and relaying to the backend.
* **Shared** — A WASM-safe crate of protocol types shared between frontend and backend, eliminating serialization boilerplate.

Features include configurable message retention, session sharing with role-based permissions, device-flow OAuth for CLI auth, and background cost tracking that broadcasts token usage to connected clients.

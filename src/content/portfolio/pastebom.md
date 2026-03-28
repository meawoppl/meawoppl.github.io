---
date: 2026-01-03
name: PasteBom
thumb: /images/pastebom/logo.svg
---

[PasteBom](https://pastebom.com) is a shareable interactive PCB Bill of Materials viewer. Upload a board file and get a link to an interactive viewer with a searchable BOM table. Supports seven EDA formats: KiCad, EasyEDA, Eagle, Altium, GDSII, Gerber, and ODB++.

![PasteBom PCB viewer](/images/pastebom/pcb-viewer.png)

The viewer renders front and back board views on stacked HTML5 canvases with click-to-highlight for nets and components, per-layer visibility toggles, pan/zoom/rotate, and dark mode. Uploads can be marked secret or left public on a shared feed. Each paste gets an SVG thumbnail for embedding.

The whole stack is Rust:

* **pcb-extract** — A parser library that reads `.kicad_pcb`, EasyEDA JSON, Eagle XML, Altium `.pcbdoc`, GDSII, Gerber, and ODB++ files into a common intermediate representation.
* **pastebom-server** — An Axum/Tokio HTTP server handling multipart uploads, S3-backed storage, and serving the viewer.
* **pastebom-viewer** — A Yew/WASM frontend compiled with Trunk, rendering interactive board views on canvas with path caching for performance.

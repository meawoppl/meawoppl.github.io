---
date: 2026-01-03
name: PasteBom
thumb: /images/pastebom/logo.svg
---

[PasteBom](https://pastebom.com) is a shareable interactive PCB Bill of Materials viewer. Upload a board file from KiCad, EasyEDA, Eagle, or Altium and get a link to an interactive viewer with a searchable BOM table.

![PasteBom PCB viewer](/images/pastebom/pcb-viewer.png)

The viewer renders front and back board views on stacked HTML5 canvases with click-to-highlight for nets and components, layer visibility toggles, pan/zoom/rotate, and dark mode.

The whole stack is Rust:

* **pcb-extract** — A parser library that reads `.kicad_pcb`, EasyEDA JSON, Eagle XML, and Altium `.pcbdoc` files into a common intermediate representation.
* **pastebom-server** — An Axum/Tokio HTTP server handling multipart uploads, S3-backed storage, and serving the viewer.
* **pastebom-viewer** — A Yew/WASM frontend compiled with Trunk, rendering interactive board views on canvas with path caching for performance.

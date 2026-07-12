const DATA_BASE = "data/";
const DOCS_BASE = "docs/";

let allItems = [];
let docsIndex = {};
let currentFilter = "all";
let themeFilter = null;

function slugify(title) {
  return title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

function hashStr(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
  }
  return Math.abs(hash);
}

function themeColor(name) {
  const h = hashStr(name) % 360;
  return `hsl(${h}, 55%, 45%)`;
}

function esc(str) {
  const d = document.createElement("div");
  d.textContent = String(str);
  return d.innerHTML;
}

const URL_RE = /(https?:\/\/[^\s"<>)]+)/g;

// Escape text, then turn any bare URLs into clickable, new-tab links.
function linkify(str) {
  return String(str)
    .split(URL_RE)
    .map((part, i) =>
      i % 2 === 1
        ? `<a href="${esc(part)}" target="_blank" rel="noopener">${esc(part)}</a>`
        : esc(part)
    )
    .join("");
}

async function loadData() {
  try {
    const [ideasResp, indexResp] = await Promise.all([
      fetch(DATA_BASE + "ideas.json"),
      fetch(DOCS_BASE + "index.json").catch(() => null),
    ]);
    allItems = ideasResp.ok ? await ideasResp.json() : [];
    docsIndex = indexResp && indexResp.ok ? await indexResp.json() : {};
  } catch {
    allItems = [];
  }
  renderThemeBar();
  render();
}

function hasDoc(item) {
  return Object.prototype.hasOwnProperty.call(docsIndex, slugify(item.title));
}

function filteredItems() {
  let items = allItems;
  if (currentFilter === "burning_man") {
    items = items.filter((i) => i.burning_man === true);
  } else if (currentFilter === "business") {
    items = items.filter((i) => i.business === "yes" || i.business === "maybe");
  }
  if (themeFilter) {
    items = items.filter((i) => (i.themes || []).includes(themeFilter));
  }
  return items;
}

function renderThemeBar() {
  const counts = {};
  for (const item of allItems) {
    for (const t of item.themes || []) counts[t] = (counts[t] || 0) + 1;
  }
  const themes = Object.keys(counts).sort((a, b) => counts[b] - counts[a] || a.localeCompare(b));
  const bar = document.getElementById("theme-bar");
  bar.innerHTML =
    `<button class="theme-chip${themeFilter === null ? " active" : ""}" data-theme="">All themes</button>` +
    themes
      .map((t) => {
        const bg = themeColor(t);
        const active = themeFilter === t ? " active" : "";
        return `<button class="theme-chip${active}" data-theme="${esc(t)}" style="--chip:${bg}">${esc(t)} <span class="chip-count">${counts[t]}</span></button>`;
      })
      .join("");
  bar.querySelectorAll(".theme-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      themeFilter = chip.dataset.theme || null;
      renderThemeBar();
      render();
    });
  });
}

function badge(label, cls) {
  return `<span class="badge ${cls}">${esc(label)}</span>`;
}

function render() {
  const content = document.getElementById("content");
  const items = filteredItems().slice().sort((a, b) =>
    a.title.localeCompare(b.title, undefined, { sensitivity: "base" })
  );

  if (items.length === 0) {
    content.innerHTML = "<p>No ideas found.</p>";
    return;
  }

  let html = `<p class="count">${items.length} idea${items.length === 1 ? "" : "s"}</p><div class="cards">`;
  for (const item of items) {
    const badges = [];
    if (item.burning_man === true) badges.push(badge("Burning Man", "bm"));
    if (item.business === "yes") badges.push(badge("Business", "biz"));
    else if (item.business === "maybe") badges.push(badge("Business?", "biz-maybe"));

    const themes = (item.themes || [])
      .map((t) => `<span class="theme-chip small" style="--chip:${themeColor(t)}">${esc(t)}</span>`)
      .join("");

    const meta = [];
    if (item.status) meta.push(`<span class="meta-status">${esc(item.status)}</span>`);
    if (item.doc) meta.push(`<span class="meta-doc">doc: ${esc(item.doc)}</span>`);
    if (item.first_step) meta.push(`<span class="meta-step">first step: ${esc(item.first_step)}</span>`);

    const detail = hasDoc(item);
    const slug = slugify(item.title);

    html += `<article class="card${detail ? " has-detail" : ""}"${detail ? ` data-slug="${esc(slug)}" tabindex="0" role="button"` : ""}>
      <div class="card-head">
        <h2>${esc(item.title)}</h2>
        <div class="badges">${badges.join("")}</div>
      </div>
      ${item.summary ? `<p class="summary">${linkify(item.summary)}</p>` : ""}
      ${themes ? `<div class="themes">${themes}</div>` : ""}
      ${meta.length ? `<div class="meta">${meta.join("")}</div>` : ""}
      ${detail ? `<div class="read-more">Open write-up &rarr;</div>` : ""}
    </article>`;
  }
  html += "</div>";
  content.innerHTML = html;

  content.querySelectorAll(".card.has-detail").forEach((card) => {
    const open = () => openDoc(card.dataset.slug);
    card.addEventListener("click", open);
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });
  });
}

function renderBlocks(blocks) {
  return (blocks || [])
    .map((b) => {
      if (b.type === "list") {
        return `<ul class="doc-list">${b.items
          .map(
            (it) =>
              `<li class="lvl-${it.level || 0}"><span class="marker">${esc(it.marker || "•")}</span> ${linkify(it.text)}</li>`
          )
          .join("")}</ul>`;
      }
      return `<p>${linkify(b.text || "")}</p>`;
    })
    .join("");
}

async function openDoc(slug) {
  const overlay = document.getElementById("modal");
  const body = document.getElementById("modal-body");
  body.innerHTML = "<p>Loading…</p>";
  overlay.classList.add("open");
  document.body.style.overflow = "hidden";

  let manifest;
  try {
    const resp = await fetch(`${DOCS_BASE}${slug}.json`);
    manifest = await resp.json();
  } catch {
    body.innerHTML = "<p>Could not load this write-up.</p>";
    return;
  }

  const images = (manifest.images || [])
    .map(
      (name) =>
        `<a href="${DOCS_BASE}${slug}/${esc(name)}" target="_blank" rel="noopener" class="doc-img">
           <img loading="lazy" src="${DOCS_BASE}${slug}/${esc(name)}" alt="">
         </a>`
    )
    .join("");

  body.innerHTML = `
    <h2 class="modal-title">${esc(manifest.title || slug)}</h2>
    <div class="doc-text">${renderBlocks(manifest.blocks)}</div>
    ${images ? `<div class="doc-gallery">${images}</div>` : ""}`;
  body.scrollTop = 0;
}

function closeDoc() {
  document.getElementById("modal").classList.remove("open");
  document.body.style.overflow = "";
}

document.querySelectorAll(".filter[data-filter]").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter[data-filter]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    render();
  });
});

document.getElementById("modal").addEventListener("click", (e) => {
  if (e.target.id === "modal" || e.target.classList.contains("modal-close")) closeDoc();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeDoc();
});

loadData();

const DATA_BASE = "data/";
const DOCS_BASE = "docs/";

let allItems = [];
let docsIndex = {};
let currentFilter = "all";
let themeFilter = null;
let openSlug = null;
let targetSlug = null;

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

const VALID_FILTERS = ["all", "burning_man", "business"];
const BASE_TITLE = document.title;

// State lives in the hash so every view is a link you can paste somewhere.
function stateToHash() {
  const params = new URLSearchParams();
  if (currentFilter !== "all") params.set("filter", currentFilter);
  if (themeFilter) params.set("theme", themeFilter);
  if (openSlug) params.set("idea", openSlug);
  const q = params.toString();
  return q ? "#" + q : "";
}

let lastAppliedHash = null;

function syncURL(push) {
  const url = location.pathname + location.search + stateToHash();
  if (push) history.pushState(null, "", url);
  else history.replaceState(null, "", url);
  lastAppliedHash = location.hash;
}

// The pre-rendered page is what unfurls in Slack/iMessage/etc, so share that
// rather than the hash link. Both resolve to the same idea.
const APP_BASE = location.pathname.replace(/[^/]*$/, "");

function permalink(slug) {
  return location.origin + APP_BASE + "i/" + encodeURIComponent(slug) + "/";
}

function itemBySlug(slug) {
  return slug ? allItems.find((i) => slugify(i.title) === slug) : null;
}

function applyURL() {
  // popstate and hashchange can both fire for one navigation
  if (location.hash === lastAppliedHash) return;
  lastAppliedHash = location.hash;

  const params = new URLSearchParams(location.hash.slice(1));
  const f = params.get("filter");
  currentFilter = VALID_FILTERS.includes(f) ? f : "all";
  themeFilter = params.get("theme") || null;

  const item = itemBySlug(params.get("idea"));
  // A shared link has to resolve, so drop filters that would hide its target.
  if (item && !filteredItems().includes(item)) {
    currentFilter = "all";
    themeFilter = null;
  }

  targetSlug = item ? slugify(item.title) : null;
  openSlug = item && hasDoc(item) ? targetSlug : null;

  syncFilterButtons();
  renderThemeBar();
  render();

  if (openSlug) showModal(openSlug);
  else hideModal();
}

function syncFilterButtons() {
  document.querySelectorAll(".filter[data-filter]").forEach((b) => {
    b.classList.toggle("active", b.dataset.filter === currentFilter);
  });
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
  applyURL();
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
      syncURL(false);
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

    html += `<article class="card${detail ? " has-detail" : ""}" id="idea-${esc(slug)}" data-slug="${esc(slug)}"${detail ? ` tabindex="0" role="button"` : ""}>
      <div class="card-head">
        <h2>${esc(item.title)}</h2>
        <div class="badges">${badges.join("")}</div>
      </div>
      ${item.summary ? `<p class="summary">${linkify(item.summary)}</p>` : ""}
      ${themes ? `<div class="themes">${themes}</div>` : ""}
      ${meta.length ? `<div class="meta">${meta.join("")}</div>` : ""}
      <div class="card-foot">
        ${detail ? `<span class="read-more">Open write-up &rarr;</span>` : "<span></span>"}
        <button class="permalink" type="button" data-slug="${esc(slug)}" aria-label="Copy link to ${esc(item.title)}">Copy link</button>
      </div>
    </article>`;
  }
  html += "</div>";
  content.innerHTML = html;

  content.querySelectorAll(".card.has-detail").forEach((card) => {
    const open = () => openIdea(card.dataset.slug);
    card.addEventListener("click", (e) => {
      if (e.target.closest(".permalink")) return;
      open();
    });
    card.addEventListener("keydown", (e) => {
      if (e.target.closest(".permalink")) return;
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });
  });

  content.querySelectorAll(".permalink").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      copyLink(permalink(btn.dataset.slug), btn);
    });
  });

  if (targetSlug) highlightCard(targetSlug);
}

function highlightCard(slug) {
  const card = document.getElementById("idea-" + slug);
  if (!card) return;
  card.classList.add("targeted");
  if (!openSlug) card.scrollIntoView({ behavior: "smooth", block: "center" });
  setTimeout(() => card.classList.remove("targeted"), 2500);
}

async function copyLink(url, btn) {
  const done = (ok) => {
    const prev = btn.textContent;
    btn.textContent = ok ? "Copied!" : url;
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = prev;
      btn.classList.remove("copied");
    }, 1600);
  };
  try {
    await navigator.clipboard.writeText(url);
    done(true);
  } catch {
    // clipboard API needs a secure context; fall back to a selectable field
    const ta = document.createElement("textarea");
    ta.value = url;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try {
      ok = document.execCommand("copy");
    } catch {
      ok = false;
    }
    document.body.removeChild(ta);
    done(ok);
  }
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

// Navigation: pushes history so back/forward closes and reopens a write-up.
function openIdea(slug) {
  openSlug = slug;
  targetSlug = slug;
  syncURL(true);
  showModal(slug);
}

async function showModal(slug) {
  const overlay = document.getElementById("modal");
  const body = document.getElementById("modal-body");
  body.innerHTML = "<p>Loading…</p>";
  overlay.classList.add("open");
  overlay.setAttribute("aria-hidden", "false");
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

  const title = manifest.title || slug;
  document.title = `${title} — ${BASE_TITLE}`;

  body.innerHTML = `
    <h2 class="modal-title">${esc(title)}</h2>
    <button class="permalink modal-permalink" type="button" data-slug="${esc(slug)}" aria-label="Copy link to ${esc(title)}">Copy link</button>
    <div class="doc-text">${renderBlocks(manifest.blocks)}</div>
    ${images ? `<div class="doc-gallery">${images}</div>` : ""}`;
  body.scrollTop = 0;

  const btn = body.querySelector(".modal-permalink");
  btn.addEventListener("click", () => copyLink(permalink(slug), btn));
}

function hideModal() {
  const overlay = document.getElementById("modal");
  overlay.classList.remove("open");
  overlay.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
  document.title = BASE_TITLE;
}

function closeDoc() {
  if (!openSlug) return;
  hideModal();
  openSlug = null;
  syncURL(true);
}

document.querySelectorAll(".filter[data-filter]").forEach((btn) => {
  btn.addEventListener("click", () => {
    currentFilter = btn.dataset.filter;
    syncFilterButtons();
    render();
    syncURL(false);
  });
});

// Back/forward, and hand-edited or pasted URLs.
window.addEventListener("popstate", applyURL);
window.addEventListener("hashchange", applyURL);

document.getElementById("modal").addEventListener("click", (e) => {
  if (e.target.id === "modal" || e.target.classList.contains("modal-close")) closeDoc();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeDoc();
});

loadData();

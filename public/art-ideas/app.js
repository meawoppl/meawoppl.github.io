const DATA_BASE = "data/";

let allItems = [];
let currentFilter = "all";
let themeFilter = null;

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
    const resp = await fetch(DATA_BASE + "ideas.json");
    allItems = resp.ok ? await resp.json() : [];
  } catch {
    allItems = [];
  }
  renderThemeBar();
  render();
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

    html += `<article class="card">
      <div class="card-head">
        <h2>${esc(item.title)}</h2>
        <div class="badges">${badges.join("")}</div>
      </div>
      ${item.summary ? `<p class="summary">${linkify(item.summary)}</p>` : ""}
      ${themes ? `<div class="themes">${themes}</div>` : ""}
      ${meta.length ? `<div class="meta">${meta.join("")}</div>` : ""}
    </article>`;
  }
  html += "</div>";
  content.innerHTML = html;
}

document.querySelectorAll(".filter[data-filter]").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter[data-filter]").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    render();
  });
});

loadData();

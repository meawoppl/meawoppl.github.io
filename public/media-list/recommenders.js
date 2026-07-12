const DATA_BASE = "data/";

let scores = [];
let sortCol = "avg";
let sortAsc = false;

function hashStr(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
  }
  return Math.abs(hash);
}

function autoColor(name) {
  const h = hashStr(name) % 360;
  return `hsl(${h}, 55%, 45%)`;
}

function textColor(bgColor) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, 1, 1);
  const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? "#222" : "#fff";
}

function esc(str) {
  const d = document.createElement("div");
  d.textContent = String(str);
  return d.innerHTML;
}

async function loadData() {
  const [mediaResp, recResp] = await Promise.all([
    fetch(DATA_BASE + "media.json"),
    fetch(DATA_BASE + "recommenders.json"),
  ]);
  const items = mediaResp.ok ? await mediaResp.json() : [];
  const recList = recResp.ok ? await recResp.json() : [];

  const recMap = {};
  const recColors = {};
  for (const r of recList) {
    recMap[r.initial] = r.full_name;
    if (r.color) recColors[r.initial] = r.color;
  }

  const stats = {};
  for (const r of recList) {
    stats[r.initial] = { total: 0, rated: 0, sum: 0, ratings: [] };
  }

  for (const item of items) {
    if (!item.recommended_by) continue;
    for (const r of item.recommended_by) {
      if (!stats[r]) continue;
      stats[r].total++;
      if (item.rating) {
        stats[r].rated++;
        stats[r].sum += item.rating;
        stats[r].ratings.push(item.rating);
      }
    }
  }

  scores = [];
  for (const [initial, s] of Object.entries(stats)) {
    if (s.total === 0) continue;
    const avg = s.rated > 0 ? s.sum / s.rated : null;
    const bg = recColors[initial] || autoColor(initial);
    scores.push({
      initial,
      name: recMap[initial] || initial,
      total: s.total,
      rated: s.rated,
      avg,
      ratings: s.ratings,
      bg,
    });
  }

  render();
}

function sortItems(items) {
  const dir = sortAsc ? 1 : -1;
  return items.slice().sort((a, b) => {
    if (sortCol === "name") {
      return dir * a.name.localeCompare(b.name, undefined, { sensitivity: "base" });
    }
    if (sortCol === "total") {
      return dir * (a.total - b.total);
    }
    if (sortCol === "rated") {
      return dir * (a.rated - b.rated);
    }
    if (sortCol === "avg") {
      const aa = a.avg ?? -1;
      const bb = b.avg ?? -1;
      if (aa !== bb) return dir * (aa - bb);
      return b.total - a.total;
    }
    return 0;
  });
}

function setSort(col) {
  if (sortCol === col) {
    sortAsc = !sortAsc;
  } else {
    sortCol = col;
    sortAsc = col === "name";
  }
  render();
}

function sortIndicator(col) {
  if (sortCol !== col) return "";
  return sortAsc ? " \u25B2" : " \u25BC";
}

function starsFor(rating) {
  return "\u2605".repeat(Math.round(rating));
}

function ratingDistribution(ratings) {
  if (ratings.length === 0) return "";
  const counts = [0, 0, 0, 0, 0];
  for (const r of ratings) counts[r - 1]++;
  const max = Math.max(...counts);

  const W = 120;
  const H = 44;
  const padL = 2;
  const padR = 2;
  const padT = 2;
  const axisH = 10;
  const chartH = H - padT - axisH;
  const bw = (W - padL - padR) / 5;
  const gap = 2;

  let bars = "";
  let labels = "";
  for (let i = 0; i < 5; i++) {
    const h = max > 0 ? (counts[i] / max) * chartH : 0;
    const x = padL + i * bw + gap / 2;
    const y = padT + (chartH - h);
    const w = bw - gap;
    bars += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="1" fill="#f5a623"><title>${i + 1}★: ${counts[i]}</title></rect>`;
    if (counts[i] > 0) {
      bars += `<text x="${x + w / 2}" y="${y - 1}" text-anchor="middle" font-size="7" fill="#666">${counts[i]}</text>`;
    }
    labels += `<text x="${x + w / 2}" y="${H - 1}" text-anchor="middle" font-size="8" fill="#999">${i + 1}</text>`;
  }

  return `<svg class="dist-chart" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Rating distribution">
    <line x1="${padL}" y1="${padT + chartH + 0.5}" x2="${W - padR}" y2="${padT + chartH + 0.5}" stroke="#ddd" stroke-width="1"/>
    ${bars}
    ${labels}
  </svg>`;
}

function render() {
  const content = document.getElementById("content");
  const sorted = sortItems(scores);

  if (sorted.length === 0) {
    content.innerHTML = "<p>No recommenders with recommendations found.</p>";
    return;
  }

  let html = `<table>
    <thead><tr>
      <th class="sortable" data-col="name">Recommender${sortIndicator("name")}</th>
      <th class="sortable" data-col="total">Recs${sortIndicator("total")}</th>
      <th class="sortable" data-col="rated">Rated${sortIndicator("rated")}</th>
      <th class="sortable" data-col="avg">Avg Score${sortIndicator("avg")}</th>
      <th>Distribution</th>
    </tr></thead><tbody>`;

  for (const s of sorted) {
    const fg = textColor(s.bg);
    const bubble = `<span class="rec-bubble" style="background:${s.bg};color:${fg}">${esc(s.initial)}</span>`;
    const avgStr = s.avg !== null ? s.avg.toFixed(1) : "\u2014";
    const stars = s.avg !== null ? `<span class="col-rating">${starsFor(s.avg)}</span>` : "";
    const dist = ratingDistribution(s.ratings);

    html += `<tr>
      <td class="col-recommender">${bubble} ${esc(s.name)}</td>
      <td class="col-num">${s.total}</td>
      <td class="col-num">${s.rated}</td>
      <td class="col-avg">${avgStr} ${stars}</td>
      <td class="col-dist">${dist}</td>
    </tr>`;
  }

  html += "</tbody></table>";
  content.innerHTML = html;

  content.querySelectorAll(".sortable").forEach((th) => {
    th.addEventListener("click", () => setSort(th.dataset.col));
  });
}

loadData();

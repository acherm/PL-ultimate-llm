/* global window */
(() => {
  const PAGE_SIZE = 50;

  function qs(selector) {
    return document.querySelector(selector);
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function dataBase() {
    return (window.__DATA_BASE__ || "./data").replace(/\/$/, "");
  }

  let indexPromise = null;
  async function loadIndex() {
    if (indexPromise) return indexPromise;
    indexPromise = fetch(`${dataBase()}/index.json`, { cache: "no-cache" })
      .then((r) => {
        if (!r.ok) throw new Error(`Failed to load index.json: ${r.status}`);
        return r.json();
      })
      .then((payload) => payload.languages || []);
    return indexPromise;
  }

  function normalize(s) {
    return (s || "").toLowerCase().trim();
  }

  function matchesLang(lang, query) {
    const q = normalize(query);
    if (!q) return false;
    if (normalize(lang.name).includes(q)) return true;
    if ((lang.aliases || []).some((a) => normalize(a).includes(q))) return true;
    return false;
  }

  function formatIsoDate(iso) {
    if (!iso) return "";
    // Keep it simple + stable for a static site.
    return iso.replace("T", " ").replace("Z", " UTC");
  }

  function renderLangList(targetEl, langs, { limit, emptyText }) {
    if (!targetEl) return;
    if (!langs.length) {
      targetEl.innerHTML = `<div class="empty">${escapeHtml(emptyText || "No results.")}</div>`;
      return;
    }
    const slice = typeof limit === "number" ? langs.slice(0, limit) : langs;
    targetEl.innerHTML = `<ul class="lang-list">
      ${slice
        .map((l) => {
          const metaBits = [];
          if (typeof l.program_count === "number") metaBits.push(`${l.program_count} program${l.program_count === 1 ? "" : "s"}`);
          if (l.added_at) metaBits.push(`added ${escapeHtml(formatIsoDate(l.added_at))}`);
          const meta = metaBits.length ? `<div class="muted">${metaBits.join(" · ")}</div>` : "";
          const aliases = (l.aliases || []).length ? `<div class="muted">aka ${escapeHtml(l.aliases.slice(0, 3).join(", "))}${l.aliases.length > 3 ? "…" : ""}</div>` : "";
          return `<li class="lang-row">
            <a class="lang-link" href="${escapeHtml(window.__SITE_ROOT__ || "./")}l/${escapeHtml(l.slug)}/index.html">${escapeHtml(l.name)}</a>
            ${meta}
            ${aliases}
          </li>`;
        })
        .join("")}
    </ul>`;
  }

  async function initHomeSearch() {
    const input = qs("#homeSearch");
    const results = qs("#homeResults");
    if (!input || !results) return;
    const langs = await loadIndex();

    function update() {
      const q = input.value || "";
      if (normalize(q).length < 2) {
        results.innerHTML = `<div class="hint">Type 2+ characters to search.</div>`;
        return;
      }
      const filtered = langs.filter((l) => matchesLang(l, q)).slice(0, 20);
      renderLangList(results, filtered, { emptyText: "No matches." });
    }

    input.addEventListener("input", update);
    update();
  }

  function getParam(name) {
    const u = new URL(window.location.href);
    return u.searchParams.get(name);
  }

  function setParam(name, value) {
    const u = new URL(window.location.href);
    if (!value) u.searchParams.delete(name);
    else u.searchParams.set(name, value);
    window.history.replaceState({}, "", u.toString());
  }

  async function initBrowse() {
    const input = qs("#browseSearch");
    const results = qs("#browseResults");
    const summary = qs("#browseSummary");
    const moreBtn = qs("#browseMore");
    if (!input || !results || !summary || !moreBtn) return;

    const langs = await loadIndex();
    let shown = 0;

    function currentFilters() {
      const q = input.value || "";
      const letter = (getParam("letter") || "").toUpperCase();
      return { q, letter };
    }

    function applyFilters() {
      const { q, letter } = currentFilters();
      let filtered = langs;
      if (letter) filtered = filtered.filter((l) => (l.first_letter || "").toUpperCase() === letter);
      if (normalize(q)) filtered = filtered.filter((l) => matchesLang(l, q));
      return filtered;
    }

    function update() {
      const { q, letter } = currentFilters();
      const hasAnyFilter = normalize(q).length > 0 || !!letter;
      if (!hasAnyFilter) {
        results.innerHTML = `<div class="hint">Pick a letter above or type a search query.</div>`;
        summary.textContent = "";
        moreBtn.hidden = true;
        shown = 0;
        return;
      }

      const filtered = applyFilters();
      const total = filtered.length;
      const nextShown = Math.min(shown || PAGE_SIZE, total);
      const slice = filtered.slice(0, nextShown);
      shown = nextShown;

      summary.textContent = `${total} match${total === 1 ? "" : "es"}${letter ? ` for “${letter}”` : ""}${normalize(q) ? ` · query “${q}”` : ""}`;
      renderLangList(results, slice, { emptyText: "No matches." });

      moreBtn.hidden = shown >= total;
      moreBtn.textContent = `Load more (${Math.min(PAGE_SIZE, total - shown)} more)`;
    }

    function onLetterClick(e) {
      const a = e.target.closest("a[data-letter]");
      if (!a) return;
      e.preventDefault();
      const letter = a.getAttribute("data-letter") || "";
      setParam("letter", letter);
      shown = 0;
      update();
    }

    qs("#browseLetters")?.addEventListener("click", onLetterClick);

    input.value = getParam("q") || "";
    input.addEventListener("input", () => {
      setParam("q", input.value || "");
      shown = 0;
      update();
    });

    moreBtn.addEventListener("click", () => {
      shown += PAGE_SIZE;
      update();
    });

    update();
  }

  async function initRandomButton() {
    const btn = qs("#randomBtn");
    if (!btn) return;
    btn.addEventListener("click", async () => {
      try {
        const langs = await loadIndex();
        if (!langs.length) return;
        const pick = langs[Math.floor(Math.random() * langs.length)];
        const root = window.__SITE_ROOT__ || "./";
        window.location.href = `${root}l/${pick.slug}/index.html`;
      } catch {
        // noop
      }
    });
  }

  function initCopyButtons() {
    document.addEventListener("click", async (e) => {
      const btn = e.target.closest("button.copy-btn");
      if (!btn) return;
      const sel = btn.getAttribute("data-copy-target");
      if (!sel) return;
      const el = qs(sel);
      if (!el) return;
      const text = el.textContent || "";
      try {
        await navigator.clipboard.writeText(text);
        const prev = btn.textContent;
        btn.textContent = "Copied";
        btn.disabled = true;
        setTimeout(() => {
          btn.textContent = prev;
          btn.disabled = false;
        }, 900);
      } catch {
        // Fallback: select text.
        const range = document.createRange();
        range.selectNodeContents(el);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
    });
  }

  async function initAuditView() {
    const loadBtn = qs("#auditLoad");
    const status = qs("#auditStatus");
    const summary = qs("#auditSummary");
    const langList = qs("#auditTopLangs");
    const findingsWrap = qs("#auditFindings");
    const dupesWrap = qs("#auditDuplicates");
    const clustersWrap = qs("#auditClusters");
    const filterInput = qs("#auditFilter");
    const severitySelect = qs("#auditSeverity");
    if (!loadBtn || !status || !summary || !findingsWrap) return;

    let audit = null;
    let index = null;

    function nameToSlugMap() {
      const map = new Map();
      if (index && index.languages) {
        index.languages.forEach((l) => map.set(l.name, l.slug));
      }
      return map;
    }

    function langLink(name, slugMap) {
      const slug = slugMap.get(name);
      if (!slug) return escapeHtml(name);
      const root = window.__SITE_ROOT__ || "./";
      return `<a href="${escapeHtml(root)}l/${escapeHtml(slug)}/index.html">${escapeHtml(name)}</a>`;
    }

    function badge(sev) {
      const s = (sev || "info").toLowerCase();
      return `<span class="audit-badge ${escapeHtml(s)}">${escapeHtml(s)}</span>`;
    }

    function renderSummary() {
      const total = audit?.summary?.findings ?? (audit?.findings?.length || 0);
      let bySeverity = audit?.summary?.by_severity || audit?.by_severity;
      if (!bySeverity) {
        bySeverity = { error: 0, warn: 0, info: 0 };
        (audit?.findings || []).forEach((f) => {
          const sev = String(f.severity || "").toLowerCase();
          if (sev === "error") bySeverity.error += 1;
          else if (sev === "warn" || sev === "warning") bySeverity.warn += 1;
          else if (sev === "info") bySeverity.info += 1;
        });
      }
      const errors = bySeverity.error || 0;
      const warns = bySeverity.warn || 0;
      const infos = bySeverity.info || 0;
      summary.innerHTML = `
        <div class="stats">
          <div class="stat"><div class="num">${total}</div><div class="muted">findings</div></div>
          <div class="stat"><div class="num">${errors}</div><div class="muted">errors</div></div>
          <div class="stat"><div class="num">${warns}</div><div class="muted">warnings</div></div>
          <div class="stat"><div class="num">${infos}</div><div class="muted">infos</div></div>
        </div>
      `;
    }

    function renderTopLangs() {
      if (!langList) return;
      const slugMap = nameToSlugMap();
      let top = audit?.summary?.top_languages || [];
      if (!top.length) {
        const counts = new Map();
        (audit?.findings || []).forEach((f) => {
          if (!f.language) return;
          counts.set(f.language, (counts.get(f.language) || 0) + 1);
        });
        top = Array.from(counts.entries())
          .sort((a, b) => b[1] - a[1])
          .slice(0, 12)
          .map(([name, count]) => [name, count]);
      }
      if (!top.length) {
        langList.innerHTML = `<div class="muted">No per-language findings.</div>`;
        return;
      }
      const max = top[0][1] || 1;
      const rows = top
        .map(([name, count]) => {
          return `<li class="bar-row"><div class="muted">${langLink(name, slugMap)}</div><div class="bar" style="--w:${(count / max) * 100}%"><div></div></div><div class="muted" style="text-align:right;">${count}</div></li>`;
        })
        .join("");
      langList.innerHTML = `<ul class="bar-list">${rows}</ul>`;
    }

    function getFindings() {
      return audit?.findings || [];
    }

    function filteredFindings() {
      const q = (filterInput?.value || "").toLowerCase().trim();
      const sev = (severitySelect?.value || "all").toLowerCase();
      return getFindings().filter((f) => {
        if (sev !== "all" && String(f.severity || "").toLowerCase() !== sev) return false;
        if (!q) return true;
        const blob = [
          f.kind,
          f.language,
          f.message,
          f.program_sha256,
          f.program_folder,
          f.language_folder,
          JSON.stringify(f.details || {}),
        ]
          .join(" ")
          .toLowerCase();
        return blob.includes(q);
      });
    }

    function renderFindings() {
      const slugMap = nameToSlugMap();
      const items = filteredFindings();
      if (!items.length) {
        findingsWrap.innerHTML = `<div class="muted">No findings match the current filter.</div>`;
        return;
      }
      const rows = items
        .slice(0, 200)
        .map((f) => {
          const lang = f.language ? langLink(f.language, slugMap) : "—";
          const msg = escapeHtml(f.message || "");
          const kind = escapeHtml(f.kind || "");
          const details = f.details ? `<div class="muted">${escapeHtml(JSON.stringify(f.details))}</div>` : "";
          return `<tr>
            <td>${badge(f.severity)}</td>
            <td>${lang}</td>
            <td>${kind}</td>
            <td>${msg}${details}</td>
          </tr>`;
        })
        .join("");
      findingsWrap.innerHTML = `
        <table class="audit-table">
          <thead><tr><th>Severity</th><th>Language</th><th>Kind</th><th>Message</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
        <div class="muted" style="margin-top:8px;">Showing ${Math.min(200, items.length)} of ${items.length} findings.</div>
      `;
    }

    function renderDuplicates() {
      if (!dupesWrap) return;
      const slugMap = nameToSlugMap();
      const pairs = audit?.duplicate_candidates || [];
      if (!pairs.length) {
        dupesWrap.innerHTML = `<div class="muted">No duplicate candidates.</div>`;
        return;
      }
      const rows = pairs
        .slice(0, 50)
        .map((p) => {
          return `<tr>
            <td>${langLink(p.a, slugMap)}</td>
            <td>${langLink(p.b, slugMap)}</td>
            <td>${p.score}</td>
          </tr>`;
        })
        .join("");
      dupesWrap.innerHTML = `
        <table class="audit-table">
          <thead><tr><th>Language A</th><th>Language B</th><th>Score</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      `;
    }

    function renderClusters() {
      if (!clustersWrap) return;
      const slugMap = nameToSlugMap();
      const clusters = audit?.clusters || [];
      if (!clusters.length) {
        clustersWrap.innerHTML = `<div class="muted">No clusters.</div>`;
        return;
      }
      const rows = clusters
        .slice(0, 30)
        .map((c) => {
          const links = c.map((name) => langLink(name, slugMap)).join(", ");
          return `<div class="muted">${links}</div>`;
        })
        .join("");
      clustersWrap.innerHTML = rows;
    }

    async function loadAudit() {
      loadBtn.disabled = true;
      status.textContent = "Loading audit.json…";
      try {
        const [auditRes, indexRes] = await Promise.all([
          fetch(`${dataBase()}/audit.json`, { cache: "no-cache" }),
          fetch(`${dataBase()}/index.json`, { cache: "no-cache" }),
        ]);
        if (!auditRes.ok) throw new Error(`audit.json not available (${auditRes.status})`);
        audit = await auditRes.json();
        index = indexRes.ok ? await indexRes.json() : null;
        status.textContent = "Audit loaded.";
        renderSummary();
        renderTopLangs();
        renderFindings();
        renderDuplicates();
        renderClusters();
      } catch (err) {
        status.textContent = `Unable to load audit.json. Run build with --with-audit.`;
      } finally {
        loadBtn.disabled = false;
      }
    }

    loadBtn.addEventListener("click", loadAudit);
    filterInput?.addEventListener("input", renderFindings);
    severitySelect?.addEventListener("change", renderFindings);
  }

  async function initExtensions() {
    const listEl = qs("#extList");
    const detailsEl = qs("#extDetails");
    const searchEl = qs("#extSearch");
    if (!listEl || !detailsEl) return;

    let extData = null;
    let index = null;

    function nameToSlugMap() {
      const map = new Map();
      if (index && index.languages) {
        index.languages.forEach((l) => map.set(l.name, l.slug));
      }
      return map;
    }

    function langLink(name, slugMap) {
      const slug = slugMap.get(name);
      if (!slug) return escapeHtml(name);
      const root = window.__SITE_ROOT__ || "./";
      return `<a href="${escapeHtml(root)}l/${escapeHtml(slug)}/index.html">${escapeHtml(name)}</a>`;
    }

    function renderList(items) {
      if (!items.length) {
        listEl.innerHTML = `<div class="muted">No extensions found.</div>`;
        return;
      }
      const rows = items
        .map((e) => {
          const label = e.extension === "unknown" ? "(unknown)" : `.${e.extension}`;
          return `<li class="bar-row">
            <div><a href="#" data-ext="${escapeHtml(e.extension)}">${escapeHtml(label)}</a></div>
            <div class="bar" style="--w:${(e.program_count / items[0].program_count) * 100}%"><div></div></div>
            <div class="muted" style="text-align:right;">${e.program_count}</div>
          </li>`;
        })
        .join("");
      listEl.innerHTML = `<ul class="bar-list">${rows}</ul>`;
    }

    function renderDetails(extKey) {
      const slugMap = nameToSlugMap();
      const item = extData.extensions.find((e) => e.extension === extKey);
      if (!item) {
        detailsEl.innerHTML = `<div class="muted">Select an extension to view details.</div>`;
        return;
      }
      const label = item.extension === "unknown" ? "(unknown)" : `.${item.extension}`;
      const langs = item.languages || [];
      const langLinks = langs.map((name) => `<span class="pill">${langLink(name, slugMap)}</span>`).join("");
      const examples = (item.examples || [])
        .map((ex) => `<li class="muted">${langLink(ex.language, slugMap)} · ${escapeHtml(ex.title || "")}</li>`)
        .join("");

      detailsEl.innerHTML = `
        <div class="stats" style="margin-bottom:10px;">
          <div class="stat"><div class="num">${item.program_count}</div><div class="muted">programs</div></div>
          <div class="stat"><div class="num">${item.language_count}</div><div class="muted">languages</div></div>
          <div class="stat"><div class="num">${escapeHtml(label)}</div><div class="muted">extension</div></div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">${langLinks || "<span class='muted'>No languages</span>"}</div>
        <div style="margin-top:12px;">
          <h3 style="margin:0 0 6px;">Example programs</h3>
          <ul class="recent">${examples || "<li class='muted'>No examples</li>"}</ul>
        </div>
      `;
    }

    function applyFilter() {
      const q = (searchEl?.value || "").toLowerCase().trim();
      const items = (extData?.extensions || []).filter((e) => {
        if (!q) return true;
        return e.extension.toLowerCase().includes(q);
      });
      renderList(items);
    }

    try {
      const [extRes, indexRes] = await Promise.all([
        fetch(`${dataBase()}/ext_index.json`, { cache: "no-cache" }),
        fetch(`${dataBase()}/index.json`, { cache: "no-cache" }),
      ]);
      if (!extRes.ok) throw new Error("ext_index.json missing");
      extData = await extRes.json();
      index = indexRes.ok ? await indexRes.json() : null;
      renderList(extData.extensions || []);
    } catch {
      listEl.innerHTML = `<div class="muted">Extensions data not available. Rebuild the site.</div>`;
      return;
    }

    listEl.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-ext]");
      if (!a) return;
      e.preventDefault();
      const extKey = a.getAttribute("data-ext");
      renderDetails(extKey);
    });

    searchEl?.addEventListener("input", applyFilter);
    applyFilter();
  }

  function init() {
    initHomeSearch();
    initBrowse();
    initRandomButton();
    initCopyButtons();
    initAuditView();
    initExtensions();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

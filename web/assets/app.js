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
            <a class="lang-link" href="${escapeHtml(window.__SITE_ROOT__ || "./")}l/${escapeHtml(l.slug)}/">${escapeHtml(l.name)}</a>
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
        window.location.href = `${root}l/${pick.slug}/`;
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

  function init() {
    initHomeSearch();
    initBrowse();
    initRandomButton();
    initCopyButtons();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

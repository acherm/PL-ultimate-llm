/* global window */
(() => {
  const PAGE_SIZE = 50;

  /**
   * Submit handler for the per-extension labelling form.
   * Builds the structured GitHub-issue body from form fields and opens the
   * pre-filled issue in a new tab. No backend; pure URL-encoded redirect.
   * Exposed globally because forms use inline onsubmit="return submitExtLabel(this)".
   */
  function _buildExtLabelIssueUrl(form) {
    const ext = form.dataset.ext;
    const repo = form.dataset.repo;
    if (!repo) {
      return { error: "This site has no GitHub repository configured." };
    }
    const labelChoice = (form.label.value || "").trim();
    if (!labelChoice) return { error: "Pick a label first." };
    const customPart = (form.label_custom.value || "").trim();
    let label = labelChoice;
    // Multi-PL submissions: customPart holds a comma-list of full tokens like
    // "pl/c, pl/cpp". Pass it through verbatim — applying the template
    // /<[^>]+>/.replace only substitutes the first match, which would corrupt
    // all subsequent tokens.
    if (customPart.includes(",")) {
      label = customPart;
    } else if (labelChoice.includes("<")) {
      if (!customPart) {
        return { error: "The label has a <…> placeholder; fill the custom field." };
      }
      label = labelChoice.replace(/<[^>]+>/, customPart);
    } else if (customPart) {
      label = customPart;
    }
    const friendly = (form.friendly_name.value || "").trim();
    const refUrl = (form.reference_url.value || "").trim();
    const evidence = (form.evidence.value || "").trim();
    if (!evidence) return { error: "Evidence/notes is required." };
    const yamlBody = `<!-- ext-review: parsed by tools/process_extension_labels.py -->
\`\`\`yaml
ext: "${ext}"
label: "${label.replace(/"/g, '\\"')}"
friendly_name: "${friendly.replace(/"/g, '\\"')}"
reference_url: "${refUrl}"
evidence: |
${evidence.split('\n').map(l => '  ' + l).join('\n')}
\`\`\`

## Submitted from /ext/${ext.replace(/^\./, '')}/
`;
    const title = `Label extension: ${ext}`;
    const url =
      `https://github.com/${repo}/issues/new` +
      `?title=${encodeURIComponent(title)}` +
      `&body=${encodeURIComponent(yamlBody)}` +
      `&labels=ext-review`;
    return { url };
  }

  // Status messages render under the form (id=`label-form-status` on the form's
  // surrounding section). Visible feedback regardless of popup-blocker behaviour.
  function _setExtLabelStatus(form, html, kind) {
    const target = form.querySelector(".ext-label-status");
    if (!target) return;
    target.innerHTML = html;
    target.dataset.kind = kind || "info";
  }

  // Kept around for the inline onsubmit fallback in case older pages still use it.
  // The primary path is the addEventListener wiring below.
  window.submitExtLabel = function(form) {
    return _handleExtLabelSubmit(form);
  };

  function _handleExtLabelSubmit(form) {
    console.log("[ext-label] submit clicked", { ext: form.dataset.ext });
    const result = _buildExtLabelIssueUrl(form);
    if (result.error) {
      console.warn("[ext-label] form error:", result.error);
      _setExtLabelStatus(form, `<strong>Error:</strong> ${result.error}`, "error");
      return false;
    }
    const url = result.url;
    console.log("[ext-label] opening GitHub URL:", url);
    let win = null;
    try { win = window.open(url, "_blank", "noopener"); } catch (e) {
      console.warn("[ext-label] window.open threw:", e);
    }
    if (win) {
      _setExtLabelStatus(
        form,
        `Opened GitHub in a new tab. If you didn't see it (popup blocker), click the link below the button.`,
        "ok",
      );
    } else {
      _setExtLabelStatus(
        form,
        `Browser blocked the new tab. Click the link below the button to open the pre-filled issue.`,
        "warn",
      );
    }
    return false;  // prevent default form submit
  }

  // Quick-pick chips: ticking a proposed-PL chip auto-fills the dropdown +
  // custom field so the reviewer doesn't have to type `pl/<id>` manually.
  function _syncProposedPlChips(form) {
    const chips = form.querySelectorAll("input.proposed-pl");
    if (!chips.length) return;
    const checked = Array.from(chips).filter((c) => c.checked);
    const ids = checked.map((c) => c.value);  // bare ids, e.g., "bazel"
    const custom = form.label_custom;
    const labelSelect = form.label;
    if (ids.length === 1) {
      // Single tick: dropdown `pl/<id>` template + bare id in custom → `pl/<id>`.
      if (labelSelect && labelSelect.value !== "pl/<id>") labelSelect.value = "pl/<id>";
      if (custom) custom.value = ids[0];
      // Pre-fill friendly_name (only if reviewer hasn't typed one yet).
      if (form.friendly_name && !form.friendly_name.value.trim()) {
        const name = checked[0].getAttribute("data-name") || "";
        if (name) form.friendly_name.value = name;
      }
    } else if (ids.length >= 2) {
      // Multi tick: write full `pl/<id>, pl/<id>` so each comma-token is
      // self-contained. The dropdown template stops being meaningful for
      // multi but we still set it so the form validates.
      if (labelSelect && labelSelect.value !== "pl/<id>") labelSelect.value = "pl/<id>";
      if (custom) custom.value = ids.map((id) => `pl/${id}`).join(", ");
    } else {
      // All chips untoggled → blank the custom field only if it currently
      // matches what the chips would have produced (i.e., we filled it).
      // User-typed values are preserved.
      if (custom) {
        const all = Array.from(chips).map((c) => c.value);
        const tokens = custom.value.split(",").map((p) => p.trim().replace(/^pl\//, ""));
        const allFromChips = tokens.length > 0 && tokens.every((t) => all.includes(t));
        if (allFromChips) custom.value = "";
      }
    }
  }

  function _wireExtLabelForms() {
    if (typeof document === "undefined") return;
    const forms = document.querySelectorAll("form.ext-label-form");
    console.log(`[ext-label] wiring ${forms.length} form(s)`);
    forms.forEach((form) => {
      if (form.dataset._wired === "1") return;
      form.dataset._wired = "1";
      // Always-on submit listener (in addition to any inline onsubmit, so we
      // win even if the inline attribute was stripped by content policy).
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        _handleExtLabelSubmit(form);
      });

      // Live-updating fallback link: ALWAYS visible after form is rendered.
      // This is a regular <a> the reviewer can right-click → "Open in new tab"
      // even if popup-blocking interferes with window.open.
      const link = form.querySelector(".ext-label-fallback-link");
      const update = () => {
        if (!link) return;
        const r = _buildExtLabelIssueUrl(form);
        if (r.url) {
          link.href = r.url;
          link.style.display = "";
          link.textContent = "Open the pre-filled GitHub issue ↗";
        } else {
          // Show as disabled until the form has enough info to build a URL.
          link.removeAttribute("href");
          link.style.display = "";
          link.textContent = `(fill the form — ${r.error || "incomplete"})`;
        }
      };
      // Wire chip checkboxes: change → sync custom field + dropdown.
      form.querySelectorAll("input.proposed-pl").forEach((chip) => {
        chip.addEventListener("change", () => {
          _syncProposedPlChips(form);
          update();
        });
      });
      // Initial sync — for confirmed-polysemous, chips render pre-checked.
      _syncProposedPlChips(form);

      form.addEventListener("input", update);
      form.addEventListener("change", update);
      update();
    });
  }
  if (typeof document !== "undefined") {
    // With `defer` the DOM is already parsed when this runs; wire immediately.
    // Also bind to DOMContentLoaded as a belt-and-braces if loading order ever
    // changes; the `_wired` guard makes the second call a no-op.
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", _wireExtLabelForms);
    } else {
      _wireExtLabelForms();
    }
  }

  /**
   * Sample-request form: opens a pre-filled GitHub issue with the
   * `sample-request` label. The maintainer-side script
   * `tools/process_sample_requests.py` later picks these up to drive a
   * targeted SWH mining run.
   */
  function _buildSampleRequestUrl(form) {
    const ext = form.dataset.ext;
    const repo = form.dataset.repo;
    if (!repo) return { error: "This site has no GitHub repository configured." };
    if (!ext) return { error: "Form is missing the extension." };
    const notes = (form.notes ? form.notes.value : "").trim();
    const notesYaml = notes
      ? notes.split("\n").map((l) => "  " + l).join("\n")
      : "  (no notes)";
    const body = `<!-- sample-request: parsed by tools/process_sample_requests.py -->
\`\`\`yaml
ext: "${ext}"
notes: |
${notesYaml}
\`\`\`

## Submitted from /ext/${ext.replace(/^\./, "")}/

Pick this up by running \`python3 tools/process_sample_requests.py\` against this repo.
`;
    const title = `Sample request: ${ext}`;
    const url =
      `https://github.com/${repo}/issues/new` +
      `?title=${encodeURIComponent(title)}` +
      `&body=${encodeURIComponent(body)}` +
      `&labels=sample-request`;
    return { url };
  }

  function _handleSampleRequestSubmit(form) {
    const result = _buildSampleRequestUrl(form);
    const status = form.querySelector(".sample-request-status");
    if (result.error) {
      if (status) status.innerHTML = `<strong>Error:</strong> ${result.error}`;
      return false;
    }
    let win = null;
    try { win = window.open(result.url, "_blank", "noopener"); } catch (_) { /* noop */ }
    if (status) {
      status.innerHTML = win
        ? `Opened GitHub in a new tab. If you didn't see it, click the link to the right of the button.`
        : `Browser blocked the new tab. Click the link to the right of the button.`;
    }
    return false;
  }

  function _wireSampleRequestForms() {
    if (typeof document === "undefined") return;
    const forms = document.querySelectorAll("form.sample-request-form");
    forms.forEach((form) => {
      if (form.dataset._wired === "1") return;
      form.dataset._wired = "1";
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        _handleSampleRequestSubmit(form);
      });
      // Live-updating fallback link so the reviewer can right-click → open
      // even if popups are blocked.
      const link = form.querySelector(".sample-request-fallback-link");
      const update = () => {
        if (!link) return;
        const r = _buildSampleRequestUrl(form);
        if (r.url) {
          link.href = r.url;
          link.textContent = "Open the pre-filled GitHub issue ↗";
        } else {
          link.removeAttribute("href");
          link.textContent = `(${r.error || "incomplete"})`;
        }
      };
      form.addEventListener("input", update);
      form.addEventListener("change", update);
      update();
    });
  }
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", _wireSampleRequestForms);
    } else {
      _wireSampleRequestForms();
    }
  }

  /**
   * Add-PL form on /contribute/add-pl/. Opens a pre-filled GitHub issue with
   * the `pl-add` label and a structured YAML block. The repo-side workflow
   * (.github/workflows/pl-add-pr.yml) picks it up and opens a PR.
   */
  function _yamlEscape(s) {
    // Minimal escaping for double-quoted YAML scalars.
    return (s || "").replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  }
  function _yamlBlockLines(s, indent) {
    const pad = " ".repeat(indent || 2);
    const lines = (s || "").split("\n");
    return lines.map((l) => pad + l).join("\n");
  }

  function _buildPlAddUrl(form) {
    const repo = form.dataset.repo;
    if (!repo) return { error: "This site has no GitHub repository configured." };
    const name = (form.pl_name.value || "").trim();
    if (!name) return { error: "Language name is required." };
    const evidence_url = (form.evidence_url.value || "").trim();
    if (!evidence_url) return { error: "Evidence URL is required." };
    const aliases_raw = (form.aliases.value || "").trim();
    const aliases = aliases_raw
      ? aliases_raw.split(",").map((a) => a.trim()).filter(Boolean)
      : [];
    const aliasesYaml = aliases.length
      ? "[" + aliases.map((a) => `"${_yamlEscape(a)}"`).join(", ") + "]"
      : "[]";
    // Normalize extensions to leading-dot form (".py"); first listed is primary.
    const exts_raw = (form.extensions ? form.extensions.value : "").trim();
    const exts = exts_raw
      ? exts_raw.split(",").map((e) => {
          const t = e.trim();
          if (!t) return "";
          return t.startsWith(".") ? t : "." + t;
        }).filter(Boolean)
      : [];
    const extsYaml = exts.length
      ? "[" + exts.map((e) => `"${_yamlEscape(e)}"`).join(", ") + "]"
      : "[]";
    // Program block — optional. Include only if at least one program field is set.
    const ptitle = (form.program_title.value || "").trim();
    const pext = (form.program_ext.value || "").trim();
    const purl = (form.program_origin_url.value || "").trim();
    const plicense = (form.program_license.value || "").trim();
    const pcode = (form.program_code.value || "").trim();
    const has_program = !!(ptitle || pext || purl || pcode);
    let programYaml = "";
    if (has_program) {
      programYaml = `program:
  title: "${_yamlEscape(ptitle)}"
  ext: "${_yamlEscape(pext)}"
  origin_url: "${_yamlEscape(purl)}"
  license_guess: "${_yamlEscape(plicense)}"
  code: |
${_yamlBlockLines(pcode, 4)}
`;
    } else {
      programYaml = "program: null  # skeleton proposal — maintainer to add program\n";
    }
    const notes = (form.notes.value || "").trim();
    const notesYaml = notes
      ? `notes: |\n${_yamlBlockLines(notes, 2)}\n`
      : "notes: null\n";
    const body = `<!-- pl-add: parsed by tools/process_pl_addition.py -->
\`\`\`yaml
name: "${_yamlEscape(name)}"
aliases: ${aliasesYaml}
evidence_url: "${_yamlEscape(evidence_url)}"
extensions: ${extsYaml}
${programYaml}${notesYaml}\`\`\`

## Submitted from /contribute/add-pl/

The \`pl-add-pr\` workflow opens a draft PR from a \`pl-add/<sanitized-name>\` branch with this content materialized into \`languages/${name.replace(/[^A-Za-z0-9._-]/g, "_")}/\` + \`pl_list.txt\`. Review the PR before merge.
`;
    const title = `Add PL: ${name}`;
    const url =
      `https://github.com/${repo}/issues/new` +
      `?title=${encodeURIComponent(title)}` +
      `&body=${encodeURIComponent(body)}` +
      `&labels=pl-add`;
    return { url };
  }

  function _handlePlAddSubmit(form) {
    const status = form.querySelector(".pl-add-status");
    const result = _buildPlAddUrl(form);
    if (result.error) {
      if (status) status.innerHTML = `<strong>Error:</strong> ${result.error}`;
      return false;
    }
    let win = null;
    try { win = window.open(result.url, "_blank", "noopener"); } catch (_) { /* noop */ }
    if (status) {
      status.innerHTML = win
        ? `Opened GitHub in a new tab. If you didn't see it, click the fallback link.`
        : `Browser blocked the new tab. Click the fallback link to open the pre-filled issue.`;
    }
    return false;
  }

  function _wirePlAddForms() {
    if (typeof document === "undefined") return;
    const forms = document.querySelectorAll("form.pl-add-form");
    forms.forEach((form) => {
      if (form.dataset._wired === "1") return;
      form.dataset._wired = "1";
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        _handlePlAddSubmit(form);
      });
      const link = form.querySelector(".pl-add-fallback-link");
      const update = () => {
        if (!link) return;
        const r = _buildPlAddUrl(form);
        if (r.url) {
          link.href = r.url;
          link.textContent = "Open the pre-filled GitHub issue ↗";
        } else {
          link.removeAttribute("href");
          link.textContent = `(${r.error || "incomplete"})`;
        }
      };
      form.addEventListener("input", update);
      form.addEventListener("change", update);
      update();
    });
  }
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", _wirePlAddForms);
    } else {
      _wirePlAddForms();
    }
  }

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
          if (typeof l.program_count === "number" && l.program_count > 0) metaBits.push(`${l.program_count} program${l.program_count === 1 ? "" : "s"}`);
          if (l.added_at) metaBits.push(`added ${escapeHtml(formatIsoDate(l.added_at))}`);
          const meta = metaBits.length ? `<div class="muted">${metaBits.join(" · ")}</div>` : "";
          const aliases = (l.aliases || []).length ? `<div class="muted">aka ${escapeHtml(l.aliases.slice(0, 3).join(", "))}${l.aliases.length > 3 ? "…" : ""}</div>` : "";
          const badges = [];
          if (l.has_swh) badges.push(`<span class="pill" style="background:rgba(80,200,120,0.18); color:#c6f0d4;" title="${l.swh_sample_count} SWH sample(s)">SWH</span>`);
          if (l.taxonomy_only) badges.push(`<span class="pill src-taxonomy" title="No LLM-curated program">taxonomy</span>`);
          if (typeof l.source_count === "number" && l.source_count >= 4) badges.push(`<span class="pill" title="${l.source_count} sources mention this">×${l.source_count}</span>`);
          const badgeBlock = badges.length ? `<div style="display:inline-flex; gap:6px; margin-left:8px;">${badges.join("")}</div>` : "";
          return `<li class="lang-row">
            <a class="lang-link" href="${escapeHtml(window.__SITE_ROOT__ || "./")}l/${escapeHtml(l.slug)}/index.html">${escapeHtml(l.name)}</a>${badgeBlock}
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
      const hasSwh = !!qs("#fltHasSwh")?.checked;
      const hasLlm = !!qs("#fltLlm")?.checked;
      const taxonomyOnly = !!qs("#fltTaxonomy")?.checked;
      const minSources = parseInt(qs("#fltMinSources")?.value || "0", 10) || 0;
      return { q, letter, hasSwh, hasLlm, taxonomyOnly, minSources };
    }

    function applyFilters() {
      const { q, letter, hasSwh, hasLlm, taxonomyOnly, minSources } = currentFilters();
      let filtered = langs;
      if (letter) filtered = filtered.filter((l) => (l.first_letter || "").toUpperCase() === letter);
      if (normalize(q)) filtered = filtered.filter((l) => matchesLang(l, q));
      if (hasSwh) filtered = filtered.filter((l) => l.has_swh === true);
      if (hasLlm) filtered = filtered.filter((l) => (l.program_count || 0) > 0);
      if (taxonomyOnly) filtered = filtered.filter((l) => l.taxonomy_only === true);
      if (minSources > 0) filtered = filtered.filter((l) => (l.source_count || 0) >= minSources);
      return filtered;
    }

    function update() {
      const f = currentFilters();
      const { q, letter } = f;
      const hasAnyFilter = normalize(q).length > 0 || !!letter ||
        f.hasSwh || f.hasLlm || f.taxonomyOnly || (f.minSources > 0);
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
    ["#fltHasSwh", "#fltLlm", "#fltTaxonomy", "#fltMinSources"].forEach((sel) => {
      const el = qs(sel);
      if (!el) return;
      el.addEventListener("change", () => { shown = 0; update(); });
      if (el.type === "number") el.addEventListener("input", () => { shown = 0; update(); });
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

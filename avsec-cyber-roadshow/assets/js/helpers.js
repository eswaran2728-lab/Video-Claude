/* Shared, deterministic helpers for every scene. Reads data/leaderboard.js. */
(function () {
  var D = window.AVSEC_DATA || {};
  var PH_RE = /^\s*\[.*\]\s*$/;

  function isPlaceholder(v) {
    return v === undefined || v === "" || (typeof v === "string" && PH_RE.test(v));
  }

  function fmtPoints(p) {
    if (typeof p === "number" && isFinite(p)) return p.toLocaleString("en-US");
    return String(p);
  }

  function fmtTime(t) {
    if (t === null || t === undefined || t === false) return null;
    return String(t);
  }

  // Sorted by rank so the edit order of the data block never matters.
  var board = (D.leaderboard || []).slice().sort(function (a, b) {
    return a.rank - b.rank;
  });

  function byRank(r) {
    for (var i = 0; i < board.length; i++) if (board[i].rank === r) return board[i];
    return { rank: r, name: "[NAME]", points: "[POINTS]", time: "[TIME]" };
  }

  var pending = board.some(function (e) {
    return isPlaceholder(e.name) || isPlaceholder(e.points) || isPlaceholder(e.time);
  });

  var url = D.challengeUrl || "";
  var urlOk = !isPlaceholder(url) && /^https:\/\//.test(url);

  // Font size that keeps a line inside `width` px, from character count only
  // (no layout measuring, so every frame renders the same).
  function fitSize(text, width, max, min, perChar) {
    var n = Math.max(1, String(text).length);
    var s = Math.floor(width / (n * (perChar || 0.6)));
    return Math.max(min, Math.min(max, s));
  }

  // Seeded PRNG for confetti and texture positions.
  function rng(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s + 0x6d2b79f5) >>> 0;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Logo lockup: AVSEC badge | Allstars wordmark, each shown whole (object-fit: contain).
  // A logo set to "" becomes a dashed placeholder slot; null leaves it out.
  var LOGOS = [
    { key: "avsec", label: "[AVSEC LOGO]", ratio: 889 / 1048 },
    { key: "allstars", label: "[ALLSTARS LOGO]", ratio: 1.8 },
  ];
  function logoLockup(el, opts) {
    var logos = D.logos || {};
    var shown = 0;
    LOGOS.forEach(function (L) {
      var src = logos[L.key];
      if (src === null || src === undefined) return;
      var h = opts.heights[L.key];
      if (shown++) {
        var bar = document.createElement("i");
        bar.className = "logo-divider";
        bar.style.cssText = "display:block;width:3px;height:" + Math.round(h * 0.7) + "px;background:" + opts.divider;
        el.append(bar);
      }
      var box;
      if (String(src).trim()) {
        box = document.createElement("img");
        box.src = src;
        box.alt = "";
        box.style.cssText = "display:block;height:" + h + "px;width:auto;object-fit:contain";
      } else {
        box = document.createElement("div");
        box.textContent = L.label;
        box.style.cssText = "display:flex;align-items:center;justify-content:center;height:" + h + "px;width:" +
          Math.round(h * L.ratio) + "px;min-width:280px;border:4px dashed " + opts.placeholder + ";border-radius:16px;color:" +
          opts.placeholder + ";font-family:var(--font-mono);font-size:28px;font-weight:700;white-space:nowrap";
      }
      box.className = "logo logo-" + L.key;
      el.append(box);
    });
    return shown;
  }

  var logoPending = ["avsec", "allstars"].some(function (k) {
    return D.logos && D.logos[k] === "";
  });

  window.AVSEC = {
    logoLockup: logoLockup,
    logoPending: logoPending,
    data: D,
    board: board,
    byRank: byRank,
    pending: pending,
    isPlaceholder: isPlaceholder,
    fmtPoints: fmtPoints,
    fmtTime: fmtTime,
    url: url,
    urlOk: urlOk,
    urlLabel: urlOk ? url.replace(/^https:\/\//, "") : "[PUBLIC SPOT THE RISK LINK]",
    fitSize: fitSize,
    rng: rng,
    placeLabel: { 1: "FIRST PLACE", 2: "SECOND PLACE", 3: "THIRD PLACE" },
  };
})();

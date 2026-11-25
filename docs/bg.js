/* PetriPath background: a new microscope slide on every visit.

   The biology sibling of Event Horizon 2.0's poster background. Line drawings from
   Seshan's own work (Pseudomonas with its flagellum, encapsulated Klebsiella, phages,
   mcr-1 and bla plasmids, Kirby–Bauer plates, 96-well screening plates, zebrafish larvae,
   microalgae, DNA, PCR gels) and real lab formulas are scattered behind the page.
   The selected ranking profile makes its own fields more likely: weight(field) gives
   the profile's 0–100 interest in a taxonomy field.

   Colours are CSS variables (style.css, #bg), so a theme switch recolours without a
   redraw. Motion is slow drift and a few twinkling "quantum dots" (a nod to his carbon
   quantum dot paper); it stops entirely when the reader prefers reduced motion.

   API: PPBackground.render({weight, reseed}) */
(function () {
  "use strict";

  let seed = (Date.now() ^ Math.floor(Math.random() * 1e9)) >>> 0;
  let rnd = Math.random;
  let last = {};
  function mulberry(a) {
    return function () {
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const R = (a, b) => a + (b - a) * rnd();
  const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  // stain colours: crystal violet, safranin, fluorescein, antibiotic-disc amber, DAPI cyan
  const INKS = ["v", "p", "g", "a", "c"];
  const f1 = (n) => n.toFixed(1);

  // Each motif draws in a 100 × 100 box; k is the stain.
  const MOTIF = {
    pseudomonas: (k) => `<rect x="16" y="40" width="48" height="20" rx="10" class="s ${k}"/>` +
      `<path d="M64 50c6-7 11 7 17 0s11-7 17 0" class="s ${k}"/>`,
    klebsiella: (k) => `<rect x="26" y="38" width="48" height="24" rx="12" class="s ${k}"/>` +
      `<rect x="16" y="28" width="68" height="44" rx="22" class="s ${k} dash"/>`,
    cocci: (k) => [[40, 40], [56, 38], [48, 52], [64, 52], [34, 56], [52, 66]]
      .map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8" class="s ${k}"/>`).join(""),
    chain: (k) => [14, 29, 44, 59, 74, 89]
      .map((x, i) => `<circle cx="${x}" cy="${50 + (i % 2 ? 6 : -6)}" r="7" class="s ${k}"/>`).join(""),
    phage: (k) => `<path d="M50 10l15 9v18l-15 9-15-9V19z" class="s ${k}"/>` +
      `<path d="M50 46v24M50 70L35 86M50 70l15 16M50 70v18M45 52h10M45 58h10M45 64h10" class="s ${k}"/>`,
    plasmid: (k) => {
      const gene = pick(["mcr-1", "blaNDM-1", "blaKPC-2", "blaOXA-48", "blaCTX-M-15"]);
      return `<circle cx="50" cy="50" r="30" class="s ${k}"/>` +
        `<path d="M50 20a30 30 0 0 1 27 17" class="s ${k} thick"/><path d="M73 31l5 7-8 1" class="s ${k}"/>` +
        `<path d="M23 63a30 30 0 0 1-3-13" class="s ${pick(INKS)} thick"/>` +
        `<text x="50" y="54" class="t ${k}">${gene}</text>`;
    },
    kirby: (k) => `<circle cx="50" cy="50" r="42" class="s ${k}"/><circle cx="50" cy="50" r="38" class="s ${k} faint"/>` +
      [[34, 36, 13], [67, 37, 9], [50, 67, 15]].map(([x, y, z]) =>
        `<circle cx="${x}" cy="${y}" r="${z}" class="s ${k} dash"/><circle cx="${x}" cy="${y}" r="3.6" class="s ${k}"/>`).join(""),
    wells: (k) => {
      let s = `<rect x="5" y="21" width="90" height="60" rx="6" class="s ${k}"/>`;
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 12; c++) {
          const hit = rnd() < 0.08;
          s += `<circle cx="${f1(12.5 + c * 6.8)}" cy="${f1(28.5 + r * 6.7)}" r="2.2" class="${hit ? "f " + pick(["p", "g", "a"]) : "s " + k + " faint"}"/>`;
        }
      }
      return s;
    },
    flask: (k) => `<path d="M40 12h20M44 12v26L24 78c-2 5 1 9 6 9h40c5 0 8-4 6-9L56 38V12" class="s ${k}"/>` +
      `<path d="M30 66h40" class="s ${k} faint"/><circle cx="44" cy="75" r="3" class="s ${k}"/><circle cx="56" cy="70" r="2" class="s ${k}"/>`,
    dna: (k) => {
      let a = "", b = "", rungs = "";
      for (let x = 0; x <= 100; x += 4) {
        const y1 = 50 + 18 * Math.sin((x / 100) * Math.PI * 3), y2 = 100 - y1;
        a += (x ? "L" : "M") + x + " " + f1(y1);
        b += (x ? "L" : "M") + x + " " + f1(y2);
        if (x % 8 === 0) rungs += `M${x} ${f1(y1)}L${x} ${f1(y2)}`;
      }
      return `<path d="${a}" class="s ${k}"/><path d="${b}" class="s ${k}"/><path d="${rungs}" class="s ${k} faint"/>`;
    },
    gel: (k) => {
      let s = `<rect x="14" y="14" width="72" height="72" rx="4" class="s ${k}"/>`;
      for (let l = 0; l < 5; l++) {
        const x = 20 + l * 13;
        s += `<path d="M${x} 21h9" class="s ${k} thick"/>`;
        for (let b = 0; b < 3; b++) s += `<path d="M${x} ${32 + Math.floor(rnd() * 46)}h9" class="s ${l === 0 ? "a" : k}"/>`;
      }
      return s;
    },
    zebrafish: (k) => `<path d="M8 52c14-12 40-14 60-6 8 3 14 4 22-2-2 8-2 14 2 20-7-5-14-4-22-1-20 7-46 4-62-11z" class="s ${k}"/>` +
      `<circle cx="21" cy="51" r="3" class="s ${k}"/><path d="M30 54c12 3 26 3 38-2M36 48c10-2 20-2 30 1" class="s ${k} faint"/>`,
    diatom: (k) => {
      let s = `<ellipse cx="50" cy="50" rx="41" ry="13" class="s ${k}"/><path d="M11 50h78" class="s ${k} faint"/>`;
      for (let x = 17; x <= 83; x += 6) s += `<path d="M${x} 41v18" class="s ${k} faint"/>`;
      return s;
    },
    virus: (k) => {
      let s = `<circle cx="50" cy="50" r="18" class="s ${k}"/>`;
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2;
        const x1 = 50 + 18 * Math.cos(a), y1 = 50 + 18 * Math.sin(a), x2 = 50 + 28 * Math.cos(a), y2 = 50 + 28 * Math.sin(a);
        s += `<path d="M${f1(x1)} ${f1(y1)}L${f1(x2)} ${f1(y2)}" class="s ${k}"/><circle cx="${f1(x2)}" cy="${f1(y2)}" r="2.6" class="s ${k}"/>`;
      }
      return s;
    },
    antibody: (k) => `<path d="M50 88V54M50 54L28 30M50 54l22-24M40 46L20 24M60 46l20-22" class="s ${k} thick"/>`,
    curve: (k) => `<path d="M12 86V14M12 86h78" class="s ${k} faint"/>` +
      `<path d="M14 80c14 0 18-2 24-10s12-44 24-50c8-4 16-4 24 4" class="s ${k} thick"/><text x="70" y="96" class="t ${k}">time</text>`,
    cell: (k) => `<ellipse cx="50" cy="50" rx="38" ry="28" class="s ${k}"/><circle cx="56" cy="48" r="11" class="s ${k} thick"/>` +
      `<path d="M24 42c4-4 8-4 12 0M26 60c4-3 8-3 12 0" class="s ${k} faint"/>`,
    neuron: (k) => `<circle cx="50" cy="50" r="10" class="s ${k}"/><path d="M58 56l30 24M42 44L20 22M44 58L22 76M56 42l12-26M60 50h26" class="s ${k}"/>`,
    leaf: (k) => `<path d="M18 82C18 42 50 16 84 16c0 36-26 66-66 66z" class="s ${k}"/><path d="M18 82L70 30M40 60h14M52 48h10" class="s ${k} faint"/>`,
  };
  // [taxonomy field, motif, base weight]
  const MOTIFS = [
    ["micro", "pseudomonas", 3], ["micro", "klebsiella", 3], ["micro", "phage", 2], ["micro", "plasmid", 2.5],
    ["micro", "kirby", 2.5], ["micro", "cocci", 1.5], ["micro", "chain", 1], ["micro", "virus", 1],
    ["drug", "wells", 2], ["drug", "flask", 1], ["genomics", "dna", 2], ["molbio", "gel", 1.5], ["molbio", "cell", 1],
    ["org", "zebrafish", 1], ["biotech", "diatom", 1], ["immuno", "antibody", 1], ["health", "curve", 1],
    ["org", "neuron", 0.6], ["org", "leaf", 0.6],
  ];
  // [taxonomy field, formula, what it is]
  const FORMULAS = [
    ["micro", "N(t) = N₀ · 2^(t/g)", "exponential growth"],
    ["micro", "CFU/mL = colonies × dilution ÷ volume", "plate count"],
    ["micro", "μ = ln(N₂/N₁) ÷ (t₂ − t₁)", "specific growth rate"],
    ["micro", "MOI = phages ÷ bacteria", "multiplicity of infection"],
    ["micro", "crystal violet → iodine → alcohol → safranin", "Gram stain"],
    ["drug", "Z′ = 1 − 3(σₚ + σₙ) ÷ |μₚ − μₙ|", "screening assay quality"],
    ["drug", "IC₅₀ = dose at 50 % inhibition", "dose–response"],
    ["molbio", "Tₘ ≈ 4(G+C) + 2(A+T) °C", "primer melting, Wallace rule"],
    ["molbio", "copies = N₀ · 2ⁿ", "PCR after n cycles"],
    ["molbio", "v = Vₘₐₓ[S] ÷ (Kₘ + [S])", "Michaelis–Menten"],
    ["genomics", "Q = −10 log₁₀ P", "Phred base quality"],
    ["genomics", "coverage = N · L ÷ G", "Lander–Waterman"],
    ["health", "R₀ = β ÷ γ", "SIR model"],
    ["health", "H′ = −Σ pᵢ ln pᵢ", "Shannon diversity"],
    ["biotech", "A = ε · l · c", "Beer–Lambert, OD₆₀₀"],
    ["org", "p² + 2pq + q² = 1", "Hardy–Weinberg"],
  ];

  function chooser(items, w) {
    const total = items.reduce((s, x) => s + w(x), 0);
    return () => {
      let r = rnd() * total;
      for (const x of items) if ((r -= w(x)) <= 0) return x;
      return items[0];
    };
  }

  function render(opts) {
    const host = document.getElementById("bg");
    if (!host) return;
    last = Object.assign({}, last, opts || {});
    if (last.reseed) { seed = (Math.random() * 4294967296) >>> 0; last.reseed = false; }
    rnd = mulberry(seed);
    const weight = typeof last.weight === "function" ? last.weight : () => 50;
    const W = Math.max(window.innerWidth || 1024, 360), H = Math.max(window.innerHeight || 768, 640);
    const cell = W < 700 ? 150 : 215;
    const cols = Math.ceil(W / cell) + 1, rows = Math.ceil(H / cell) + 1;
    const motif = chooser(MOTIFS, (x) => x[2] * (0.25 + (weight(x[0]) || 0) / 100));
    const formula = chooser(FORMULAS, (x) => 0.25 + (weight(x[0]) || 0) / 100);
    let out = "";
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = c * cell + (r % 2 ? cell / 2 : 0) + R(-0.22, 0.22) * cell;
        const y = r * cell + R(-0.22, 0.22) * cell;
        const roll = rnd();
        if (roll < 0.17) continue;                          // breathing room
        if (roll < 0.29) {
          const [, text, cap] = formula();
          out += `<g transform="translate(${x | 0} ${y | 0}) rotate(${f1(R(-7, 7))})"><text class="ft">${esc(text)}</text>` +
                 `<text y="17" class="fc">${esc(cap)}</text></g>`;
          continue;
        }
        const [, name] = motif();
        const sc = R(0.55, 1.05) * (cell / 215);
        const drift = rnd() < 0.35 ? ` class="drift d${1 + Math.floor(rnd() * 4)}"` : "";
        out += `<g transform="translate(${x | 0} ${y | 0}) rotate(${Math.floor(R(0, 360))}) scale(${sc.toFixed(2)}) translate(-50 -50)">` +
               `<g${drift}>${MOTIF[name](pick(INKS))}</g></g>`;
      }
    }
    let dots = "";
    const n = Math.round((W * H) / 26000);
    for (let i = 0; i < n; i++) {
      dots += `<circle cx="${Math.floor(R(0, W))}" cy="${Math.floor(R(0, H))}" r="${f1(R(1, 2.6))}" class="qd ${pick(["g", "c", "p"])}" ` +
              `style="animation-delay:${f1(R(0, 7))}s"/>`;
    }
    host.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${out}${dots}</svg>`;
  }

  let lastW = 0, timer = null;
  window.addEventListener("resize", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (Math.abs((window.innerWidth || 0) - lastW) > 80) { lastW = window.innerWidth; render(); }
    }, 250);
  });
  lastW = window.innerWidth || 0;

  window.PPBackground = { render };
})();

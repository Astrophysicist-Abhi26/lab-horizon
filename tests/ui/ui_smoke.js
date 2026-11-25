// Clicks through the whole site in a headless DOM and fails on any script error.
//   npm install jsdom@24
//   python scraper/scrape.py --offline --out /tmp/jobs.json
//   node tests/ui/ui_smoke.js /tmp/jobs.json
const fs = require("fs"), path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");
const DOCS = path.join(__dirname, "..", "..", "docs");
const data = JSON.parse(fs.readFileSync(process.argv[2] || path.join(DOCS, "jobs.json"), "utf8"));
const errors = [];
const vc = new VirtualConsole();
vc.on("jsdomError", (e) => { if (!/Not implemented: navigation/.test(e.message)) errors.push("jsdomError: " + e.message); });
vc.on("error", (e) => errors.push("console.error: " + e));
const html = fs.readFileSync(path.join(DOCS, "index.html"), "utf8").replace(/<script src="[^"]+"><\/script>/g, "");
const dom = new JSDOM(html, { url: "https://example.org/lab-horizon/", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
const w = dom.window, d = w.document;
w.fetch = async () => ({ ok: true, json: async () => JSON.parse(JSON.stringify(data)) });
w.eval(fs.readFileSync(path.join(DOCS, "score.js"), "utf8"));
w.eval(fs.readFileSync(path.join(DOCS, "bg.js"), "utf8"));
w.eval(fs.readFileSync(path.join(DOCS, "app.js"), "utf8"));
const tick = () => new Promise((r) => setTimeout(r, 30));
const check = (cond, msg) => { if (!cond) { errors.push("FAIL: " + msg); } else console.log("  ok  " + msg); };
const cards = () => [...d.querySelectorAll("#list article.job")];
const click = (el) => el.dispatchEvent(new w.MouseEvent("click", { bubbles: true }));
const change = (el) => el.dispatchEvent(new w.Event("change", { bubbles: true }));
(async () => {
  await tick(); await tick();
  const n0 = cards().length;
  check(n0 > 20, `positions render (${n0} cards)`);
  check(/Postdoctoral researcher: genomic surveillance/.test(cards()[0].querySelector("h3").textContent), "top card is the Amsterdam UMC AMR postdoc");
  check(/Sample data/.test(d.querySelector("#status").textContent), "sample banner shown for offline data");
  check(d.querySelector("#profile").options.length === data.profiles.list.length, "profile picker lists all profiles");
  check(d.querySelectorAll("#filters details.fld").length >= 5, "field filter shows fields");
  check(/Seshan/.test(d.querySelector("#hello").textContent), "hero greets Seshan");
  check(/Today's plate holds \d+ open positions/.test(d.querySelector("#today").textContent), "hero summarises today's plate");
  check(d.querySelectorAll("#bg svg g").length > 10, "biology background drawn");
  const amrDisc = d.querySelector('#discs [data-preset="amr"]');
  check(!!amrDisc, "quick-search discs rendered");
  click(amrDisc); await tick();
  check(cards().length > 0 && w.location.search.includes("sub=") && amrDisc.getAttribute("aria-pressed") === "true", `AMR disc filters the list (${cards().length})`);
  click(d.querySelector('#filters [data-act="reset"]')); await tick();
  // quick pick: wet lab only
  const wet = d.querySelector('#filters input[data-f="wet"]'); wet.checked = true; change(wet); await tick();
  check(cards().every((c) => /Wet lab|Wet \+ dry/.test(c.querySelector(".badges").textContent)), `wet-lab toggle keeps only wet/hybrid (${cards().length})`);
  check(w.location.search.includes("wet=1"), "filters are kept in the address (bookmarkable)");
  click(d.querySelector('#filters [data-act="reset"]')); await tick();
  check(cards().length === n0, "reset restores everything");
  // position type + region
  const india = d.querySelector('#filters input[data-f="region"][value="india"]'); india.checked = true; change(india); await tick();
  check(cards().length > 0 && cards().every((c) => /🇮🇳/.test(c.querySelector(".meta").textContent)), `region India (${cards().length})`);
  click(d.querySelector('#filters [data-act="reset"]')); await tick();
  // search
  const q = d.querySelector("#q"); q.value = "phage"; q.dispatchEvent(new w.Event("input", { bubbles: true })); await new Promise((r) => setTimeout(r, 250));
  check(cards().length >= 2 && cards().every((c) => /phage/i.test(c.textContent)), `search "phage" (${cards().length})`);
  q.value = ""; q.dispatchEvent(new w.Event("input", { bubbles: true })); await new Promise((r) => setTimeout(r, 250));
  // topic chip filters by sub-field
  const chip = cards()[0].querySelector(".chip"); const sub = chip.dataset.sub; click(chip); await tick();
  check(cards().length > 0 && w.location.search.includes("sub=" + sub), `topic chip filters to ${sub} (${cards().length})`);
  click(d.querySelector('#filters [data-act="reset"]')); await tick();
  // why this score
  check(/Antimicrobial resistance/.test(cards()[0].querySelector(".why").textContent), "score explanation lists the reasons");
  // track + hide
  const first = cards()[0]; const id = first.dataset.id;
  click(first.querySelector('[data-act="track"]')); await tick();
  check(d.querySelector("#tcount").textContent === "1", "tracking updates the tab count");
  check(JSON.parse(w.localStorage.getItem("lh.tracker"))[id].status === "saved", "tracker saved in localStorage");
  const second = cards()[1]; const hid = second.dataset.id;
  click(second.querySelector('[data-act="hide"]')); await tick();
  check(!cards().some((c) => c.dataset.id === hid), "hidden position leaves the list");
  // sort by deadline
  const sort = d.querySelector("#sort"); sort.value = "deadline"; change(sort); await tick();
  const dls = cards().map((c) => data.jobs.find((j) => j.id === c.dataset.id).deadline).filter(Boolean);
  check(dls.join() === [...dls].sort().join(), "deadline sort is chronological");
  sort.value = "match"; change(sort); await tick();
  // profile switch re-ranks
  const sel = d.querySelector("#profile"); sel.value = "ai-wetlab"; change(sel); await tick();
  const topAi = data.jobs.find((j) => j.id === cards()[0].dataset.id);
  check(topAi.sector === "ai-bio", `AI × biology profile puts an AI-bio wet-lab role first (${topAi.title})`);
  sel.value = "seshan"; change(sel); await tick();
  // tune: raise India bonus, India post rises
  click(d.querySelector("#tune-btn")); await tick();
  const rank = () => cards().findIndex((c) => data.jobs.find((j) => j.id === c.dataset.id).region === "india");
  const before = rank();
  const slider = d.querySelector('#tune input[data-tune="regions.india"]'); slider.value = "40"; slider.dispatchEvent(new w.Event("input", { bubbles: true })); await tick();
  check(rank() <= before && rank() === 0, `tuning India +40 lifts the first Indian post from #${before + 1} to #${rank() + 1}`);
  click(d.querySelector("#tune-reset")); await tick();
  // tabs
  click(d.querySelector('.tabs [data-tab="tracker"]')); await tick();
  check(d.querySelectorAll("#board .tcard").length === 1 && !d.querySelector("#view-tracker").hidden, "tracker tab shows the tracked position");
  const st = d.querySelector('#board select[data-t="status"]'); st.value = "applied"; change(st); await tick();
  check(/Applied/.test([...d.querySelectorAll("#board .col")].find((c) => c.querySelector(".tcard")).querySelector("h3").textContent), "status change moves the card");
  const form = d.querySelector("#add-form"); form.querySelector('[name="title"]').value = "LinkedIn post: AMR postdoc, Utrecht";
  form.querySelector('[name="deadline"]').value = "2027-02-01"; form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true })); await tick();
  check(d.querySelectorAll("#board .tcard").length === 2, "manual add works");
  click(d.querySelector('.tabs [data-tab="fellowships"]')); await tick();
  check(/MSCA Postdoctoral Fellowships/.test(d.querySelector("#fellowships").textContent) && /opens 7 Apr 2027/.test(d.querySelector("#fellowships").textContent), "fellowships tab shows MSCA 2027 window");
  click(d.querySelector('#fellowships [data-fid="msca-pf"]')); await tick();
  check(JSON.parse(w.localStorage.getItem("lh.tracker"))["f-msca-pf"].deadline === "2027-09-08", "tracking a fellowship stores its deadline");
  click(d.querySelector('.tabs [data-tab="search"]')); await tick();
  const li = [...d.querySelectorAll("#search a.lcard")].find((a) => /LinkedIn Jobs/.test(a.textContent));
  check(li && /keywords=postdoc%20antimicrobial%20resistance/.test(li.href) && /location=Europe/.test(li.href), "LinkedIn saved search uses his profile terms");
  click(d.querySelector('.tabs [data-tab="sources"]')); await tick();
  check(d.querySelectorAll("#sources table.health tbody tr").length === data.health.length, "sources tab lists every source");
  // calendar file
  let icsText = ""; w.URL.createObjectURL = (b) => { const r = new w.FileReader(); r.onload = () => (icsText = r.result); r.readAsText(b); return "blob:x"; }; w.URL.revokeObjectURL = () => {};
  click(d.querySelector('.tabs [data-tab="tracker"]')); await tick(); click(d.querySelector("#ics")); await new Promise((r) => setTimeout(r, 60));
  check(/BEGIN:VEVENT/.test(icsText) && /DTSTART;VALUE=DATE:20270908/.test(icsText), "calendar export contains the deadlines");
  console.log(errors.length ? "\nPROBLEMS:\n" + errors.join("\n") : "\nAll UI checks passed, no script errors.");
  process.exit(errors.length ? 1 : 0);
})();

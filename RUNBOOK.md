# Runbook

Day-to-day operation of Lab Horizon: first deployment, what runs when, and what to do when something breaks.

## 1. First deployment

```bash
cd lab-horizon
git init -b main
git add .
git commit -m "Lab Horizon: postdoc and biology job radar for Seshan"
git remote add origin https://github.com/Astrophysicist-Abhi26/lab-horizon.git   # create the empty repo on GitHub first
git push -u origin main
```

Then, on GitHub:

1. *Settings → Pages → Build and deployment → Source:* **GitHub Actions**.
2. *Actions → Update positions and publish → Run workflow.* The first run has no earlier state to restore. It collects
   everything, runs the tests, and publishes `https://astrophysicist-abhi26.github.io/lab-horizon/`.
3. If the run says *"GitHub Pages is off"*, step 1 was not saved yet. Fix it and run again.

If the site shows *"No data yet"*, the first run has not finished. Watch it on the *Actions* tab.

## 2. What runs when

| When | What |
|---|---|
| Every day at 07:00 IST (`cron: "30 1 * * *"`) | full update: tests, then collect, classify, rank, publish, then post the digest |
| A push to `main` that touches `scraper/`, `docs/`, `tests/` | the same update (no digest) |
| An "Add a position" issue is opened, edited or closed | the same update, so the position appears or disappears within minutes |
| A pull request, or a push to another branch | tests only (Python suite + site click-through) |

There is no database and no committed data. `docs/jobs.json` is created by each run and published with the site.
The next run reads it back from the live site, which preserves "first seen" dates, "new" badges and source health.

## 3. Reading the Sources tab

| Status | Meaning | Action |
|---|---|---|
| OK | the source answered with postings | — |
| Fewer than usual | fewer than its `min_expected` | usually fine (quiet week); check if it persists |
| Nothing found | answered, but nothing usable | the page layout may have changed: `python scraper/doctor.py --show "<name>"` |
| Error | could not be read (server down, URL moved) | wait a day; if it persists, fix the URL in the YAML |
| Blocked by robots.txt | the site asks automated tools not to read that page | look for a feed or API instead, or remove the source |
| Unconfirmed URL failing | a "to confirm" / "partly confirmed" source failed | fix or set `enabled: false` (see below) |

A source that fails keeps its last good, still-open postings for up to 10 days. They are marked
*"Source down today — last known"*. A confirmed source that newly breaks is also listed in that day's digest.

## 4. Confirming or fixing a source

```bash
pip install -r requirements.txt
python scraper/doctor.py                       # every source: status, postings found, seconds
python scraper/doctor.py --show "Academic Positions"   # print what one source returns
python scraper/doctor.py --probe recursionpharmaceuticals   # which job-board API answers for a company
python scraper/doctor.py --markdown            # regenerate SOURCES.md
```

- **A company board fails:** run `--probe` with the company's board name. Companies often move between Greenhouse,
  Lever, Ashby and Workable. Put the board that answers into `companies.yaml` and set `verified: true`.
- **A Workday site fails:** open the company's careers page in a browser. The address shows the host and site
  (`https://<tenant>.wd3.myworkdayjobs.com/<site>`). Copy them into `companies.yaml`.
- **An institute page returns nothing:** check the page in a browser. If it lists jobs as PDFs in a table, the
  extractor needs a link and a date in the same row. Try `title_cells: 2`, `skip_if: "\\bClosed\\b"` or `include:`.
- Once a source works, change its `verified:` line to say when you checked it.

## 5. Adding an Indian institute or a European lab page

Add an entry to `scraper/institutes.yaml`:

```yaml
  - name: CSIR-IMTECH Chandigarh — project positions
    url: https://<the page that lists current openings>
    group: India
    org: CSIR-Institute of Microbial Technology (IMTECH)
    location: Chandigarh, India
    country: IN
    topics: [life.general]
    keep_untagged: true
    verified: "2026-12 — checked with doctor.py --show"
```

Run `python scraper/doctor.py --show IMTECH`. When the titles and deadlines look right, commit.

## 6. Changing the ranking or the CV profile

- `scraper/profiles.yaml`: weights per field and sub-field, bonuses by position type, lab type, region, visa line.
  The tests check that every name used exists.
- `scraper/cv/seshan.txt`: the research text used for "Similar to the CV". Update it when he publishes or his focus
  changes. Keep it to research content only; the repository is public.
- The site's **Tune** panel changes a profile in one browser only, which is handy for experimenting first.

## 7. The optional Claude fit check

- Turn it on by adding the repository secret `ANTHROPIC_API_KEY`.
- Each day Claude reads up to 40 new postings that already score at least 45 (`LH_LLM_MAX_NEW` changes the number).
  For each it labels wet/dry lab, coding, visa and a 0–100 fit with one sentence of reasons.
- Each posting is read once; results are cached in `scraper/cache/llm_fit.json` between runs.
- The model is `claude-haiku-5-5`; set `LH_LLM_MODEL` in the workflow to change it.
- With no key, nothing is sent and the site works exactly the same, without the notes.

## 8. Renaming or moving

- **New repository name:** the site URL follows it. Nothing in the code depends on the name. The daily run uses
  `GITHUB_REPOSITORY`.
- **New site title:** edit `<title>`, the `<h1>` and `#tagline` in `docs/index.html`, and `site.title` in
  `scraper/scrape.py`.

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| The site says "No data yet" | Pages was just switched on and the first run hasn't finished, or every run failed its tests (see the Actions log) |
| "Data is more than two days old" banner | scheduled runs stopped. GitHub pauses schedules after 60 days without commits: push any small change, or press *Run workflow* |
| The tracker is empty on another device | the tracker lives in each browser's storage. Use *Export backup* and *Import backup* |
| A position appears twice | different titles on two boards. De-duplication merges identical titles (same employer, or same country for long titles) |
| An Indian post shows a wrong deadline | the notice page mixed several dates in one row. Open the PDF; add `include:` / `exclude:` rules if it repeats |

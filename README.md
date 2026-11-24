# Lab Horizon

**Postdocs, fellowships and biology jobs — collected every day and ranked for Seshan Sivasankar.**

A sibling of [Event Horizon 2.0](https://github.com/Astrophysicist-Abhi26/event-horizon-2.0), built the same way
(one shared database, ranked per research profile, rebuilt every morning by GitHub Actions, published on
GitHub Pages) but for **positions** instead of events. It is tailored to one microbiologist's CV:
antimicrobial resistance, clinical and One Health microbiology, genome analysis of pathogens, compound
screening, and years of hands-on wet-lab work.

**Site:** https://astrophysicist-abhi26.github.io/lab-horizon/ (live after the one-time setup below)

## What it does

- **Collects positions every day from 53 sources**, in Europe, India and worldwide:
  - **Academic job boards:** EURAXESS (biological and medical sciences at postdoc level, plus AMR, microbiology,
    infection biology, phage and One Health searches, plus its fellowship and funding offers), Nature Careers,
    Science Careers, Times Higher Education, Chronicle, Inside Higher Ed, jobRxiv, the Max Planck Society,
    jobs.ac.uk, Academic Positions, EuroScienceJobs and SciLifeLab.
  - **India:** IndiaBioscience, Biotecnika, and the notice pages of NCBS, IISc and THSTI.
  - **30 companies, read through their official job-board APIs.** 19 of them are AI labs and
    AI-first biology companies that run their own wet labs: Anthropic, Isomorphic Labs, Xaira, Biohub, Lila Sciences,
    Adaptyv (Lausanne and London), Tabula Bio (AI-designed phage therapies), Latent Labs, Google DeepMind and others.
    The rest are biotech, research foundations and pharma.
  - **Positions added by hand** through an "Add a position" issue.
- **Reads every posting** and labels it:
  - which of 10 fields and 38 sub-fields it belongs to;
  - position type (postdoc, fellowship, scientist, technician-level, faculty);
  - wet lab / wet + dry / computational, and whether it is coding-heavy;
  - seniority, and whether the advert offers or refuses visa sponsorship.
  - It also compares the text with his research profile (`scraper/cv/seshan.txt`).
- **Ranks** everything with Seshan's profile by default. 9 other profiles (microbiology, AI × biology
  wet labs, molecular & cell biology, genomics, immunology, biotech industry, public health, plant & ecology, or
  everything) re-rank the same list instantly. The **Tune** panel adjusts any profile with sliders.
- **Filters and sorts** by field, region and country, sector, position type, lab type, deadline and posting date.
  Quick picks hide coding-heavy roles, senior roles, technician-level roles, or roles that refuse visa sponsorship.
  Every card has a **Why this score?** breakdown.
- **Tracks applications**, kept only in the browser:
  - stages Saved → Preparing → Applied → Interview → Offer;
  - deadlines, follow-up dates, notes, and a document checklist;
  - export of every deadline to a calendar (.ics), plus backup export and import.
- **Fellowships tab:** 13 schemes he can apply for with a host lab (MSCA Postdoctoral Fellowships with the
  checked 2027 dates, EMBO, HFSP, Humboldt, EMBL, FEMS, India Alliance, ANRF N-PDF, DBT-RA, ICMR, CSIR…), plus
  live funding calls from EURAXESS.
- **Search elsewhere:** one-click LinkedIn, Google Jobs, X, Bluesky and EURAXESS searches built from his profile.
- **Daily digest:** new strong matches (and any source that broke) are posted as a comment on a GitHub issue.
  Subscribe to that issue to get them by e-mail.

## How Seshan's ranking works

Each position gets 0–100 for the selected profile. For Seshan's profile (`scraper/profiles.yaml`):

- **Topic:** antimicrobial resistance 100; anti-infective drug discovery 95; clinical microbiology and microbial
  genomics 90; pathogenesis, One Health and phage biology 85; other microbiology 70; epidemiology 70; molecular
  biology 65; and so on down to ecology 10. A second field adds a quarter of its weight.
- **Position and place:**
  - postdoc +12, fellowship +10, scientist +8, technician-level −15;
  - wet lab +10, computational −25, coding-heavy −20, senior −12;
  - Europe +12, India +4, North America +3;
  - visa support mentioned +4, sponsorship refused −35.
- **His CV:** up to +20 for text similar to his research profile.
- **Co-author network:** a small bonus for Amsterdam UMC, Münster and Tübingen, where (as far as we know) his
  co-authors work. Edit the list freely.
- **Optional Claude fit check:** ±10.

The total goes through a soft cap, so strong matches don't all tie at 100. The same formula runs in Python
(`scraper/profiles.py`) and in the browser (`docs/score.js`); a test checks that they agree to the last point.

## What it cannot do

- **LinkedIn and X** forbid automated collection and hide most posts behind a login, so they are not scraped.
  The *Search elsewhere* tab opens ready-made searches instead. Anything found there can be added to the tracker,
  or put on the site with an **Add a position** issue.
- **Labels are keyword-based**, so read the original advert before applying. Add an Anthropic API key and Claude
  will also read the best matches and write a one-line fit note for each.
- **31 sources were confirmed live in November 2026, 6 partly, and
  16 follow a site's usual pattern but were not tested.** They are mostly big-pharma Workday sites
  and well-known company boards. If one fails, the **Sources** tab shows it in amber and
  `python scraper/doctor.py --probe <name>` finds the right board.
- It reads public pages only, respects every site's `robots.txt`, and asks each host at most once a second.

## Set up (once, about 10 minutes)

1. **Create a public repository** on GitHub named `lab-horizon`, then push this folder to it (commands in
   [RUNBOOK.md](RUNBOOK.md)).
2. **Turn on Pages:** go to *Settings → Pages* and set *Source* to **GitHub Actions**.
3. **Run it once:** on the *Actions* tab, open **Update positions and publish** and click **Run workflow**. The run
   takes about 10–15 minutes. After that it runs every morning at 07:00 IST.
4. **Optional:** add a repository secret `ANTHROPIC_API_KEY` (*Settings → Secrets and variables → Actions*) to turn
   on the Claude fit check. It reads at most 40 new postings a day, each only once.
5. **Optional:** after the first scheduled run, open the issue labelled **digest** and click *Subscribe*. Seshan can
   do the same with his GitHub account.

## Run it on your computer

```bash
pip install -r requirements.txt
python scraper/scrape.py --offline            # no network: builds docs/jobs.json from the test fixtures
python -m http.server -d docs 8000            # then open http://localhost:8000
python scraper/scrape.py                      # the real thing (5–15 minutes)
python scraper/doctor.py --show EURAXESS      # test one source live and print what it finds
```

## Change things

| To … | edit |
|---|---|
| add a job board or feed | `scraper/sources.yaml` |
| add an institute notice page | `scraper/institutes.yaml` |
| add a company (Greenhouse, Lever, Ashby, Workable, Workday) | `scraper/companies.yaml`, find its board with `doctor.py --probe` |
| change what ranks first | `scraper/profiles.yaml` (or the **Tune** panel, per browser) |
| update his research profile for the CV match | `scraper/cv/seshan.txt` |
| add or update a fellowship | `scraper/fellowships.yaml` |
| pin a position permanently | `scraper/watchlist.yaml`, or open an **Add a position** issue |

[SOURCES.md](SOURCES.md) lists every source with how it is read and how it was checked
(`python scraper/doctor.py --markdown` regenerates it).

## Repository layout

```
scraper/   scrape.py (daily pipeline) · sources_*.py (feeds, EURAXESS, web pages, company APIs, manual)
           classify.py · taxonomy.py · geo.py · profiles.py · cvmatch.py · llm_fit.py · doctor.py · digest.py
           *.yaml (sources, institutes, companies, profiles, fellowships, watchlist) · cv/seshan.txt
docs/      the website: index.html · app.js · score.js · style.css   (jobs.json is written by the daily run)
tests/     pytest suite on offline fixtures · ui/ui_smoke.js (clicks through the site in a headless DOM)
.github/   daily update + deploy workflow · test workflow · "Add a position" and "Suggest a source" forms
```

## Tests

`python -m pytest -q tests` runs everything offline against saved copies of each source (`tests/fixtures`). It covers:
- every parser;
- the classifier and the ranking, including the browser/Python agreement;
- the whole pipeline (de-duplication, expiry, carrying a broken source's postings forward) and every config file.

The daily run stops before publishing if a test fails, so the live site keeps its last good data. Pull requests also
run `tests/ui/ui_smoke.js`, which clicks through every tab of the site.

Built with Claude for Seshan Sivasankar · MIT licence

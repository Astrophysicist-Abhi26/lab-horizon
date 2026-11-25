<p align="center"><img src="docs/icon.svg" width="96" alt="PetriPath icon"></p>

# PetriPath

**Postdocs, fellowships and biology jobs, cultured fresh every morning for Dr Seshan Sivasankar.**

The name is the idea: a Petri dish whose colonies grow into a path to his next lab. PetriPath is a sibling of
[Event Horizon 2.0](https://github.com/Astrophysicist-Abhi26/event-horizon-2.0). Both keep one shared database,
ranked per research profile, rebuilt every morning by GitHub Actions and published on GitHub Pages. PetriPath does
this for **positions** instead of events, and it is tailored to one microbiologist's CV: antimicrobial resistance,
clinical and One Health microbiology, genome analysis of pathogens, compound screening, and years of hands-on
wet-lab work.

**Site:** https://astrophysicist-abhi26.github.io/lab-horizon/ (or `/petripath/` after the optional rename below) ·
**Android app:** the [latest release](../../releases/latest)

## How it looks, and why

- **Gram-stain colours.** The interface uses crystal violet. Safranin pink marks his Gram-negative world: wet-lab
  roles and the strongest matches. Fluorescein green marks anything new, and antibiotic-disc amber marks
  deadlines. The default background is a deep "darkfield" indigo; the light theme is a freshly stained slide.
- **Seshan on a plate.** The hero shows an illustrated Seshan in his blue suit, pointing out of a MacConkey agar
  plate. The plate has pink Klebsiella-like colonies, and meropenem, imipenem and ceftazidime discs with their
  zones of inhibition. The colonies grow when the page opens.
- **A new microscope slide on every visit.** Like Event Horizon's physics poster, the background redraws itself.
  It uses line drawings from his own papers: Pseudomonas with its flagellum, encapsulated Klebsiella, phages,
  mcr-1 and bla plasmid maps, Kirby–Bauer plates, the 96-well plates of his MMV screens, zebrafish larvae (the
  carbon-quantum-dot paper), microalgae (his biofuel internship), DNA, PCR gels. It also shows real lab formulas
  (Z′-factor, Wallace rule, Phred quality…) and a few twinkling quantum dots. The ranking profile picks which
  fields appear most.
- **Scores as zones of inhibition.** Each card's match score is a zone around an antibiotic disc: a bigger zone
  means a better match.
- Type is Bricolage Grotesque for headings and Atkinson Hyperlegible for long job lists. Motion stops for anyone
  who asks their device for reduced motion.

## What it does

- **Collects positions every day from 53 sources**, in Europe, India and worldwide:
  - **Academic boards:**
    - EURAXESS: biological and medical sciences at postdoc level; AMR, microbiology, infection-biology, phage
      and One Health searches; and its fellowship offers.
    - Nature Careers, Science Careers, Times Higher Education, Chronicle, Inside Higher Ed, jobRxiv, the Max
      Planck Society, jobs.ac.uk, Academic Positions, EuroScienceJobs and SciLifeLab.
  - **India:** IndiaBioscience, Biotecnika, and the notice pages of NCBS, IISc and THSTI.
  - **30 companies, read through their official job-board APIs.** 19 of them are AI labs and
    AI-first biology companies that run their own wet labs: Anthropic, Isomorphic Labs, Xaira, Biohub, Lila,
    Adaptyv, Tabula Bio, Latent Labs, Google DeepMind and others.
- **Reads every posting** and labels it: field (10 fields, 38 sub-fields), position
  type, wet / wet + dry / computational, coding-heavy, seniority, and any visa line. It also compares the text
  with his research profile.
- **Ranks** with Seshan's profile by default. 9 other profiles re-rank the same list instantly, and
  the **Tune** panel adjusts any of them with sliders. Every card has a **Why this score?** breakdown.
- **Quick searches** on the hero, one tap each: AMR & infection, Europe wet labs, AI labs with wet benches, India,
  closing soon, and new since the last visit. Full filters and sorting sit underneath.
- **Tracker:**
  - stages Saved → Preparing → Applied → Interview → Offer;
  - deadlines, follow-ups, notes and a document checklist;
  - deadlines exported to the phone's calendar.
  - It is kept on the device only, with backup export and import.
- **Fellowships:** 13 schemes, including the checked MSCA 2027 dates, plus live funding calls.
- **Search elsewhere:** one-tap LinkedIn, Google Jobs, X, Bluesky and EURAXESS searches built from his profile
  (LinkedIn and X cannot be collected automatically).
- **Daily digest:** new strong matches are posted to a GitHub issue. Subscribe to it to get them by e-mail.

## The Android app

`android/` is a small native app (`PetriPath.apk`) that opens the live site full-screen. Job adverts open in the
phone's browser. The tracker is kept on the phone, and calendar exports go to Downloads. After one visit online,
the last positions stay readable without a signal.

GitHub builds it: **Actions → Build Android app → Run workflow**. About five minutes later, `PetriPath.apk`
appears on the repository's **Releases** page, and the site's **Android app** button always points to the newest
build. To install it, send Seshan the link or the file. He taps it on his phone and allows installing from his
browser or WhatsApp when Android asks. Later builds install over the old one, and the tracker is kept.

On an iPhone (or without the APK), open the site in the browser and use **Add to Home Screen**: the site works as
an installable web app too.

## Set up (once)

1. Push this folder to the `lab-horizon` repository (commands in [RUNBOOK.md](RUNBOOK.md)).
2. *Settings → Pages → Source*: **GitHub Actions**.
3. *Actions → Update positions and publish → Run workflow*. After this it runs every morning at 07:00 IST.
4. *Actions → Build Android app → Run workflow* for the APK.
5. Optional:
   - **Rename the repository** to `petripath` (*Settings → General*). Do this before step 4, because the app
     opens whatever address the repository has when it is built.
   - **Add the secret** `ANTHROPIC_API_KEY` for Claude's one-line fit notes.
   - **Subscribe** to the *digest* issue.

## What it cannot do

- **LinkedIn and X** forbid automated collection, so their posts are not collected. Use *Search elsewhere*, then
  add finds to the tracker or with an **Add a position** issue.
- **Labels come from keywords,** so read the original advert before applying.
- **Not every source is confirmed yet:** 31 sources were confirmed live in November 2026,
  6 partly, and 16 follow a site's usual pattern. Anything failing shows
  amber on the **Sources** tab, and `python scraper/doctor.py` helps fix it.
- It reads public pages only, respects `robots.txt`, and asks each host at most once a second.

## Run it on your computer

```bash
pip install -r requirements.txt
python scraper/scrape.py --offline         # no network: builds docs/jobs.json from the test fixtures
python -m http.server -d docs 8000         # then open http://localhost:8000
python scraper/scrape.py                   # the real collection (5–15 minutes)
python scraper/doctor.py --show EURAXESS   # test one source live
```

## Change things

| To … | edit |
|---|---|
| add a job board, feed, institute or company | `scraper/sources.yaml`, `institutes.yaml`, `companies.yaml` |
| change what ranks first | `scraper/profiles.yaml` (or the **Tune** panel, per browser) |
| update his research profile for the CV match | `scraper/cv/seshan.txt` |
| add or update a fellowship | `scraper/fellowships.yaml` |
| redraw the avatar or icon | `tools/make_art.py`, then `python tools/make_art.py` (needs `pip install resvg-py`) |
| change colours, type or the background slide | `docs/style.css`, `docs/bg.js` |

[SOURCES.md](SOURCES.md) lists every source and how it was checked.

## Repository layout

```
scraper/   daily pipeline (scrape.py), source readers, classifier, ranking, Claude fit check, doctor, digest
docs/      the website: index.html · app.js · score.js · bg.js · style.css · sw.js · seshan.svg · icons
android/   the Android app (built by .github/workflows/android.yml)
tools/     make_art.py: redraws the avatar and icons
tests/     pytest suite on offline fixtures · ui/ui_smoke.js clicks through the whole site
```

## Tests

`python -m pytest -q tests` runs offline against saved copies of every source. It covers:
- the parsers;
- the classifier, including the AMR false-positive guard;
- the ranking, and that the browser computes the same scores as Python;
- the full pipeline and the config files.

The daily run publishes nothing if a test fails. Pull requests also run the site click-through.

Built for Seshan by his friend Abhishek · MIT licence

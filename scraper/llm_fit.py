"""
Optional: Claude reads the best-matching postings and judges them for Seshan.

For each posting it returns lab (wet / hybrid / dry), whether real programming is
required, the visa line, a fit score 0-100 and one sentence of reasons. The keyword
classifier's lab / coding / visa labels are replaced by Claude's, and the `llm` weight in
profiles.yaml turns the fit into points (+/- 10 for Seshan's profile).

Runs only when ANTHROPIC_API_KEY is set (a repository secret). Each posting is read once:
results are cached in scraper/cache/llm_fit.json, which the GitHub Action keeps between
runs. LH_LLM_MAX_NEW bounds the new readings per run (default 40), LH_LLM_MODEL picks
the model (default claude-haiku-5-5).
"""

import json
import os
import re

import common as C

API = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("LH_LLM_MODEL", "claude-haiku-5-5")
MAX_NEW = int(os.environ.get("LH_LLM_MAX_NEW", "40"))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "llm_fit.json")

CANDIDATE = """PhD in microbiology (2026, India). Five years of hands-on wet-lab research on antimicrobial
resistance: carbapenem- and colistin-resistant Gram-negative bacteria (Klebsiella, Pseudomonas,
Enterobacterales) from clinical, poultry and food samples; whole-genome sequencing data analysis of
pathogens; in vitro screening of compound libraries (MMV boxes) against drug-resistant clinical
isolates; PCR, Sanger sequencing, bacterial culture and susceptibility testing. Six papers, four as
first author. Limited programming (basic bioinformatics tools only). Based in India: needs a visa
or work permit for posts abroad. Prefers Europe; also open to India, the US and industry,
including AI companies that run wet labs."""

PROMPT = """You screen job postings for one candidate.

Candidate:
{candidate}

Posting:
Title: {title}
Organisation: {org}
Location: {location}
Text: {text}

Answer with one JSON object and nothing else:
{{"lab": "wet" | "hybrid" | "dry", "coding_required": true | false,
  "visa": "sponsors" | "no-sponsorship" | "unknown", "fit": <integer 0-100>,
  "why": "<one sentence, at most 25 words, on why this does or does not suit the candidate>"}}
"lab" is "wet" when most of the work is at the bench, "dry" when it is computational.
"coding_required" is true only if substantial programming is a requirement, not a plus.
"fit" weighs topic, seniority, wet-lab focus and whether he could realistically be hired."""


def _load():
    try:
        with open(CACHE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(cache):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=0, sort_keys=True)


def cache_key(job):
    return job["id"] + ":" + C.text_hash(job.get("title"), job.get("description", "")[:4000])


def _parse(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    data = json.loads(m.group(0)) if m else {}
    out = {}
    if data.get("lab") in ("wet", "hybrid", "dry"):
        out["lab"] = data["lab"]
    if isinstance(data.get("coding_required"), bool):
        out["coding"] = data["coding_required"]
    if data.get("visa") in ("sponsors", "no-sponsorship", "unknown"):
        out["visa"] = data["visa"]
    try:
        out["fit"] = max(0, min(100, int(data["fit"])))
    except (KeyError, TypeError, ValueError):
        return None
    out["why"] = C.truncate(str(data.get("why", "")), 200)
    return out


def ask(job, key):
    prompt = PROMPT.format(candidate=CANDIDATE, title=job.get("title", ""), org=job.get("org", ""),
                           location=job.get("location", ""), text=C.truncate(job.get("description", ""), 3500))
    r = C.HTTP.post(API, timeout=(10, 90), headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": MODEL, "max_tokens": 300, "messages": [{"role": "user", "content": prompt}]})
    r.raise_for_status()
    text = "".join(b.get("text", "") for b in r.json().get("content", []) if b.get("type") == "text")
    return _parse(text)


def apply(job, label):
    job["llm"] = {"fit": label["fit"], "why": label["why"]}
    for k in ("lab", "coding", "visa"):
        if k in label:
            job[k] = label[k]


def label_jobs(candidates, all_jobs):
    """Reads up to MAX_NEW uncached `candidates`; applies every cached label to `all_jobs`."""
    cache = _load()
    key = os.environ.get("ANTHROPIC_API_KEY")
    asked = failed = 0
    if key:
        for job in candidates:
            if asked >= MAX_NEW:
                break
            k = cache_key(job)
            if k in cache:
                continue
            try:
                label = ask(job, key)
            except Exception as e:                                  # noqa: BLE001
                failed += 1
                if failed >= 3:
                    print(f"  Claude fit check stopped after 3 errors: {e}")
                    break
                continue
            asked += 1
            if label:
                cache[k] = label
        _save(cache)
    used = 0
    for job in all_jobs:
        label = cache.get(cache_key(job))
        if label:
            apply(job, label)
            used += 1
    if not key:
        return {"status": "off", "detail": f"no ANTHROPIC_API_KEY; {used} cached readings reused"}
    return {"status": "ok", "detail": f"{asked} new readings with {MODEL}, {used} applied, {failed} errors"}

import json

import common as C
import offline
import scrape as S

GONE = ["PhD position in bacterial cell biology", "Lecturer in Accounting", "Software Engineer, Infrastructure",
        "Postdoc in microbial ecology of soils", "Postdoc in Quantum Optics (m/f/d)", "PhD Studentship in Plant Pathology",
        "Postdoc position in Human-Centred Artificial Intelligence", "Engineer Trainee (IT Department) at NCBS"]


def run(tmp_path, monkeypatch, name="jobs.json"):
    monkeypatch.setattr(C, "HTTP", C.HTTP)          # undone after the test
    monkeypatch.setattr(C, "HOST_GAP", 0)
    out = tmp_path / name
    assert S.main(["--offline", "--out", str(out), "--notify", str(tmp_path / "notify"), "--no-llm", "--workers", "4"]) == 0
    return out, json.loads(out.read_text())


def test_offline_run_builds_the_site_data(tmp_path, monkeypatch):
    _, d = run(tmp_path, monkeypatch)
    titles = {j["title"] for j in d["jobs"]}
    assert d["sample"] is True and d["profiles"]["default"] == "seshan" and d["fellowships"]
    assert "Research Scientist, Life Sciences (Experimental Biology)" in titles
    assert "Research Scientist, Biosecurity" in titles
    for gone in GONE:
        assert gone not in titles
    top = d["jobs"][0]
    assert top["region"] == "europe" and "micro.amr" in top["topics"] and top["kind"] == "postdoc"
    for j in d["jobs"]:
        assert {"id", "title", "url", "kind", "sector", "lab", "region", "topics", "first_seen", "summary"} <= set(j)
    assert len(d["health"]) == len(S.build_sources())
    amr = [j for j in d["jobs"] if "carbapenem-resistant Enterobacterales" in j["title"]]
    assert len(amr) == 1 and len(amr[0]["sources"]) >= 3                 # one posting, several EURAXESS searches
    assert (tmp_path / "notify" / "digest.md").read_text().startswith("### ")


def test_first_seen_survives_and_a_broken_source_is_carried(tmp_path, monkeypatch):
    out, d = run(tmp_path, monkeypatch)
    d["sample"] = False                                # pretend it was a real deployed run
    tabula = next(j for j in d["jobs"] if j.get("org") == "Tabula Bio")
    tabula["first_seen"] = "2026-11-01"
    out.write_text(json.dumps(d))
    monkeypatch.setattr(offline, "ROUTES", [("GET", r"job-board/tabulabio\b", "missing.json")] + offline.ROUTES)
    _, d2 = run(tmp_path, monkeypatch)
    health = {h["name"]: h for h in d2["health"]}
    assert health["Tabula Bio"]["status"] == "error" and health["Tabula Bio"]["carried"] == 1
    t2 = next(j for j in d2["jobs"] if j.get("org") == "Tabula Bio")
    assert t2["carried"] and t2["first_seen"] == "2026-11-01"

from classify import classify


def c(title, description="", org="", location="", **hints):
    return classify({"title": title, "description": description, "org": org, "location": location, "hints": hints})


def test_amr_postdoc_in_europe():
    j = c("Postdoctoral Researcher in Antimicrobial Resistance of Klebsiella pneumoniae",
          "Wet-lab project on carbapenem resistance: bacterial culture, PCR and whole-genome sequencing of clinical "
          "isolates. PhD in microbiology required. Visa support available.", "Amsterdam UMC", "Amsterdam, Netherlands")
    assert j["relevant"] and j["kind"] == "postdoc" and j["lab"] == "wet" and j["region"] == "europe"
    assert j["topics"][0] == "micro.amr" and j["sector"] == "academic" and j["visa"] == "sponsors" and not j["coding"]


def test_ai_lab_wet_and_dry_roles():
    wet = c("Research Scientist, Life Sciences (Experimental Biology)",
            "Design and run experimental programs: molecular biology, biochemistry, protein and nucleic acid "
            "characterization, assay development. PhD in a biological science. We do sponsor visas!",
            "Anthropic", "San Francisco, CA", sector="ai-bio")
    assert (wet["kind"], wet["lab"], wet["sector"], wet["visa"], wet["coding"]) == ("scientist", "wet", "ai-bio", "sponsors", False)
    dry = c("Machine Learning Scientist, AI for Protein Engineering",
            "Strong ML fundamentals; proficiency in Python and PyTorch; protein design; wet-lab teams.",
            "Lila Sciences", "San Francisco, CA", sector="ai-bio")
    assert dry["relevant"] and dry["lab"] == "dry" and dry["coding"]


def test_not_research_or_not_biology_is_dropped():
    assert not c("Software Engineer, Infrastructure", "Kubernetes", "Anthropic", sector="ai-bio")["relevant"]
    assert not c("Lecturer in Accounting", "Financial accounting")["relevant"]
    assert not c("Postdoc in galaxy evolution", "stellar populations")["relevant"]
    assert not c("Postdoc position in Human-Centred Artificial Intelligence", "HCI and AI safety")["relevant"]
    assert not c("Machine Learning Engineer", "PyTorch, LLMs, Python pipelines")["relevant"]
    assert not c("PhD position in bacterial cell biology", "Streptococcus")["relevant"]


def test_research_associate_depends_on_country_and_sector():
    assert c("Research Associate, Biology", "PCR, cloning. BS or MS in microbiology.", "Anthropic",
             "San Francisco, CA", sector="ai-bio")["kind"] == "technician"
    uk = c("Research Associate in Bacterial Genomics", "PhD required. Eligible for sponsorship under the Skilled "
           "Worker route.", "University of Oxford", "Oxford, UK")
    assert (uk["kind"], uk["level"], uk["visa"]) == ("postdoc", "mid", "sponsors")
    assert c("Research Associate-I (Bacterial pathogenesis)", "", "THSTI", "Faridabad")["kind"] == "postdoc"
    assert c("Junior Research Fellow (JRF)", "MSc Microbiology", "CSIR-IMTECH", "Chandigarh")["kind"] == "technician"


def test_visa_refusal_wins_and_wet_cues():
    j = c("Senior Scientist, Phage Engineering", "Hands-on bench role in phage engineering; molecular biology. "
          "We are unable to sponsor visas for this role.", "Tabula Bio", "San Francisco", sector="ai-bio")
    assert (j["visa"], j["lab"], j["level"]) == ("no-sponsorship", "wet", "senior")
    assert c("Biologist, DeepMind", "3 years of wet-lab experience with high-consequence pathogens. Microbiology.",
             "Google DeepMind", "London, UK", sector="ai-bio")["lab"] == "wet"

"""
The biology taxonomy: 10 fields, 38 sub-fields, each with keyword patterns.

A sub-field id is "<field>.<name>" (micro.amr). Patterns are case-insensitive regular
expressions. A pattern starting with "!" is *strong*: one mention in the description
is enough to tag the sub-field. A pattern starting with "~" is *generic* (words like
"evolution", "AI", "Python", "surveillance" that also occur outside biology): it never
tags a sub-field on its own, even in a title, but it counts towards the two-pattern rule.
A pattern starting with "@" is read in the title only, and is strong there: a job titled
"... Antimicrobial Research" is about antimicrobials, while the word inside a description may not be.
Otherwise a sub-field is tagged when the title matches, or when two different patterns
match the description.

A posting is relevant to the site only if it has a topic outside CONTEXT_ONLY (AI, lab
automation, nanomaterials, QC, lab operations, clinical trials need a biology topic
beside them); company boards of biology companies may also count lab operations and QC.

The site's field filter and every research profile (profiles.yaml) use these ids;
tests/test_config.py fails if a profile names an id that is not here.
"""

import re

FIELDS = {
    "micro": "Microbiology & infection",
    "drug": "Drug discovery & therapeutics",
    "immuno": "Immunology & vaccines",
    "molbio": "Molecular & cell biology",
    "genomics": "Genomics & computational biology",
    "biotech": "Biotechnology & bioengineering",
    "health": "Epidemiology & public health",
    "org": "Organismal, plant & ecology",
    "ops": "Quality, biosafety & lab operations",
    "life": "Life sciences (general)",
}

_B = r"(?<![\w-])"          # left word boundary that also treats "-" as part of a word
_E = r"(?![\w-])"

SUBFIELDS = {
    # ── Microbiology & infection ───────────────────────────────────────────
    "micro.amr": ("Antimicrobial resistance", [
        r"@\b(antimicrobials?|antibiotics?)\b", r"!antimicrobial[- ]resistan\w*", r"!antibiotic[- ]resistan\w*", r"!\bAMR\b", r"!carbapenem\w*",
        r"!colistin", r"!\bmcr-\d", r"!\bESBLs?\b", r"!(beta|β)-?lactamase\w*", r"!\b(NDM|KPC|OXA-48)\b",
        r"!\bMRSA\b", r"!\bVRE\b", r"multi-?drug[- ]resist\w*", r"pan-?drug[- ]resist\w*",
        r"\b(MDR|XDR|PDR)\b", r"!resistome", r"!antimicrobial stewardship",
        r"!antimicrobial susceptibility", r"!minimum inhibitory concentration",
        r"~drug[- ]resistan\w*", r"~resistance mechanism\w*", r"~\bantibiotics?\b", r"~\bantimicrobials?\b",
        r"persister\w*", r"~efflux pump\w*"]),
    "micro.phage": ("Bacteriophages & phage therapy", [
        r"!bacteriophage\w*", r"!\bphages?\b", r"!phage therap\w*", r"!endolysin\w*", r"\blysins?\b"]),
    "micro.clinical": ("Clinical & diagnostic microbiology", [
        r"!clinical microbiolog\w*", r"!medical microbiolog\w*", r"!diagnostic microbiolog\w*",
        r"!clinical isolates?", r"!nosocomial", r"!(hospital|healthcare)[- ]acquired",
        r"infection (prevention|control)", r"\bsepsis\b|bloodstream infection\w*",
        r"urinary tract infection\w*", r"\binfectious diseases?\b", r"blood cultures?",
        r"diagnostic\w* (assay|test)\w*", r"clinical (laborator\w*|diagnostics?)"]),
    "micro.pathogenesis": ("Bacterial pathogenesis & host–pathogen", [
        r"!host[- ]pathogen", r"!pathogenesis", r"!virulence", r"!infection biology",
        r"bacterial (pathogens?|infections?)", r"!Pseudomonas", r"!Klebsiella", r"!Acinetobacter",
        r"Escherichia coli|\bE\. ?coli\b", r"!Salmonella", r"!Staphylococc\w*", r"Streptococc\w*",
        r"Enterobacter\w*", r"!Mycobacteri\w*|tubercul\w*", r"Clostridi\w*|C\. ?difficile",
        r"Helicobacter", r"Neisseria", r"\bVibrio\b", r"\bListeria\b", r"Campylobacter", r"\bShigella\b",
        r"biofilm\w*", r"quorum sensing", r"\bpathogens?\b"]),
    "micro.genomics": ("Microbial genomics & genomic epidemiology", [
        r"!genomic epidemiolog\w*", r"!whole[- ]genome sequencing|\bWGS\b",
        r"!(bacterial|microbial|pathogen) genom\w*", r"!\b(cg|wg)?MLST\b", r"!phylogenom\w*",
        r"pan-?genom\w*", r"\bplasmids?\b", r"mobile genetic elements?", r"!genomic surveillance",
        r"\bnanopore\b", r"comparative genomics", r"\bAMRFinder|ResFinder|\bCARD\b"]),
    "micro.onehealth": ("One Health, food & environmental microbiology", [
        r"!one health", r"!food microbiolog\w*", r"food safety", r"food-?borne",
        r"!environmental microbiolog\w*", r"~wastewater|sewage", r"soil microb\w*",
        r"water microbiolog\w*|aquatic microb\w*", r"\bzoono\w*", r"veterinar\w*",
        r"livestock|poultry|chickens?|cattle|swine|\bpigs?\b|aquaculture", r"agricultural microb\w*"]),
    "micro.microbiome": ("Microbiome & metagenomics", [
        r"!microbiome\w*", r"!microbiota", r"!metagenom\w*", r"metatranscriptom\w*", r"\b16S\b",
        r"gut bacteri\w*", r"commensal\w*"]),
    "micro.virology": ("Virology", [
        r"!virolog\w*", r"~\bvir(al|us|uses)\b", r"!SARS-CoV-2|coronavir\w*", r"\bHIV\b", r"!influenza",
        r"dengue|zika|arbovir\w*", r"hepatitis"]),
    "micro.mycoparasit": ("Mycology, parasitology & tropical infection", [
        r"!mycolog\w*", r"\bfung(al|i|us)\b", r"!antifungal\w*", r"!\bCandida\b", r"!Aspergill\w*",
        r"!parasitolog\w*", r"\bparasit\w*", r"!malaria|Plasmodium", r"Leishmani\w*|Trypanosom\w*",
        r"helminth\w*", r"!tropical (medicine|diseases?|infections?)|neglected tropical"]),
    "micro.general": ("Microbiology (general)", [
        r"!microbiolog\w*", r"!\bmicrob(e|es|ial)\b", r"\bbacteri(a|al|um)\b", r"infecti(on|ous)\w*",
        r"\bmicroorganisms?\b"]),
    # ── Drug discovery ─────────────────────────────────────────────────────
    "drug.antiinfective": ("Anti-infective drug discovery", [
        r"@\b(antimicrobials?|antibiotics?)\b(?![- ]resist)", r"!antibiotic (discovery|development)", r"!antibacterial\w*", r"!anti-?infective\w*",
        r"antimicrobial (peptides?|drugs?|discovery|compounds?|agents?)",
        r"!antifungal (discovery|drugs?|compounds?)", r"!antiviral (drugs?|discovery|compounds?)",
        r"natural products?", r"!\bMMV\b|Pathogen Box|Pandemic Response Box", r"\bhit compounds?\b"]),
    "drug.screening": ("Screening, assays & pharmacology", [
        r"!high[- ]throughput screen\w*|\bHTS\b", r"!(compound|drug|phenotypic) screen\w*",
        r"!assay development", r"in vitro pharmacolog\w*|cellular pharmacolog\w*", r"\bADME\b|DMPK",
        r"hit[- ]to[- ]lead|lead optimi[sz]ation", r"target (identification|validation)",
        r"mechanism of action", r"~(molecular )?docking", r"dose[- ]response"]),
    "drug.biologics": ("Biologics, antibodies & peptides", [
        r"!antibod(y|ies)", r"\bbiologics?\b", r"protein therapeutics?", r"peptide (drugs?|therapeutics?|design)",
        r"\bmAbs?\b", r"nanobod\w*", r"~binder\w*"]),
    "drug.general": ("Drug discovery (general)", [
        r"!drug discovery", r"drug development", r"~pharmaceutic\w*", r"~\btherapeutics?\b",
        r"medicinal chemistry", r"pharmacolog\w*", r"preclinical"]),
    # ── Immunology ─────────────────────────────────────────────────────────
    "immuno.vaccines": ("Vaccines", [r"!vaccin\w*", r"immunogen\w*", r"adjuvants?"]),
    "immuno.general": ("Immunology", [
        r"!immunolog\w*", r"immune (response|system|cells?)", r"\b(T|B)[- ]cells?\b", r"macrophages?",
        r"innate immun\w*", r"inflammat\w*", r"cytokines?", r"neutrophils?"]),
    # ── Molecular & cell biology ───────────────────────────────────────────
    "molbio.molecular": ("Molecular biology & genetics", [
        r"!molecular biolog\w*", r"\b(q|RT-?q?|digital )?PCR\b", r"molecular cloning|\bcloning\b",
        r"\bCRISPR\w*", r"gene (expression|editing|regulation)", r"\bgenetics?\b", r"\bSanger\b",
        r"plasmid (construction|prep\w*)", r"transcriptom\w*|RNA-?seq", r"western blot\w*",
        r"genome editing", r"nucleic acids?", r"\bmutagenesis\b"]),
    "molbio.cell": ("Cell biology & cell culture", [
        r"!cell biolog\w*", r"!(cell|tissue) culture", r"mammalian cells?", r"stem cells?|\biPSCs?\b",
        r"organoids?", r"flow cytometr\w*|\bFACS\b", r"~microscop\w*", r"cell[- ]based assays?",
        r"live[- ]cell imaging"]),
    "molbio.biochem": ("Biochemistry, proteins & structural biology", [
        r"!biochemi\w*", r"protein (expression|purification|science|engineering|characteri[sz]ation)",
        r"\benzym\w*", r"!structural biolog\w*", r"cryo-?EM|crystallograph\w*",
        r"~mass spectrometr\w*", r"proteomic\w*", r"biophysic\w*", r"~\bSPR\b|\bITC\b|\bBLI\b"]),
    "molbio.cancer": ("Cancer biology", [r"!\bcancer\b|oncolog\w*", r"tumou?rs?\b", r"\bHPV\b|papillomavir\w*"]),
    # ── Genomics & computation ─────────────────────────────────────────────
    "genomics.ngs": ("Sequencing & genomics", [
        r"!next[- ]generation sequencing|\bNGS\b", r"\bsequencing\b", r"\bgenomics?\b", r"single[- ]cell",
        r"\bIllumina\b", r"long[- ]read", r"library prep\w*"]),
    "genomics.bioinfo": ("Bioinformatics & computational biology", [
        r"!bioinformatic\w*", r"!computational biolog\w*", r"systems biolog\w*", r"biostatistic\w*",
        r"~(data|sequence) analysis", r"~\bpipelines?\b", r"~\bPython\b", r"Bioconductor|\bR\b programming",
        r"~\bin silico\b"]),
    "genomics.aibio": ("AI / machine learning for biology", [
        r"!machine learning", r"!deep learning", r"~artificial intelligence|\bAI\b", r"~foundation models?",
        r"~(protein )?language models?|\bLLMs?\b", r"protein design|generative (models?|design)",
        r"~autonomous (lab\w*|science)|closed[- ]loop", r"~active learning"]),
    # ── Biotechnology ──────────────────────────────────────────────────────
    "biotech.synbio": ("Synthetic biology & protein engineering", [
        r"!synthetic biolog\w*", r"!protein engineering|directed evolution", r"metabolic engineering",
        r"strain (engineering|construction|development)", r"genetic circuits?"]),
    "biotech.industrial": ("Industrial, algal & environmental biotech", [
        r"!industrial biotech\w*", r"bioprocess\w*", r"\bfermentation\b", r"!biofuels?|bioenerg\w*",
        r"!microalga\w*|\balga(e|l)\b", r"bioremediation", r"biomanufactur\w*", r"biocatalys\w*"]),
    "biotech.nano": ("Nanobiotechnology & biomaterials", [
        r"!nanobiotech\w*", r"~nanoparticles?|nanomaterials?|nanotechnolog\w*", r"~quantum dots?|carbon dots?|\bCQDs?\b",
        r"biomaterials?", r"drug delivery|lipid nanoparticles?|\bLNPs?\b"]),
    "biotech.automation": ("Lab automation & robotics", [
        r"!lab(oratory)? automation", r"liquid[- ]handl\w*", r"~robotic\w*",
        r"high[- ]throughput (experiment\w*|lab\w*)", r"!cloud lab|self-driving lab|automated lab\w*",
        r"~\bopentrons\b|\bhamilton\b"]),
    # ── Health ─────────────────────────────────────────────────────────────
    "health.epi": ("Epidemiology & surveillance", [
        r"!epidemiolog\w*", r"~\bsurveillance\b", r"~\boutbreaks?\b", r"transmission (dynamics|model\w*)",
        r"cohort stud\w*", r"!public health"]),
    "health.global": ("Global & tropical health", [
        r"!global health", r"\bLMICs?\b|low- and middle-income", r"neglected diseases?", r"~\btropical\b"]),
    "health.clinical": ("Clinical & translational research", [
        r"!clinical (trials?|research|stud(y|ies))", r"translational (research|medicine|biology)",
        r"patient (samples?|cohorts?)", r"biobank\w*", r"~\bclinicians?\b"]),
    # ── Organismal ─────────────────────────────────────────────────────────
    "org.plant": ("Plant biology & agriculture", [
        r"!plant (biology|sciences?|patholog\w*|microb\w*|physiolog\w*)", r"!botan\w*", r"agronom\w*",
        r"~\bcrops?\b", r"Arabidopsis"]),
    "org.ecology": ("Ecology, evolution & marine biology", [
        r"!ecolog\w*", r"!evolution(ary)? biolog\w*", r"~\bevolution(ary)?\b", r"biodiversity", r"!marine biolog\w*",
        r"zoolog\w*", r"~\bconservation\b"]),
    "org.neuro": ("Neuroscience", [r"!neurosci\w*|neurobiolog\w*", r"\bneurons?\b|neuronal", r"~\bbrain\b"]),
    "org.dev": ("Developmental biology & model organisms", [
        r"!developmental biolog\w*", r"!zebrafish", r"Drosophila", r"C\. ?elegans", r"mouse models?",
        r"in vivo models?", r"\bembryo\w*"]),
    # ── Quality, biosafety, lab operations ────────────────────────────────
    "ops.qc": ("Quality control & regulatory", [
        r"!quality control", r"~\bQC\b", r"!quality assurance", r"~\bQA\b", r"\bGMP\b|good manufacturing practice",
        r"\bGLP\b|good laboratory practice", r"sterility test\w*|environmental monitoring",
        r"ISO 15189|ISO 17025|accreditation", r"regulatory affairs"]),
    "ops.biosafety": ("Biosafety & biosecurity", [
        r"!biosafety|biosecurity", r"!\bBSL-?[234]\b|containment level [234]|\bCL[34]\b",
        r"!select agents?", r"!dual[- ]use", r"!high[- ]consequence pathogens?",
        r"biological (weapons?|threats?)|biodefen[cs]e|biothreats?"]),
    "ops.labops": ("Lab operations & facilities", [
        r"!lab(oratory)? (operations|manager|management)", r"core facilit\w*|facility manager",
        r"lab(oratory)? coordinator"]),
    # ── General ────────────────────────────────────────────────────────────
    "life.general": ("Life sciences (general)", [
        r"\bbiolog(y|ical|ist)\b", r"!\blife[- ]sciences?\b", r"bioscien\w*", r"biomedic\w*",
        r"biotechnolog\w*"]),
}


def field_of(node):
    return node.split(".", 1)[0]


# Without one of their unmistakable terms (carbapenem, colistin, "antimicrobial resistance" …), these
# sub-fields also need a microbial context: cancer "multidrug resistance" is not AMR.
_MICROBIAL = re.compile(r"bacteri|microb|pathogen|infecti|antibiotic|fung|isolates?\b|nosocomial|gram[- ](negative|positive)|"
                        r"klebsiella|pseudomonas|acinetobacter|e\. ?coli|salmonella|staphylococc|enterobacter|mycobacteri|tubercul",
                        re.I)
REQUIRES = {"micro.amr": _MICROBIAL, "drug.antiinfective": _MICROBIAL}
CONTEXT_ONLY = {"genomics.aibio", "biotech.automation", "biotech.nano", "ops.qc", "ops.labops", "health.clinical"}
COMPANY_CORE = {"ops.qc", "ops.labops", "biotech.automation"}   # core on a biology company's own board


def _compile(pattern):
    title_only = pattern.startswith("@")
    return (pattern.startswith("!") or title_only, pattern.startswith("~"), title_only,
            re.compile(pattern.lstrip("!~@"), re.I))


COMPILED = {sid: [_compile(p) for p in pats] for sid, (_, pats) in SUBFIELDS.items()}
NODES = set(FIELDS) | set(SUBFIELDS)


def label(node):
    if node in SUBFIELDS:
        return SUBFIELDS[node][0]
    return FIELDS.get(node, node)


def tag(title, text):
    """Sub-fields found in a posting, strongest first, as [(id, strength)].

    strength = 3 per title pattern + 1 per description pattern (distinct patterns).
    Tagged when the title matches, a strong pattern matches the description, or two
    patterns match the description."""
    title = title or ""
    text = text or ""
    out = []
    for sid, pats in COMPILED.items():
        t_hits = d_hits = specific = 0
        strong_hit = strong_any = False
        for strong, generic, title_only, rx in pats:
            if title_only:
                if rx.search(title):
                    t_hits += 1
                    strong_any = True
                continue
            if rx.search(title):
                if generic:
                    d_hits += 1
                else:
                    t_hits += 1
                strong_any = strong_any or strong
            elif rx.search(text):
                d_hits += 1
                specific += not generic
                strong_hit = strong_hit or strong
        if t_hits or strong_hit or (d_hits >= 2 and specific):
            need = REQUIRES.get(sid)
            if need and not (strong_any or strong_hit) and not need.search(title + " " + text):
                continue
            out.append((sid, 3 * t_hits + d_hits))
    out.sort(key=lambda x: -x[1])
    return out

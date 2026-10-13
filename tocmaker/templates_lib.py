"""Example specs per template (also used by tests and by `toc init`)."""
from __future__ import annotations

EXAMPLES = {
    "flow": """# Left-to-right story: exposure -> mechanism -> outcome (the ES&T / Environ Int default)
journal: {journal}
palette: envtox
template: flow
panels:
  - role: exposure
    label: Prenatal PFAS exposure
    sublabel: maternal serum, 1st trimester
    icons: [pregnant-woman, chemical-flask-hazard]
  - role: mechanism
    label: Placental inflammation
    icons: [placenta-umbilical, inflammation-cell]
  - role: outcome
    label: Lower birth weight
    icons: [fetus]
    badge: "−48 g per ln-unit"
arrows:
  - {{from: 0, to: 1}}
  - {{from: 1, to: 2, label: mediates, style: dashed}}
footer: "n = 1,203 mother–infant pairs, prospective cohort"
""",
    "cohort": """# Epidemiology: population -> exposure assessment -> model -> outcome, with the key estimate as a badge
journal: {journal}
palette: calm
template: cohort
panels:
  - role: organism
    label: 12,480 adults
    sublabel: 3 Chinese cities, 2015–2023
    icons: [cohort-people, map-pin-region]
  - role: exposure
    label: Long-term PM2.5
    sublabel: satellite-based, 1 km
    icons: [pm25-particles]
  - role: method
    label: Cox models + mediation
    icons: [forest-plot-mini]
  - role: outcome
    label: Incident hypertension
    icons: [heart-rate-ecg]
    badge: "HR 1.18 per 10 µg/m³"
arrows:
  - {{from: 0, to: 1}}
  - {{from: 1, to: 2}}
  - {{from: 2, to: 3}}
""",
    "split": """# Many sources -> one model system -> several outcomes
journal: {journal}
palette: envtox
template: split
panels:
  - role: exposure
    label: Microplastics
    icons: [plastic-bottle-microplastics]
  - role: exposure
    label: Cadmium
    icons: [water-drop-contaminated]
  - role: organism
    label: Zebrafish larvae, 5 dpf
    sublabel: co-exposure, 96 h
    icons: [{{id: zebrafish-larva, scale: 1.3}}]
  - role: outcome
    label: Hypoactivity
    icons: [dose-response-curve]
  - role: outcome
    label: Gut dysbiosis
    icons: [gut-microbiome]
  - role: outcome
    label: Oxidative stress
    icons: [ros-radical]
left: [0, 1]
center: 2
right: [3, 4, 5]
""",
    "hub": """# One central hazard with converging evidence lines
journal: {journal}
palette: alert
template: hub
center: 0
hub_direction: in
panels:
  - role: outcome
    label: Thyroid disruption
    icons: [thyroid]
    badge: "TSH ↑ 14%"
  - role: exposure
    label: Drinking-water PFAS
    icons: [tap-faucet]
  - role: exposure
    label: Dietary fish
    icons: [food-fish-plate]
  - role: mechanism
    label: Receptor binding
    icons: [receptor-ligand]
  - role: organism
    label: Cohort, n = 2,310
    icons: [cohort-people]
""",
    "two_row": """# Two evidence streams (in vivo + human) converging on one outcome
journal: {journal}
palette: envtox
template: two_row
converge: 4
panels:
  - role: exposure
    label: BPA analogues
    icons: [chemical-flask-hazard]
  - role: organism
    label: Zebrafish
    icons: [zebrafish-adult]
  - role: exposure
    label: Urinary BPA
    icons: [blood-drop]
  - role: organism
    label: Children, n = 980
    icons: [child]
  - role: outcome
    label: Impaired neurodevelopment
    icons: [brain]
    badge: "β = −2.1 IQ"
rows: [[0, 1], [2, 3]]
""",
    "cycle": """# Circular story (source -> environment -> exposure -> effect -> policy)
journal: {journal}
palette: calm
template: cycle
panels:
  - role: exposure
    label: Emissions
    icons: [factory-smokestack]
  - role: method
    label: Monitoring
    icons: [map-pin-region]
  - role: organism
    label: Exposure
    icons: [human-adult]
  - role: outcome
    label: Health burden
    icons: [lungs]
""",
}


def example_spec(template: str = "flow", journal: str = "acs") -> str:
    if template not in EXAMPLES:
        raise KeyError(f"no example for template '{template}'; known: {', '.join(EXAMPLES)}")
    return EXAMPLES[template].format(journal=journal)

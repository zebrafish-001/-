# envtox icon set

Flat vector icons for journal TOC graphics / graphical abstracts in environmental toxicology and population health.

## License

These icons are original work created for this repository and are released under the
[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) public-domain dedication.
You may copy, modify, distribute and use them, including commercially, without attribution.

## File conventions

- Every file is a standalone SVG: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">`, no `width`/`height`.
- Only `<path>`, `<circle>`, `<ellipse>`, `<rect>`, `<polygon>`, `<line>`, `<polyline>` and `<g>` are used; no `<text>`, `<style>`, CSS classes, gradients, filters, rasters or external references.
- ~6 units of margin inside the viewBox; stroke widths 4-6 (thicker only for silhouette-like strokes), `stroke-linecap="round" stroke-linejoin="round"`.
- Line 1 of each file is `<!-- keywords: ... -->` with English (and, where natural, Chinese) search keywords.

## Colour tokens

The renderer recolours icons by literal string replacement, so exactly these uppercase hex values appear in the files and nothing else:

| Token | Hex | Role |
|---|---|---|
| primary ink | `#1F2937` | main silhouette / outline |
| accent | `#4F8FC0` | one meaningful element: pollutant, water, organ highlight, ligand, curve |
| white | `#FFFFFF` | optional cut-outs and highlights (eyes, windows, nucleus) |

`fill="none"` is used for open outlines.

Validate with the convention checker (XML, viewBox, forbidden elements, colour literals) before adding or editing icons.

## Icons

### Organisms and people

| File | Keywords |
|---|---|
| `zebrafish-adult.svg` | zebrafish, adult fish, Danio rerio, model organism, aquatic, 斑马鱼, 成鱼 |
| `zebrafish-larva.svg` | zebrafish larva, embryo, yolk sac, dpf, developmental toxicity, 斑马鱼幼鱼, 胚胎 |
| `mouse.svg` | mouse, rodent, laboratory animal, in vivo, murine, 小鼠, 动物实验 |
| `human-adult.svg` | adult, person, human, standing figure, population, 成人, 人群 |
| `pregnant-woman.svg` | pregnant woman, pregnancy, maternal exposure, prenatal, gestation, 孕妇, 妊娠 |
| `child.svg` | child, kid, children, pediatric, early life, 儿童, 幼儿 |
| `elderly-person.svg` | elderly, older adult, ageing, senior, cane, geriatric, 老年人, 老龄化 |
| `cohort-people.svg` | cohort, population, group, participants, epidemiology, people, 队列, 人群 |
| `fetus.svg` | fetus, prenatal, in utero, embryo, womb, developmental, 胎儿, 宫内 |

### Organs

| File | Keywords |
|---|---|
| `lungs.svg` | lungs, respiratory, pulmonary, inhalation, airway, 肺, 呼吸 |
| `brain.svg` | brain, neurotoxicity, neurodevelopment, cognition, nervous system, 大脑, 神经 |
| `liver.svg` | liver, hepatotoxicity, hepatic, metabolism, 肝脏, 肝毒性 |
| `heart.svg` | heart, cardiovascular, cardiotoxicity, cardiac, 心脏, 心血管 |
| `kidney.svg` | kidney, renal, nephrotoxicity, ureter, 肾脏, 肾毒性 |
| `placenta-umbilical.svg` | placenta, umbilical cord, maternal-fetal transfer, prenatal, 胎盘, 脐带 |
| `gut-intestine.svg` | gut, intestine, gastrointestinal, bowel, digestion, 肠道, 消化道 |
| `thyroid.svg` | thyroid, endocrine, hormone, trachea, endocrine disruption, 甲状腺, 内分泌 |
| `blood-drop.svg` | blood, drop, serum, biomarker, blood sample, 血液, 血滴 |
| `sperm-ovum.svg` | fertility, sperm, ovum, egg, reproduction, reproductive toxicity, 生殖, 精子, 卵子 |

### Exposure sources

| File | Keywords |
|---|---|
| `factory-smokestack.svg` | factory, industry, smokestack, emission, air pollution, industrial, 工厂, 排放 |
| `car-exhaust.svg` | car, vehicle, traffic, exhaust, emission, roadway, 汽车, 尾气 |
| `cigarette-smoke.svg` | cigarette, smoking, tobacco, secondhand smoke, nicotine, 吸烟, 香烟 |
| `pesticide-sprayer.svg` | pesticide, spray, agriculture, insecticide, herbicide, farm, 农药, 喷洒 |
| `plastic-bottle-microplastics.svg` | plastic bottle, microplastics, nanoplastics, polymer, fragmentation, 塑料, 微塑料 |
| `pm25-particles.svg` | PM2.5, particulate matter, aerosol, air pollution, fine particles, haze, 细颗粒物, 雾霾 |
| `water-drop-contaminated.svg` | water, contamination, pollutant, drinking water, aquatic, 水污染, 水滴 |
| `tap-faucet.svg` | tap, faucet, drinking water, water supply, plumbing, 水龙头, 自来水 |
| `food-fish-plate.svg` | seafood, fish, dietary exposure, food, plate, diet, 鱼类, 饮食暴露 |
| `chemical-flask-hazard.svg` | chemical, flask, laboratory, toxicant, hazardous substance, reagent, 化学品, 烧瓶 |
| `pill-drug.svg` | pill, drug, pharmaceutical, medication, capsule, 药物, 胶囊 |

### Mechanism and biology

| File | Keywords |
|---|---|
| `dna-helix.svg` | DNA, helix, genotoxicity, genetics, gene, mutation, 基因, DNA损伤 |
| `mitochondria.svg` | mitochondria, mitochondrion, oxidative phosphorylation, energy metabolism, cristae, 线粒体 |
| `ros-radical.svg` | ROS, reactive oxygen species, oxidative stress, free radical, superoxide, 活性氧, 氧化应激 |
| `inflammation-cell.svg` | inflammation, immune cell, macrophage, cytokine, inflammatory response, 炎症, 免疫细胞 |
| `gut-microbiome.svg` | gut microbiome, microbiota, bacteria, dysbiosis, microbial community, 肠道菌群, 细菌 |
| `receptor-ligand.svg` | receptor, ligand, binding, signaling, cell membrane, endocrine disruptor, 受体, 配体 |
| `epigenetic-methyl.svg` | epigenetics, DNA methylation, methyl group, CpG, gene regulation, 表观遗传, 甲基化 |

### Analysis and outcome

| File | Keywords |
|---|---|
| `forest-plot-mini.svg` | forest plot, meta-analysis, confidence interval, effect estimate, odds ratio, hazard ratio, 森林图, 置信区间 |
| `dose-response-curve.svg` | dose-response, sigmoid, EC50, concentration-response, benchmark dose, 剂量效应, 曲线 |
| `map-pin-region.svg` | map, location, region, geographic, study area, spatial, 地图, 区域 |
| `risk-up-arrow.svg` | risk, increase, trend, association, elevated risk, hazard, 风险升高, 上升趋势 |
| `heart-rate-ecg.svg` | heart rate, ECG, cardiovascular outcome, arrhythmia, cardiac function, 心率, 心电图 |

`_contact_sheet.png` is a rendered overview of the whole set (120 px per icon).

# Endoscopic Lesion Localization

The workflow:- https://itbworkflow.vercel.app

Website Interface (Inital Development):-  https://abdtb.vercel.app/

This repository contains documentation and exploratory material for an ongoing **research-oriented project** focused on **detecting and localizing mucosal lesions from colonoscopic and capsule endoscopy images**.

The project is motivated by gastrointestinal conditions such as **intestinal (abdominal) tuberculosis**, where accurate identification of mucosal abnormalities plays a critical role in clinical assessment. The work is framed as a **proof-of-concept study**, emphasizing methodological development and experimental analysis rather than clinical deployment.

---

## 🔬 Problem Statement

Given a collection of colonoscopic and capsule endoscopy images, the objective of this research is to design a learning framework capable of **detecting and localizing mucosal lesions suggestive of intestinal tuberculosis (ITB)**.

The current phase focuses exclusively on **visual lesion localization from endoscopic imagery**, serving as a foundational step toward more comprehensive clinical and multimodal analysis.

---

## 🧠 Project Scope

### Included in the current phase
- Unimodal analysis using endoscopic images  
- Detection and localization of mucosal lesions  
- Visual interpretability of model outputs  

### Out of scope for the current phase
- Multimodal integration (CT enterography, histopathology, clinical text)  
- Differential diagnosis between gastrointestinal conditions  
- Automated clinical reasoning or reporting  
- Claims of diagnostic or clinical performance  

---

## 🧭 Methodological Overview

The proposed workflow involves:
1. Preprocessing and normalization of endoscopic images  
2. Feature extraction using visual representation models  
3. Localization of lesion-relevant regions  
4. Generation of visual explanations highlighting areas of interest  

A detailed description of the workflow and methodology is provided in the `docs/` directory.

---

## 🗂 Repository Structure (Planned)

```text
endoscopic-lesion-localization/
│
├── README.md
├── docs/
│   ├── methodology.md
|   ├── Gantt chart
│   └── workflow.html
│
├── data/
│   └── README.md
│
├── models/
├── experiments/
└── utils/

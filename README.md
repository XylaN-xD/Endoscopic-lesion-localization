# 🔬 Endoscopic Lesion Localization

<div align="center">
  
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=2800&pause=500&color=2F81F7&center=true&vCenter=true&width=600&lines=Gastrointestinal+Imaging+Research;Capsule+Endoscopy+Analysis;Mucosal+Lesion+Detection;Intestinal+Tuberculosis+Study" alt="Typing Animation" />

<div align="center">
  <img src="dna.svg" alt="DNA Animation" />
</div>
   
  <!-- Status Badges -->
  <img src="https://img.shields.io/badge/Phase-Data%20Preparation-2F81F7?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Research%20Prototype-yellow?style=for-the-badge" />
  
  <br>
  <br>

<!-- Links -->
  <table>
    <tr>
      <td align="center"><b>📊 Workflow</b></td>
      <td align="center"><b>💻 Interface</b></td>
    </tr>
    <tr>
      <td align="center"><a href="https://itbworkflow.vercel.app"><img src="https://img.shields.io/badge/View-Workflow-2F81F7?style=flat-square&logo=vercel" /></a></td>
      <td align="center"><a href="https://abdtb.vercel.app/"><img src="https://img.shields.io/badge/View-Interface-2F81F7?style=flat-square&logo=vercel" /></a></td>
    </tr>
  </table>
  
  <br>
  
  <!-- Branches Overview -->
  <details>
    <summary><b>🪾 Repository Current Branches</b></summary>
    <br>
    <table>
      <tr>
        <th>Branch</th>
        <th>Purpose</th>
      </tr>
      <tr>
        <td><code>main</code></td>
        <td>🔜 Stable release (coming soon)</td>
      </tr>
      <tr>
        <td><code>data-preparation</code></td>
        <td>🔵 Active - Dataset creation & annotation</td>
      </tr>
      <tr>
        <td><code>frontend</code></td>
        <td>🟡 In Progress - UI development</td>
      </tr>
    </table>
  </details>
  
</div>

## 📋 Overview
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
data/
│   ├── README.md                    # Dataset overview, source, citation, access
│   ├── metadata.json                # All image metadata in JSON format
│   ├── preprocessing.json           # Preprocessing steps/config in JSON
│   ├── annotation_protocol.json     # Annotation guidelines in JSON
│   └── splits/                      # Train/val/test splits
│       ├── train.txt
│       ├── val.txt
│       └── test.txt
│
├── models/
├── experiments/
└── utils/

# 🧬 Benchmarking Models for Capsule Endoscopy Lesion Detection and Segmentation for Vision LLMs

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&duration=2800&pause=500&color=2F81F7&center=true&vCenter=true&width=640&lines=Gastrointestinal+Imaging+Research;Capsule+Endoscopy+Analysis;Mucosal+Lesion+Detection;Foundation+Model+Benchmarking" alt="Typing animation" />

<br>

<img src="dna.svg" alt="DNA Animation" />

<br><br>

<img src="https://img.shields.io/badge/Phase-Benchmark%20Evaluation-2F81F7?style=for-the-badge" />
&nbsp;
<img src="https://img.shields.io/badge/Status-Research%20Prototype-F5A623?style=for-the-badge" />
&nbsp;


<br><br>

<table>
  <tr>
    <td align="center"><b>📊 Workflow</b></td>
    <td align="center"><b>💻 Interface</b></td>
    <td align="center"><b>💾 Data Archive</b></td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://itbworkflow.vercel.app">
        <img src="https://img.shields.io/badge/View-Workflow-2F81F7?style=flat-square&logo=vercel" />
      </a>
    </td>
    <td align="center">
      <a href="https://abdtb.vercel.app/">
        <img src="https://img.shields.io/badge/View-Interface-2F81F7?style=flat-square&logo=vercel" />
      </a>
    </td>
    <td align="center">
      <a href="https://drive.google.com/drive/folders/1XQCivGj5UsD78iUjcUe_vsKN8wfFq5zy?usp=drive_link">
        <img src="https://img.shields.io/badge/Google_Drive-Documentation%20%26%20Dataset-4285F4?style=flat-square&logo=google-drive" />
      </a>
    </td>
  </tr>
</table>

<details>
<summary><b>🌿 Repository Branches</b></summary>
<br>

| Branch | Purpose |
|---|---|
| `main` | Documentation & entry point |
| `data-preparation` | Full pipeline — data, models, MedSAM, evaluation |
| `frontend` | UI & visualization |

</details>

</div>

---

## 👥 Authors & Mentor

<div align="center">

<table>
  <tr>
    <th align="center" width="160">Role</th>
    <th align="center" width="260">Name</th>
    <th align="center">Affiliation</th>
  </tr>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Author-2F81F7?style=flat-square" />
    </td>
    <td align="center"><b>Ishan Jha</b></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Author-2F81F7?style=flat-square" />
    </td>
    <td align="center"><b>Neil Lohit Bose</b></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Mentor-6C3FC4?style=flat-square" />
    </td>
    <td align="center"><b>Dr. Sujoy K Biswas</b></td>
    <td align="center">IDEAS — ISI Kolkata</td>
  </tr>
</table>
> *This research was conducted under the mentorship of **Dr. Sujoy K Biswas** at the IDEAS, Indian Statistical Institute Kolkata.*

</div>

---

## 📋 Overview

This repository presents a **research-grade evaluation pipeline** for automated lesion detection and segmentation in capsule endoscopy, leveraging the large-scale **Kvasir-Capsule dataset**.

The central contribution is a systematic **zero-shot benchmark** of state-of-the-art foundation models — CLIP, BLIP-2, LLaVA, and MedSAM — probing their ability to generalize to a specialized, low-contrast medical imaging domain without any domain-specific fine-tuning.

---

## 🔬 Problem Statement

Capsule endoscopy procedures routinely produce **4–8 hours of video footage** (~4.7 million frames per study), making exhaustive manual review by clinicians both time-consuming and susceptible to human error.

> **Core research question:** *Can large pretrained vision-language foundation models generalize to capsule endoscopy without domain-specific training?*

---

## 🧠 Project Scope

### ✅ In Scope

- Endoscopic image analysis (capsule endoscopy)
- Lesion localization via bounding boxes and segmentation masks
- Zero-shot evaluation of foundation models
- Quantitative benchmarking (IoU, Dice, Precision, Recall, F1)

### ❌ Out of Scope

- Clinical diagnosis or patient-level decision making
- Multimodal or longitudinal patient data
- Automated medical reporting systems

---

## 🧭 Methodology

### Stage 1–2 · Data Preparation

- Metadata parsing → bounding box extraction (4-point → `x1,y1,x2,y2`)
- OpenCV-based video splitting pipeline
- Source: 117 videos → 85 annotated clips selected
- Final corpus: **1,862 annotated frames** across 4 lesion classes

### Stage 3–4 · Assembly & Validation

- Clip generation with frame-level annotation alignment
- Random baseline construction for sanity verification
- Evaluation metrics defined: IoU, Dice, Precision, Recall, F1

### Stage 5–6 · Model Evaluation

- **CLIP / BLIP-2 / LLaVA 1.5** evaluated on stratified image samples
- **MedSAM** run with ground-truth bounding box prompts (upper-bound segmentation setting)
- Full segmentation mask generation across the annotated dataset
- Comparative benchmark against random and prior baselines

---

## 🔄 Pipeline

```
metadata.json
    └── bounding box extraction
            └── frame extraction (OpenCV)
                    └── MedSAM inference (GT-prompted)
                            └── segmentation masks
                                    └── IoU / Dice / F1 evaluation
                                            └── benchmark comparison
```

---

## 🖼️ Visual Workflow

Full interactive pipeline diagram: 👉 [itbworkflow.vercel.app](https://itbworkflow.vercel.app)

---

## 📊 Dataset

### Corpus Overview

| Metric | Value |
|---|---|
| Total videos in dataset | 117 |
| Total frames | 4.7M+ |
| Lesion classes | 14 |
| Clips used in evaluation | 85 |
| Annotated frames used | 1,862 |

### Evaluated Class Breakdown

| Class | Clips | Frames |
|---|---|---|
| Ulcer | 29 | 782 |
| Erosion | 46 | 397 |
| Blood-fresh | 9 | 446 |
| Polyp | 1 | 52 |

> Dataset source: [Kvasir-Capsule](https://datasets.simula.no/kvasir-capsule/) — Simula Research Laboratory.

---

## 🧪 Models Evaluated

| Model | Type | Setting |
|---|---|---|
| [CLIP](https://github.com/openai/CLIP) | Vision-language | Zero-shot classification |
| [BLIP-2](https://github.com/salesforce/LAVIS) | Vision-language | Zero-shot VQA |
| [LLaVA 1.5](https://github.com/haotian-liu/LLaVA) | Multimodal LLM | Zero-shot VQA |
| [MedSAM](https://github.com/bowang-lab/MedSAM) | Medical segmentation | GT-prompted segmentation |

---

## 📊 Results

### Vision-Language Model Performance

| Model | Accuracy | Notes |
|---|---|---|
| CLIP | 30% | Majority-class bias; no genuine lesion understanding |
| BLIP-2 | 0% | Systematic hallucination; entirely misaligned |
| LLaVA 1.5 | Partial | Some semantic understanding; inconsistent localization |

### MedSAM Segmentation Metrics

| Metric | Value |
|---|---|
| Mean IoU | **0.5101** |
| Mean Dice | **0.6152** |
| Micro Precision | 0.8857 |
| Micro Recall | 0.0998 |
| Micro F1 | 0.1795 |

> **Note:** MedSAM was evaluated in a privileged setting using ground-truth bounding box prompts. Despite this, recall remains critically low — indicating severe domain mismatch rather than a localization failure.

---

## 📉 Key Findings

1. **Persistent domain gap** — All evaluated foundation models exhibit a substantial performance drop on capsule endoscopy imagery, reflecting the distributional distance between internet-scale pretraining data and narrow medical imaging domains.

2. **High-precision, low-recall failure mode** — MedSAM achieves reasonable mask quality when prompted, but misses approximately **90% of true lesion instances**, producing a micro recall of ~0.10.

3. **Blood class completely undetected** — Fresh blood findings yielded **zero detections** across all models, likely due to severe underrepresentation in pretraining corpora.

4. **Zero-shot is not sufficient** — Supervised CNNs fine-tuned on Kvasir-Capsule substantially outperform all zero-shot foundation models, underscoring the necessity of domain adaptation.

---

## 🖼️ Sample Outputs

| Class | Sample |
|---|---|
| Ulcer | `[PLACEHOLDER: ulcer_sample.png]` |
| Erosion | `[PLACEHOLDER: erosion_sample.png]` |
| Blood-fresh | `[PLACEHOLDER: blood_sample.png]` |
| Polyp | `[PLACEHOLDER: polyp_sample.png]` |

---

## 🗂 Repository Structure

### `main` branch

```
endoscopic-lesion-localization/
├── README.md
├── dna.svg
└── Docs/
    └── methodology, presentation, workflow
```

> Sub-directories `data prep/`, `evaluation/`, `medsam/`, and `models/` exist as cross-branch reference stubs.

### `data-preparation` branch

```
data-preparation/
├── data prep/
│   ├── Datasort_script.py
│   ├── build_ground_truth.py
│   └── data_prep.ipynb
├── evaluation/
│   ├── Evaluation.ipynb
│   ├── evaluate.py
│   ├── baseline_results.json
│   └── ground_truth.json
├── medsam/
│   ├── Medsam_combined.ipynb
│   ├── run_medsam.py
│   ├── evaluate_medsam.py
│   ├── complete_matrics.py
│   └── medsam_complete_metrics.json
└── models/
    ├── Testing_of_the_shelf_models.ipynb
    └── test_models.py
```

### `frontend` branch

```
frontend/
├── README.md
├── dna.svg
├── Docs/
├── Streamlit/
│   └── app.py
└── Frontend-ui/
```

---

## 🚀 Quickstart

```bash
# Step 1: Build ground truth annotations
python build_ground_truth.py

# Step 2: Run model evaluations
python evaluate.py

# Step 3: Compute full MedSAM metrics
python complete_metrics.py
```

---

## 🔮 Future Work

- [ ] **Domain fine-tuning** — Supervised fine-tuning of MedSAM on Kvasir-Capsule training split
- [ ] **Full class coverage** — Extend evaluation pipeline to all 14 annotated lesion classes
- [ ] **Temporal modeling** — Exploit frame-level continuity in capsule video sequences
- [ ] **LLaVA full evaluation** — Complete evaluation pass of LLaVA 1.5 on the full annotated corpus
- [ ] **Prompt sensitivity analysis** — Ablation over MedSAM bounding box prompt quality vs. segmentation performance

---

## 📚 References

- Pogorelov et al. (2017). *Kvasir: A Multi-Class Image Dataset for Computer-Aided Gastrointestinal Disease Detection.* MMSys.
- Ma et al. (2023). *Segment Anything in Medical Images.* arXiv:2304.12306.
- Radford et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision.* ICML.
- Li et al. (2023). *BLIP-2: Bootstrapping Language-Image Pre-training.* ICML.
- Liu et al. (2023). *Visual Instruction Tuning (LLaVA).* NeurIPS.

---

## 🙌 Acknowledgements

This work was conducted at **IDEAS — Indian Statistical Institute Kolkata**, under the mentorship of **Dr. Sujoy K Biswas**. The authors gratefully acknowledge the Simula Research Laboratory for making the Kvasir-Capsule dataset publicly available.

---

<div align="center">
  <sub>Ishan Jha · Neil Lohit Bose &nbsp;|&nbsp; Mentor: Dr. Sujoy K Biswas &nbsp;|&nbsp; IDEAS, ISI Kolkata</sub>
</div>

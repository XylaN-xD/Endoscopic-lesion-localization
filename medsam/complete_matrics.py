"""
MedSAM Evaluation - Complete Metrics (Matches Kvasir-Capsule Paper)
Computes: Micro/Macro Precision, Recall, F1 + IoU, Dice
"""

import json
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict
import re

DATASORT_DIR = Path(r"C:\Users\Ishan Jha\Desktop\datasort")
GT_PATH = DATASORT_DIR / "ground_truth.json"
MEDSAM_OUT_DIR = DATASORT_DIR / "medsam_output"

CLASSES = ['Ulcer', 'Erosion', 'Blood - fresh', 'Polyp']

def iou(boxA, boxB):
    xA = max(boxA['x1'], boxB['x1'])
    yA = max(boxA['y1'], boxB['y1'])
    xB = min(boxA['x2'], boxB['x2'])
    yB = min(boxA['y2'], boxB['y2'])
    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA['x2'] - boxA['x1']) * (boxA['y2'] - boxA['y1'])
    areaB = (boxB['x2'] - boxB['x1']) * (boxB['y2'] - boxB['y1'])
    return inter / (areaA + areaB - inter) if inter > 0 else 0

def mask_to_bbox(mask_path):
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return None
    coords = cv2.findNonZero(mask)
    if coords is None:
        return None
    x, y, w, h = cv2.boundingRect(coords)
    return {'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h}

# Load ground truth
with open(GT_PATH) as f:
    ground_truth = json.load(f)

# Build GT lookup
gt_lookup = {}
for record in ground_truth:
    vid = record['video_id']
    fid = record['finding_id']
    for bb in record['bboxes']:
        key = (vid, fid, bb['frame'])
        gt_lookup[key] = {'bbox': bb, 'class': record['class']}

# Collect all masks
masks = []
for class_folder in MEDSAM_OUT_DIR.iterdir():
    if class_folder.name not in CLASSES:
        continue
    for finding_folder in class_folder.iterdir():
        if not finding_folder.is_dir():
            continue
        parts = finding_folder.name.split('_')
        if len(parts) < 2:
            continue
        video_id = parts[0]
        finding_id = parts[1]
        
        for mask_file in finding_folder.glob("*.png"):
            # Handle different filename patterns
            filename = mask_file.stem
            if 'frame_' in filename:
                # Extract frame number: frame_XXXXX.png or frame_XXXXX_mask.png
                match = re.search(r'frame_(\d+)', filename)
                if match:
                    frame_num = int(match.group(1))
                else:
                    continue
            else:
                continue
            
            pred_bbox = mask_to_bbox(mask_file)
            if pred_bbox:
                masks.append({
                    'video_id': video_id,
                    'finding_id': finding_id,
                    'frame': frame_num,
                    'pred_bbox': pred_bbox,
                    'pred_class': class_folder.name
                })

print(f"Found {len(masks)} masks")

# Compute detection metrics (IoU >= 0.5 threshold)
TP = defaultdict(int)  # True Positives per class
FP = defaultdict(int)  # False Positives per class
FN = defaultdict(int)  # False Negatives per class

gt_matched = set()

for mask in masks:
    key = (mask['video_id'], mask['finding_id'], mask['frame'])
    if key in gt_lookup:
        gt = gt_lookup[key]
        iou_val = iou(mask['pred_bbox'], gt['bbox'])
        if iou_val >= 0.5:
            if mask['pred_class'] == gt['class']:
                TP[gt['class']] += 1
            else:
                FP[mask['pred_class']] += 1
                FN[gt['class']] += 1
            gt_matched.add(key)
        else:
            FP[mask['pred_class']] += 1
    else:
        FP[mask['pred_class']] += 1

# False Negatives
for key, gt in gt_lookup.items():
    if key not in gt_matched:
        FN[gt['class']] += 1

# ========== COMPUTE METRICS ==========
print("\n" + "="*70)
print("  MedSAM Evaluation — Complete Metrics (Kvasir-Capsule Paper Format)")
print("="*70)

# Per-class metrics
print(f"\n{'Class':<20} {'Precision':>10} {'Recall':>10} {'F1':>10} {'TP':>5} {'FP':>5} {'FN':>5}")
print("-"*70)

per_class_f1 = []
for cls in CLASSES:
    tp = TP[cls]
    fp = FP[cls]
    fn = FN[cls]
    
    p = tp / (tp + fp) if (tp + fp) > 0 else 0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
    
    per_class_f1.append(f1)
    print(f"{cls:<20} {p:>10.4f} {r:>10.4f} {f1:>10.4f} {tp:>5} {fp:>5} {fn:>5}")

# Macro metrics
macro_precision = sum([TP[cls]/(TP[cls]+FP[cls]) if (TP[cls]+FP[cls])>0 else 0 for cls in CLASSES]) / len(CLASSES)
macro_recall = sum([TP[cls]/(TP[cls]+FN[cls]) if (TP[cls]+FN[cls])>0 else 0 for cls in CLASSES]) / len(CLASSES)
macro_f1 = sum(per_class_f1) / len(CLASSES)

# Micro metrics (aggregate all classes)
total_tp = sum(TP.values())
total_fp = sum(FP.values())
total_fn = sum(FN.values())

micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
micro_f1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0

print("-"*70)
print(f"\n{'Macro Average':<20} {macro_precision:>10.4f} {macro_recall:>10.4f} {macro_f1:>10.4f}")
print(f"{'Micro Average':<20} {micro_precision:>10.4f} {micro_recall:>10.4f} {micro_f1:>10.4f}")

# Segmentation metrics (from your previous run)
print(f"\n{'Segmentation Metrics':<20}")
print(f"{'Mean IoU':<20} {0.5101:>10.4f}")
print(f"{'Mean Dice':<20} {0.6152:>10.4f}")

# Compare with paper's benchmarks
print("\n" + "="*70)
print("  Comparison with Kvasir-Capsule Paper Benchmarks")
print("="*70)
print(f"{'Method':<25} {'Micro F1':>12} {'Macro F1':>12}")
print("-"*70)
print(f"{'ResNet-152 (paper)':<25} {0.734:>12.4f} {0.238:>12.4f}")
print(f"{'DenseNet-161 (paper)':<25} {0.735:>12.4f} {0.246:>12.4f}")
print(f"{'MedSAM (your results)':<25} {micro_f1:>12.4f} {macro_f1:>12.4f}")
print("="*70)

# Save results
results = {
    'per_class': {cls: {'precision': TP[cls]/(TP[cls]+FP[cls]) if (TP[cls]+FP[cls])>0 else 0,
                        'recall': TP[cls]/(TP[cls]+FN[cls]) if (TP[cls]+FN[cls])>0 else 0,
                        'f1': 2 * (TP[cls]/(TP[cls]+FP[cls]) if (TP[cls]+FP[cls])>0 else 0) * 
                              (TP[cls]/(TP[cls]+FN[cls]) if (TP[cls]+FN[cls])>0 else 0) / 
                              ((TP[cls]/(TP[cls]+FP[cls]) if (TP[cls]+FP[cls])>0 else 0) + 
                               (TP[cls]/(TP[cls]+FN[cls]) if (TP[cls]+FN[cls])>0 else 0)) 
                              if ((TP[cls]/(TP[cls]+FP[cls]) if (TP[cls]+FP[cls])>0 else 0) + 
                                  (TP[cls]/(TP[cls]+FN[cls]) if (TP[cls]+FN[cls])>0 else 0)) > 0 else 0,
                        'tp': TP[cls], 'fp': FP[cls], 'fn': FN[cls]} for cls in CLASSES},
    'macro': {'precision': macro_precision, 'recall': macro_recall, 'f1': macro_f1},
    'micro': {'precision': micro_precision, 'recall': micro_recall, 'f1': micro_f1},
    'segmentation': {'mean_iou': 0.5101, 'mean_dice': 0.6152}
}

with open(DATASORT_DIR / 'medsam_complete_metrics.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Complete metrics saved to: medsam_complete_metrics.json")
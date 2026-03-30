"""
MedSAM Evaluation Script (masks already generated)
====================================================
Reads existing masks from medsam_output/,
compares with ground_truth.json, computes metrics.

USAGE:
    python evaluate_medsam.py
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATASORT_DIR   = r"C:\Users\Ishan Jha\Desktop\datasort"
GT_PATH        = os.path.join(DATASORT_DIR, "ground_truth.json")
MEDSAM_OUT_DIR = os.path.join(DATASORT_DIR, "medsam_output")
RESULTS_PATH   = os.path.join(DATASORT_DIR, "medsam_results.json")

CLASSES = ['Ulcer', 'Erosion', 'Blood - fresh', 'Polyp']

LABEL_FOLDER_MAP = {
    "Ulcer":         "Ulcer",
    "Erosion":       "Erosion",
    "Polyp":         "Polyp",
    "Blood - fresh": "Blood_fresh",
}
# ──────────────────────────────────────────────────────────────────────────────


def mask_to_bbox(mask_path):
    """Read mask PNG and convert to bbox dict {x1,y1,x2,y2}."""
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return None, None
    coords = cv2.findNonZero(mask)
    if coords is None:
        return None, mask.shape  # empty mask
    x, y, w, h = cv2.boundingRect(coords)
    return {'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h}, mask.shape


def iou_bbox(boxA, boxB):
    """IoU between two bbox dicts."""
    xA = max(boxA['x1'], boxB['x1'])
    yA = max(boxA['y1'], boxB['y1'])
    xB = min(boxA['x2'], boxB['x2'])
    yB = min(boxA['y2'], boxB['y2'])
    inter = max(0, xB - xA) * max(0, yB - yA)
    if inter == 0:
        return 0.0
    areaA = (boxA['x2'] - boxA['x1']) * (boxA['y2'] - boxA['y1'])
    areaB = (boxB['x2'] - boxB['x1']) * (boxB['y2'] - boxB['y1'])
    return inter / (areaA + areaB - inter)


def iou_mask(mask_path, gt_bbox):
    """
    Compute IoU directly between the PNG mask and the GT bbox rasterized as mask.
    More accurate than bbox-to-bbox IoU.
    """
    pred_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if pred_mask is None:
        return 0.0

    H, W = pred_mask.shape
    gt_mask = np.zeros((H, W), dtype=np.uint8)
    x1 = max(0, gt_bbox['x1'])
    y1 = max(0, gt_bbox['y1'])
    x2 = min(W, gt_bbox['x2'])
    y2 = min(H, gt_bbox['y2'])
    cv2.rectangle(gt_mask, (x1, y1), (x2, y2), 255, -1)

    pred_bin = (pred_mask > 127).astype(np.uint8)
    gt_bin   = (gt_mask   > 127).astype(np.uint8)

    intersection = np.logical_and(pred_bin, gt_bin).sum()
    union        = np.logical_or(pred_bin,  gt_bin).sum()
    return float(intersection / union) if union > 0 else 0.0


def dice_mask(mask_path, gt_bbox):
    """Compute Dice score between pred mask and GT bbox mask."""
    pred_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if pred_mask is None:
        return 0.0

    H, W = pred_mask.shape
    gt_mask = np.zeros((H, W), dtype=np.uint8)
    cv2.rectangle(gt_mask,
                  (gt_bbox['x1'], gt_bbox['y1']),
                  (gt_bbox['x2'], gt_bbox['y2']), 255, -1)

    pred_bin = (pred_mask > 127).astype(np.uint8)
    gt_bin   = (gt_mask   > 127).astype(np.uint8)

    intersection = np.logical_and(pred_bin, gt_bin).sum()
    total = pred_bin.sum() + gt_bin.sum()
    return float(2 * intersection / total) if total > 0 else 0.0


def evaluate(predictions, ground_truth):
    """Compute per-class and overall metrics."""
    gt_by_clip = {r['clip']: r for r in ground_truth}

    class_tp   = defaultdict(int)
    class_fp   = defaultdict(int)
    class_fn   = defaultdict(int)
    iou_scores  = []
    dice_scores = []

    for pred in predictions:
        clip  = pred['clip']
        p_cls = pred['class']
        p_box = pred.get('bbox')

        if clip not in gt_by_clip:
            class_fp[p_cls] += 1
            continue

        gt     = gt_by_clip[clip]
        gt_cls = gt['class']

        if p_cls == gt_cls:
            class_tp[p_cls] += 1
        else:
            class_fp[p_cls] += 1
            class_fn[gt_cls] += 1

        if p_box and gt['bboxes']:
            best_iou  = max(iou_bbox(p_box, b) for b in gt['bboxes'])
            iou_scores.append(best_iou)

        # Mask-level IoU and Dice (more meaningful)
        for mask_path, gt_bbox in pred.get('frame_evals', []):
            iou_scores.append(iou_mask(mask_path, gt_bbox))
            dice_scores.append(dice_mask(mask_path, gt_bbox))

    predicted_clips = {p['clip'] for p in predictions}
    for r in ground_truth:
        if r['clip'] not in predicted_clips:
            class_fn[r['class']] += 1

    results = {}
    for cls in CLASSES:
        tp = class_tp[cls]
        fp = class_fp[cls]
        fn = class_fn[cls]
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0.0)
        results[cls] = {
            'precision': round(precision, 4),
            'recall':    round(recall,    4),
            'f1':        round(f1,        4),
            'tp': tp, 'fp': fp, 'fn': fn,
        }

    total_tp = sum(class_tp.values())
    total_fp = sum(class_fp.values())
    total_fn = sum(class_fn.values())
    op  = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    or_ = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    of1 = (2 * op * or_ / (op + or_)) if (op + or_) > 0 else 0.0

    results['overall'] = {
        'precision': round(op,  4),
        'recall':    round(or_, 4),
        'f1':        round(of1, 4),
        'mean_iou':  round(sum(iou_scores)  / len(iou_scores)  if iou_scores  else 0.0, 4),
        'mean_dice': round(sum(dice_scores) / len(dice_scores) if dice_scores else 0.0, 4),
    }
    return results


def print_results(results):
    print(f'\n{"="*65}')
    print(f'  MedSAM — Evaluation Results')
    print(f'{"="*65}')
    print(f'{"Class":<20} {"Precision":>10} {"Recall":>10} {"F1":>10}')
    print(f'{"-"*65}')
    for cls in CLASSES:
        r = results[cls]
        print(f'{cls:<20} {r["precision"]:>10.4f} '
              f'{r["recall"]:>10.4f} {r["f1"]:>10.4f}  '
              f'(TP={r["tp"]} FP={r["fp"]} FN={r["fn"]})')
    print(f'{"-"*65}')
    ov = results['overall']
    print(f'{"Overall":<20} {ov["precision"]:>10.4f} '
          f'{ov["recall"]:>10.4f} {ov["f1"]:>10.4f}')
    print(f'{"Mean IoU":<20} {ov["mean_iou"]:>10.4f}')
    print(f'{"Mean Dice":<20} {ov["mean_dice"]:>10.4f}')
    print(f'{"="*65}')

    # Compare vs random baseline
    baseline = {
        'precision': 0.3412, 'recall': 0.3412,
        'f1': 0.3412, 'mean_iou': 0.074
    }
    print(f'\n  vs Random Baseline:')
    print(f'{"─"*65}')
    for metric in ['precision', 'recall', 'f1', 'mean_iou']:
        val = ov.get(metric, 0)
        base = baseline[metric]
        delta = val - base
        arrow = '▲' if delta >= 0 else '▼'
        print(f'  {metric:<14} baseline={base:.4f}  '
              f'MedSAM={val:.4f}  {arrow}{abs(delta):.4f}')
    print(f'{"─"*65}\n')


def main():
    print("=" * 65)
    print("  MedSAM Evaluation — Reading existing masks")
    print("=" * 65)

    # Load ground truth
    print("\n[1/3] Loading ground truth...")
    with open(GT_PATH, encoding='utf-8') as f:
        ground_truth = json.load(f)
    gt_by_clip = {r['clip']: r for r in ground_truth}
    print(f"  {len(ground_truth)} clips in ground truth")

    # Build GT frame lookup: (video_id, finding_id, frame_num) → gt_bbox
    gt_frame_lookup = {}
    for record in ground_truth:
        vid   = record['video_id']
        fid   = record['finding_id']
        for bb in record['bboxes']:
            key = (vid, fid, bb['frame'])
            gt_frame_lookup[key] = {k: bb[k] for k in ['x1','y1','x2','y2']}

    # Read masks from medsam_output/
    print("\n[2/3] Reading MedSAM masks...")
    predictions = []
    total_masks = 0
    matched_masks = 0
    skipped = 0

    for label, folder_name in LABEL_FOLDER_MAP.items():
        label_dir = os.path.join(MEDSAM_OUT_DIR, folder_name)
        if not os.path.exists(label_dir):
            print(f"  [SKIP] Folder not found: {label_dir}")
            continue

        for finding_folder in sorted(os.listdir(label_dir)):
            finding_path = os.path.join(label_dir, finding_folder)
            if not os.path.isdir(finding_path):
                continue

            # Parse video_id and finding_id from folder name
            # Format: {video_id}_{finding_id}
            parts = finding_folder.split('_')
            if len(parts) < 2:
                continue
            video_id   = parts[0]
            finding_id = parts[1]

            # Find matching clip name in ground truth
            clip_name = None
            pred_bbox = None
            frame_evals = []

            for record in ground_truth:
                if (record['video_id'] == video_id and
                        record['finding_id'] == finding_id):
                    clip_name = record['clip']
                    break

            if not clip_name:
                print(f"  [SKIP] No GT match for {finding_folder}")
                skipped += 1
                continue

            # Read all mask files in this folder
            mask_files = sorted([
                f for f in os.listdir(finding_path)
                if f.endswith('_mask.png')
            ])

            for mask_file in mask_files:
                total_masks += 1
                # Parse frame number from filename: frame_XXXX_mask.png
                try:
                    frame_num = int(mask_file.replace('frame_', '').replace('_mask.png', ''))
                except ValueError:
                    continue

                mask_path = os.path.join(finding_path, mask_file)
                pred_box, shape = mask_to_bbox(mask_path)

                # Get GT bbox for this frame
                gt_bbox = gt_frame_lookup.get((video_id, finding_id, frame_num))
                if gt_bbox is None:
                    # Try finding closest frame in GT
                    gt_record = gt_by_clip.get(clip_name)
                    if gt_record and gt_record['bboxes']:
                        gt_bbox = gt_record['bboxes'][0]  # use first bbox

                if gt_bbox:
                    frame_evals.append((mask_path, gt_bbox))
                    matched_masks += 1

                if pred_box and pred_bbox is None:
                    pred_bbox = pred_box

            predictions.append({
                'clip':        clip_name,
                'class':       label,
                'bbox':        pred_bbox,
                'frame_evals': frame_evals,
                'n_masks':     len(mask_files),
            })

            print(f"  ✓ {finding_folder} ({label}) — "
                  f"{len(mask_files)} masks, {len(frame_evals)} matched to GT")

    print(f"\n  Total masks read:    {total_masks}")
    print(f"  Matched to GT:       {matched_masks}")
    print(f"  Skipped (no GT):     {skipped}")
    print(f"  Clips to evaluate:   {len(predictions)}")

    # Evaluate
    print("\n[3/3] Computing metrics...")
    results = evaluate(predictions, ground_truth)
    print_results(results)

    # Save
    with open(RESULTS_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == '__main__':
    main()
import json
import random
from pathlib import Path
from collections import defaultdict


BASE_DIR = Path(__file__).parent
GT_PATH  = BASE_DIR / 'ground_truth.json'

CLASSES = ['Ulcer', 'Erosion', 'Blood - fresh', 'Polyp']


# ────────────── Evaluation Metrics  ────────────────
def iou(boxA, boxB):
    """Compute IoU between two boxes (x1,y1,x2,y2)."""
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

def evaluate(predictions, ground_truth, iou_threshold=0.5):
    gt_by_clip = {r['clip']: r for r in ground_truth}

    class_tp = defaultdict(int)
    class_fp = defaultdict(int)
    class_fn = defaultdict(int)
    iou_scores = []

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

        # Detection check (IoU against all GT boxes for this clip)
        if p_box and gt['bboxes']:
            best_iou = max(iou(p_box, b) for b in gt['bboxes'])
            iou_scores.append(best_iou)

    # Clips with no prediction
    predicted_clips = {p['clip'] for p in predictions}
    for r in ground_truth:
        if r['clip'] not in predicted_clips:
            class_fn[r['class']] += 1

    # Compute precision, recall, F1 per class
    results = {}
    for cls in CLASSES:
        tp = class_tp[cls]
        fp = class_fp[cls]
        fn = class_fn[cls]

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1        = (2 * precision * recall / (precision + recall)
                     if (precision + recall) > 0 else 0.0)

        results[cls] = {
            'precision': round(precision, 4),
            'recall':    round(recall, 4),
            'f1':        round(f1, 4),
            'tp': tp, 'fp': fp, 'fn': fn
        }

    # Overall metrics
    total_tp = sum(class_tp.values())
    total_fp = sum(class_fp.values())
    total_fn = sum(class_fn.values())
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall    = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1        = (2 * overall_precision * overall_recall /
                         (overall_precision + overall_recall)
                         if (overall_precision + overall_recall) > 0 else 0.0)
    mean_iou          = sum(iou_scores) / len(iou_scores) if iou_scores else 0.0

    results['overall'] = {
        'precision': round(overall_precision, 4),
        'recall':    round(overall_recall, 4),
        'f1':        round(overall_f1, 4),
        'mean_iou':  round(mean_iou, 4),
    }

    return results


def print_results(results, model_name='Model'):
    print(f'\n{"="*50}')
    print(f' {model_name} — Evaluation Results')
    print(f'{"="*50}')
    print(f'{"Class":<20} {"Precision":>10} {"Recall":>10} {"F1":>10}')
    print(f'{"-"*50}')
    for cls in CLASSES:
        r = results[cls]
        print(f'{cls:<20} {r["precision"]:>10.4f} {r["recall"]:>10.4f} {r["f1"]:>10.4f}')
    print(f'{"-"*50}')
    ov = results['overall']
    print(f'{"Overall":<20} {ov["precision"]:>10.4f} {ov["recall"]:>10.4f} {ov["f1"]:>10.4f}')
    print(f'{"Mean IoU":<20} {ov["mean_iou"]:>10.4f}')
    print(f'{"="*50}')


# -x-x-x-x-x-x-x-x-x- Random Baseline Predictor -x-x-x-x-x-x-x-x-x-x
def random_baseline(ground_truth, seed=42):
    """
    Predicts a random class and a random BB (within 336x336 frame)
    for every clip in the ground truth.
    Used to validate the evaluation pipeline.
    """
    random.seed(seed)
    predictions = []

    for record in ground_truth:
        pred_class = random.choice(CLASSES)
        # Random BB within frame (336x336)
        x1 = random.randint(0, 280)
        y1 = random.randint(0, 280)
        x2 = random.randint(x1 + 20, min(x1 + 150, 336))
        y2 = random.randint(y1 + 20, min(y1 + 150, 336))

        predictions.append({
            'clip':  record['clip'],
            'class': pred_class,
            'bbox':  {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        })

    return predictions

def main():
    if not GT_PATH.exists():
        raise FileNotFoundError(
            f'ground_truth.json not found. Run build_ground_truth.py first.'
        )

    with open(GT_PATH, encoding='utf-8') as f:
        ground_truth = json.load(f)

    print(f'Loaded {len(ground_truth)} clips from ground truth.')

    # Run random baseline
    predictions = random_baseline(ground_truth)

    # Evaluate
    results = evaluate(predictions, ground_truth)

    # Print
    print_results(results, model_name='Random Baseline')

    # Save results
    out_path = BASE_DIR / 'baseline_results.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\nResults saved to: {out_path}')

    print('\nNote: Random baseline scores confirm evaluation pipeline is working.')
    print('Any real model should significantly outperform these numbers.')


if __name__ == '__main__':
    main()

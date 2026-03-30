"""
MedSAM runner for Kvasir-Capsule dataset
-----------------------------------------
Reads metadata.json, extracts frames from output clips,
runs MedSAM inference using bounding boxes, saves masks.

SETUP (run once in terminal):
    git clone https://github.com/bowang-lab/MedSAM
    cd MedSAM
    pip install -e .
    # Download checkpoint from:
    # https://drive.google.com/drive/folders/1ETWmi4AiniJeWOt6HAsYgTjYv_fkgzoN
    # Place it at: MedSAM/work_dir/MedSAM/medsam_vit_b.pth

USAGE:
    python run_medsam.py
"""

import os
import json
import cv2
import numpy as np
import torch
from pathlib import Path

# ─── CONFIG ──────────────────────────────────────────────────────────────────
DATASORT_DIR   = r"C:\Users\Ishan Jha\Desktop\datasort"
METADATA_PATH  = os.path.join(DATASORT_DIR, "metadata.json")
CLIPS_DIR      = os.path.join(DATASORT_DIR, "output")
OUTPUT_DIR     = os.path.join(DATASORT_DIR, "medsam_output")
CHECKPOINT     = r"C:\Users\Ishan Jha\MedSAM\work_dir\MedSAM\medsam_vit_b.pth"

TARGET_LABELS  = {"Ulcer", "Blood - fresh", "Polyp", "Erosion"}
MAX_FRAMES_PER_FINDING = 3   # keep small for the demo — change to None for all frames
# ─────────────────────────────────────────────────────────────────────────────


def load_medsam(checkpoint_path):
    """Load MedSAM model."""
    import sys
    medsam_dir = str(Path(checkpoint_path).parents[3])  # MedSAM root
    if medsam_dir not in sys.path:
        sys.path.insert(0, medsam_dir)

    from segment_anything import sam_model_registry
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    medsam_model = sam_model_registry["vit_b"](checkpoint=checkpoint_path)
    medsam_model = medsam_model.to(device)
    medsam_model.eval()
    return medsam_model, device


def shape_to_bbox(shape):
    """Convert 4-point polygon shape to [x_min, y_min, x_max, y_max]."""
    xs = [pt["x"] for pt in shape]
    ys = [pt["y"] for pt in shape]
    return [min(xs), min(ys), max(xs), max(ys)]


def medsam_inference(model, img_embed, box_1024, height, width, device):
    """Run MedSAM decoder given image embedding and scaled box."""
    from segment_anything.utils.transforms import ResizeLongestSide
    box_torch = torch.as_tensor(box_1024, dtype=torch.float, device=device)
    if len(box_torch.shape) == 1:
        box_torch = box_torch.unsqueeze(0).unsqueeze(0)  # (1,1,4)

    sparse_embeddings, dense_embeddings = model.prompt_encoder(
        points=None, boxes=box_torch, masks=None
    )
    low_res_logits, _ = model.mask_decoder(
        image_embeddings=img_embed,
        image_pe=model.prompt_encoder.get_dense_pe(),
        sparse_prompt_embeddings=sparse_embeddings,
        dense_prompt_embeddings=dense_embeddings,
        multimask_output=False,
    )
    low_res_pred = torch.sigmoid(low_res_logits)
    low_res_pred = low_res_pred.squeeze().cpu().numpy()
    medsam_seg = (cv2.resize(low_res_pred, (width, height)) > 0.5).astype(np.uint8) * 255
    return medsam_seg


def process_frame(model, device, frame_bgr, bbox_raw):
    """
    Preprocess a frame and run MedSAM.
    bbox_raw: [x_min, y_min, x_max, y_max] in original pixel coords
    """
    H, W = frame_bgr.shape[:2]
    img_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Resize to 1024x1024 (MedSAM input size)
    img_1024 = cv2.resize(img_rgb, (1024, 1024))
    img_1024 = img_1024 / 255.0
    img_1024 = np.transpose(img_1024, (2, 0, 1))[None].astype(np.float32)
    img_tensor = torch.tensor(img_1024, dtype=torch.float32).to(device)

    # Scale bbox to 1024
    x_min, y_min, x_max, y_max = bbox_raw
    box_1024 = np.array([
        x_min / W * 1024,
        y_min / H * 1024,
        x_max / W * 1024,
        y_max / H * 1024,
    ])

    with torch.no_grad():
        img_embed = model.image_encoder(img_tensor)
        mask = medsam_inference(model, img_embed, box_1024, H, W, device)

    return mask


def overlay_mask(frame_bgr, mask, bbox_raw, label, alpha=0.4):
    """Draw mask overlay + bounding box on frame."""
    overlay = frame_bgr.copy()
    color_map = {
        "Ulcer":        (0, 0, 255),    # red
        "Erosion":      (0, 165, 255),  # orange
        "Polyp":        (0, 255, 0),    # green
        "Blood - fresh":(255, 0, 0),    # blue
    }
    color = color_map.get(label, (255, 255, 0))

    # Mask overlay
    overlay[mask > 0] = color
    result = cv2.addWeighted(frame_bgr, 1 - alpha, overlay, alpha, 0)

    # Bounding box
    x_min, y_min, x_max, y_max = [int(v) for v in bbox_raw]
    cv2.rectangle(result, (x_min, y_min), (x_max, y_max), color, 2)
    cv2.putText(result, label, (x_min, max(y_min - 5, 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return result


def find_clip(clips_dir, video_id, finding_id, label):
    """
    Find the clip file in output/<Label>/ matching video_id and finding_id.
    Filename pattern: {video_id}_{finding_id}_{Label}_no{N}.mp4
    """
    # Map label to folder name
    label_folder_map = {
        "Ulcer":        "Ulcer",
        "Erosion":      "Erosion",
        "Polyp":        "Polyp",
        "Blood - fresh":"Blood_fresh",
    }
    folder = label_folder_map.get(label)
    if not folder:
        return None

    clip_dir = os.path.join(clips_dir, folder)
    if not os.path.exists(clip_dir):
        return None

    for fname in os.listdir(clip_dir):
        if fname.startswith(f"{video_id}_{finding_id}_"):
            return os.path.join(clip_dir, fname)
    return None


def main():
    print("Loading metadata...")
    with open(METADATA_PATH) as f:
        metadata = json.load(f)

    print("Loading MedSAM model...")
    model, device = load_medsam(CHECKPOINT)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_processed = 0

    for video_id, video_data in metadata.items():
        findings = video_data.get("findings", {})
        if not findings:
            continue

        for finding_id, finding in findings.items():
            label = finding["metadata"].get("pillcam_subtype")
            if label not in TARGET_LABELS:
                continue

            frames_data = finding.get("frames", {})
            if not frames_data:
                continue

            # Find matching clip
            clip_path = find_clip(CLIPS_DIR, video_id, finding_id, label)
            if not clip_path:
                print(f"  [SKIP] No clip found for {video_id} finding {finding_id} ({label})")
                continue

            print(f"\nProcessing: {os.path.basename(clip_path)} ({label})")

            # Output folder per finding
            safe_label = label.replace(" ", "_").replace("-", "").replace("__", "_")
            out_folder = os.path.join(OUTPUT_DIR, safe_label, f"{video_id}_{finding_id}")
            os.makedirs(out_folder, exist_ok=True)

            # Sort frame numbers, optionally cap
            frame_numbers = sorted(frames_data.keys(), key=lambda x: int(x))
            if MAX_FRAMES_PER_FINDING:
                frame_numbers = frame_numbers[:MAX_FRAMES_PER_FINDING]

            # Open video
            cap = cv2.VideoCapture(clip_path)
            video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Build frame_number → bbox lookup
            # Clip frames are relative (0-indexed), metadata frames are absolute
            # We'll map by position within the clip
            frame_num_list = sorted(frames_data.keys(), key=lambda x: int(x))
            clip_frame_idx = {fn: i for i, fn in enumerate(frame_num_list)}

            for frame_num in frame_numbers:
                shape = frames_data[frame_num].get("shape")
                if not shape or len(shape) < 4:
                    continue

                bbox = shape_to_bbox(shape)

                # Seek to frame in clip
                seek_idx = clip_frame_idx.get(frame_num, 0)
                cap.set(cv2.CAP_PROP_POS_FRAMES, seek_idx)
                ret, frame = cap.read()
                if not ret:
                    # fallback: try first frame
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
                if not ret:
                    print(f"  [WARN] Could not read frame {frame_num}")
                    continue

                # Run MedSAM
                try:
                    mask = process_frame(model, device, frame, bbox)
                except Exception as e:
                    print(f"  [ERROR] MedSAM failed on frame {frame_num}: {e}")
                    continue

                # Save outputs
                result = overlay_mask(frame, mask, bbox, label)
                out_base = os.path.join(out_folder, f"frame_{frame_num}")
                cv2.imwrite(f"{out_base}_original.jpg", frame)
                cv2.imwrite(f"{out_base}_mask.png", mask)
                cv2.imwrite(f"{out_base}_overlay.jpg", result)

                print(f"  ✓ Frame {frame_num} → saved to {out_folder}")
                total_processed += 1

            cap.release()

    print(f"\n Done! Processed {total_processed} frames.")
    print(f"Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

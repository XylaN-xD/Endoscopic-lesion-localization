"""
Off-the-shelf Vision & Vision-Language Model Testing
Kvasir-Capsule Dataset — 4 Classes
======================================
Tests 3 models from HuggingFace:
    1. CLIP   — zero-shot image classification
    2. BLIP-2 — visual question answering
    3. LLaVA  — vision language model reasoning

Results are saved to results/model_results.json
"""

import json
import random
from pathlib import Path

import torch
from PIL import Image
from transformers import pipeline, CLIPProcessor, CLIPModel
from tqdm import tqdm


# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(r"C:\Users\Ishan Jha\Desktop\Final Dataset")
OUTPUT_DIR  = Path(r"C:\Users\Ishan Jha\Desktop\model_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLASSES = ['ulcer', 'erosion', 'blood fresh', 'polyp']
SAMPLES_PER_CLASS = 10   # test 10 images per class = 40 total

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")

# ── Helpers ───────────────────────────────────────────────────────────────────

def sample_images(base_dir, classes, n=10, seed=42):
    random.seed(seed)
    samples = {}
    for cls in classes:
        images = list((base_dir / cls).glob("*.jpg"))
        images += list((base_dir / cls).glob("*.png"))
        images = random.sample(images, min(n, len(images)))
        samples[cls] = images
    return samples


def save_results(results, name):
    out = OUTPUT_DIR / f"{name}.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {out}")


def print_summary(results, model_name):
    print(f"\n{'='*50}")
    print(f" {model_name} — Summary")
    print(f"{'='*50}")
    correct = sum(1 for r in results if r.get("correct"))
    total   = len(results)
    print(f"Accuracy: {correct}/{total} = {correct/total:.2%}")
    print()
    for cls in CLASSES:
        cls_results = [r for r in results if r["true_class"] == cls]
        cls_correct = sum(1 for r in cls_results if r.get("correct"))
        print(f"  {cls:15s}: {cls_correct}/{len(cls_results)}")
    print(f"{'='*50}")


# ── 1. CLIP — Zero-shot Classification ───────────────────────────────────────

def test_clip(samples):
    print("\n--- Testing CLIP (zero-shot classification) ---")

    model     = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # Text prompts for each class
    text_prompts = [
        "a capsule endoscopy image showing an ulcer",
        "a capsule endoscopy image showing erosion",
        "a capsule endoscopy image showing fresh blood",
        "a capsule endoscopy image showing a polyp",
    ]

    results = []
    for true_cls in tqdm(CLASSES, desc="CLIP"):
        for img_path in samples[true_cls]:
            image  = Image.open(img_path).convert("RGB")
            inputs = processor(text=text_prompts, images=image,
                               return_tensors="pt", padding=True).to(DEVICE)

            with torch.no_grad():
                outputs    = model(**inputs)
                logits     = outputs.logits_per_image
                probs      = logits.softmax(dim=1).squeeze().tolist()

            pred_idx  = probs.index(max(probs))
            pred_cls  = CLASSES[pred_idx]
            correct   = pred_cls == true_cls

            results.append({
                "model":       "CLIP",
                "image":       img_path.name,
                "true_class":  true_cls,
                "pred_class":  pred_cls,
                "correct":     correct,
                "confidence":  round(max(probs), 4),
                "all_probs":   {CLASSES[i]: round(p, 4) for i, p in enumerate(probs)}
            })

    save_results(results, "clip_results")
    print_summary(results, "CLIP")
    return results


# ── 2. BLIP-2 — Visual Question Answering ────────────────────────────────────

def test_blip2(samples):
    print("\n--- Testing BLIP-2 (visual question answering) ---")

    from transformers import BlipProcessor, BlipForQuestionAnswering

    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model     = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base").to(DEVICE)

    questions = [
        "What abnormality is visible in this endoscopy image?",
        "Is there any bleeding visible?",
        "What type of lesion is shown?",
        "Describe what you see in this capsule endoscopy frame.",
    ]

    results = []
    for true_cls in tqdm(CLASSES, desc="BLIP-2"):
        for img_path in samples[true_cls]:
            image   = Image.open(img_path).convert("RGB")
            answers = {}
            for q in questions:
                inputs = processor(image, q, return_tensors="pt").to(DEVICE)
                with torch.no_grad():
                    out = model.generate(**inputs)
                answers[q] = processor.decode(out[0], skip_special_tokens=True)

            results.append({
                "model":      "BLIP-2",
                "image":      img_path.name,
                "true_class": true_cls,
                "answers":    answers,
            })

    save_results(results, "blip2_results")

    print("\nSample BLIP-2 outputs:")
    for r in results[:4]:
        print(f"\n  [{r['true_class']}] {r['image']}")
        for q, a in r["answers"].items():
            print(f"    Q: {q}")
            print(f"    A: {a}")

    return results


# ── 3. LLaVA — Vision Language Model ─────────────────────────────────────────

def test_llava(samples):
    print("\n--- Testing LLaVA (vision language model) ---")

    try:
        llava = pipeline(
            "image-text-to-text",
            model="llava-hf/llava-1.5-7b-hf",
            device_map="auto",
            torch_dtype=torch.float16
        )
    except Exception as e:
        print(f"LLaVA load failed: {e}")
        print("Skipping LLaVA — requires ~14GB VRAM. Consider running on Colab.")
        return []

    prompt = (
        "USER: <image>\n"
        "This is a capsule endoscopy frame. "
        "Identify if it shows any of the following: ulcer, erosion, fresh blood, polyp, or normal mucosa. "
        "Explain your reasoning.\nASSISTANT:"
    )

    results = []
    for true_cls in tqdm(CLASSES, desc="LLaVA"):
        for img_path in samples[true_cls][:5]:   # only 5 per class for LLaVA (slow)
            image = Image.open(img_path).convert("RGB")
            try:
                out      = llava(image, text=prompt, max_new_tokens=200)
                response = out[0]["generated_text"]
            except Exception as e:
                response = f"Error: {e}"

            results.append({
                "model":      "LLaVA",
                "image":      img_path.name,
                "true_class": true_cls,
                "response":   response,
            })

    save_results(results, "llava_results")

    print("\nSample LLaVA outputs:")
    for r in results[:3]:
        print(f"\n  [{r['true_class']}] {r['image']}")
        print(f"  Response: {r['response'][:300]}...")

    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading image samples...")
    samples = sample_images(BASE_DIR, CLASSES, n=SAMPLES_PER_CLASS)
    for cls, imgs in samples.items():
        print(f"  {cls}: {len(imgs)} images sampled")

    # Run tests
    clip_results  = test_clip(samples)
    blip2_results = test_blip2(samples)
    llava_results = test_llava(samples)

    # Combined summary
    summary = {
        "total_images_tested": SAMPLES_PER_CLASS * len(CLASSES),
        "device": DEVICE,
        "clip": {
            "accuracy": sum(1 for r in clip_results if r["correct"]) / len(clip_results)
            if clip_results else 0
        },
        "blip2": {"samples": len(blip2_results)},
        "llava": {"samples": len(llava_results)},
    }

    save_results(summary, "summary")
    print("\nAll tests complete. Results saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

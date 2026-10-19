import argparse
import numpy as np

R = 2  # radius: 5x5 -> 2


def box_blur_5x5(img: np.ndarray) -> np.ndarray:
    """5x5 box blur, same edge-padded shifted-views arithmetic as filter_ref.py."""
    padded = np.pad(img.astype(np.float64), pad_width=R, mode="edge")
    acc = np.zeros_like(img, dtype=np.float64)
    h, w = img.shape
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            acc += padded[R + dy: R + dy + h, R + dx: R + dx + w]
    acc /= float((2 * R + 1) ** 2)   # 25.0
    return np.clip(acc, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in-prefix", type=str, default="test_image")
    ap.add_argument("--out-prefix", type=str, default="test_image_filtered_serial5")
    args = ap.parse_args()

    img = np.load(f"{args.in_prefix}.npy")
    np.save(f"{args.out_prefix}.npy", box_blur_5x5(img))
    print(f"5x5 serial reference written: {args.out_prefix}.npy")


if __name__ == "__main__":
    main()
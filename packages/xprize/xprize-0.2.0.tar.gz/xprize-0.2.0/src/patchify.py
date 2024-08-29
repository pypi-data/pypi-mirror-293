import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from tqdm import tqdm

from src.utils import f2s, mahalanobis_distance_2d, split_sort, timer

Image.MAX_IMAGE_PIXELS = None


def process_image(imgf, dstep):
    array = cv2.imread(str(imgf))
    array = cv2.resize(array, (dstep, dstep), interpolation=cv2.INTER_AREA)
    col, row = get_patch_position(imgf)
    row *= dstep
    col *= dstep
    return array, col, row


def make_collage(
    patch_dir: Path,
    collage_path: Path,
    step: int,
    downscale_factor: int,
) -> None:
    max_col, max_row = find_max_col_row(patch_dir)
    dstep = step // downscale_factor
    max_row *= dstep
    max_col *= dstep
    canvas = np.zeros((max_row + dstep, max_col + dstep, 3), dtype=np.uint8)
    img_files = sorted(patch_dir.glob("*.png"), key=split_sort)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, imgf, dstep) for imgf in img_files]
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Creating collage"
        ):
            array, col, row = future.result()
            canvas[row : row + dstep, col : col + dstep] = array

    save_collage(canvas, collage_path)


def find_max_col_row(output_dir: Path):
    max_row = max(int(imgf.stem.split("_")[1]) for imgf in output_dir.iterdir())
    max_col = max(int(imgf.stem.split("_")[2]) for imgf in output_dir.iterdir())
    return max_row, max_col


def find_min_row_col(output_dir: Path):
    min_row = min(int(imgf.stem.split("_")[1]) for imgf in output_dir.iterdir())
    min_col = min(int(imgf.stem.split("_")[2]) for imgf in output_dir.iterdir())
    return min_row, min_col


def get_patch_position(imgf: Path) -> Tuple[int, int]:
    splits = imgf.stem.split("_")
    return tuple(map(int, splits[1:]))


def save_collage(canvas: np.ndarray, collage_path: Path) -> None:
    cv2.imwrite(str(collage_path), cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    print(f"Collage saved to {collage_path}")


def save_patch(patch, img_dir: Path, img_path: Path, row: int, col: int):
    Image.fromarray(patch[..., :3]).save(img_dir / f"{img_path.stem}_{row}_{col}.png")


def is_fully_opaque(patch):
    return not (patch[..., 3] == 0).any()


def save_image(canvas: np.ndarray, path: Path, downscale_factor: int) -> None:
    if downscale_factor > 1:
        size = (
            canvas.shape[1] // downscale_factor,
            canvas.shape[0] // downscale_factor,
        )
        canvas = cv2.resize(canvas, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(path), canvas)


def draw_rectangles(
    img: np.ndarray,
    positions: List[Tuple[int, int]],
    step: int,
    downscale_factor: int,
) -> np.ndarray:
    dstep = step // downscale_factor
    for position in positions:
        x1, y1 = position
        x1 *= dstep
        y1 *= dstep
        x2, y2 = x1 + dstep, y1 + dstep
        img = cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=4)
    return img


def generate_correlation_map(
    x_pred: np.ndarray,  # (n, d)
    x_train: np.ndarray,  # (m, d), m < n
    y_train: np.ndarray,  # (m,)
    # emb_paths: List[Path],
    source_img_paths: List[Path],
    pos_idx: List[bool],
    # query_img_path: Path,
    # model_path: Path,
    # split_img_dir: Path,
    step: int,
    downscale_factor: int,
    # metric: str,
    # aggregation: str,
    output_path: Path,
) -> None:
    print("-" * 40 + "generate_correlation_map" + "-" * 40)
    n, d = x_pred.shape
    m, d_ = x_train.shape
    assert d == d_, f"{d=}, {d_=}"

    # compute mahalanobis distance
    dists = mahalanobis_distance_2d(x_pred, x_train)  # (n,)
    assert dists.shape == (n,), f"{dists.shape=}"
    # normalize to [0, 1]
    dists = (dists.max() - dists) / (dists.max() - dists.min())
    # normalize to [0, 255]
    dists = (dists * 255).astype(np.uint8)

    img_name_to_dist = dict(zip(source_img_paths, dists))
    dstep = step // downscale_factor
    max_col, max_row = find_max_col_row(source_img_paths[0].parent)
    max_col *= dstep
    max_row *= dstep
    canvas = np.zeros((max_row + dstep, max_col + dstep, 3), dtype=np.uint8)

    for emb_path, dist in img_name_to_dist.items():
        col, row = get_patch_position(emb_path)
        row *= dstep
        col *= dstep
        canvas[row : row + dstep, col : col + dstep] = dist

    t0 = timer()
    save_image(canvas, output_path, 1)
    t1 = timer()
    print(f"save_image: {f2s(t1 - t0)}")


def _setup_directories(xprize_dir: Path, img_stem: str):
    cor_map_dir = xprize_dir / "correlation_maps"
    cor_map_dir.mkdir(exist_ok=True)
    split_dir = xprize_dir / "split_images"
    assert split_dir.exists(), f"{split_dir} does not exist"
    split_img_dir = split_dir / img_stem
    assert split_img_dir.exists(), f"{split_img_dir} does not exist"
    npy_dir = xprize_dir / "embeddings" / img_stem
    assert npy_dir.exists(), f"{npy_dir} does not exist"
    return cor_map_dir, split_img_dir, npy_dir, split_dir


def main():
    xprize_dir = Path().home() / "xprize_data"
    img_stem = "1"
    cor_map_dir, split_img_dir, npy_dir, split_dir = _setup_directories(
        xprize_dir, img_stem
    )
    npy_paths = sorted(list(npy_dir.glob("*.npy")), key=split_sort)
    assert len(npy_paths) > 0, f"No npy files found in {npy_dir}"
    npy_path = npy_dir.parent / f"{img_stem}.npy"
    assert npy_path.exists(), f"{npy_path} does not exist"
    model_path = Path("models") / "v13_encoder.onnx"
    assert model_path.exists(), f"{model_path} does not exist"
    split_img_paths = list(split_img_dir.glob("*.png"))
    assert len(split_img_paths) > 0, f"No images found in {split_img_dir}"

    metrics = [
        "original",
        "euclidean",
        "cosine",
        "manhattan",
        "chebyshev",
        "mahalanobis",
        "correlation",
    ]
    random_split_img_paths = random.choices(split_img_paths, k=3)
    plt.rcParams["figure.dpi"] = 300
    fig, axes = plt.subplots(
        len(random_split_img_paths),
        len(metrics),
        figsize=(4 * len(metrics), 7 * len(random_split_img_paths)),
    )
    pbar = tqdm(total=len(metrics) * len(random_split_img_paths))

    for i, metric in enumerate(metrics):
        for j, split_img_path in enumerate(random_split_img_paths):
            pbar.update(1)
            if metric == "original":
                collage = cv2.imread(
                    str(xprize_dir / "collages" / f"{img_stem}_10x.png")
                )
                ax = axes[j, i]
                ax.imshow(cv2.cvtColor(collage, cv2.COLOR_BGR2RGB))
                ax.axis("off")
                ax.set_title(f"{split_img_path.stem} | {metric}")
                continue
            collage_name = f"{img_stem}_{split_img_path.stem}_{metric}.png"
            collage_path = cor_map_dir / collage_name
            t0 = timer()
            generate_correlation_map(
                npy_path,
                npy_paths,
                split_img_path,
                model_path,
                split_img_dir,
                step=128,
                downscale_factor=10,
                metric=metric,
                output_path=collage_path,
            )
            t1 = timer()
            print(f"generate_correlation_map: {f2s(t1 - t0)}")
            t0 = timer()
            collage = cv2.imread(str(collage_path))
            ax = axes[j, i]
            ax.imshow(cv2.cvtColor(collage, cv2.COLOR_BGR2RGB))
            ax.axis("off")
            ax.set_title(f"{split_img_path.stem} | {metric}")
            t1 = timer()
            print(f"imread, imshow, axis, set_title: {f2s(t1 - t0)}")

    pbar.close()
    plt.tight_layout()
    plt.savefig(cor_map_dir / f"{img_stem}.png")


if __name__ == "__main__":
    main()

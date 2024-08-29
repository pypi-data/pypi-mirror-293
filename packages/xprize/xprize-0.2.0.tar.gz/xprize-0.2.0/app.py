from pathlib import Path
from typing import Dict, List

import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from src.infer import infer_all_patches
from src.patchify import (
    generate_correlation_map,
    make_collage,
)
from src.split import split_image_cv2
from src.utils import int_sort, load_emb, split_sort

st.set_page_config(page_title="XPRIZE 2024", layout="wide")

st.title("🛰 XPRIZE Hackathon 2024 🌎")
st.caption("Few shot representation learning from satellite images.")
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

# Paths
model_path = Path("models") / "encoder.onnx"
if not model_path.exists():
    st.error(f"Please download the model in `{model_path.resolve()}`")
    st.stop()
xprize_dir = Path("xprize_data")
cached_dir = Path(".cache")
cached_dir.mkdir(exist_ok=True)
raw_dir = xprize_dir / "raw_images"
if not raw_dir.exists():
    st.error(f"Please download the raw images in `{raw_dir.resolve()}`")
    st.stop()
split_dir = cached_dir / "split_images"
split_dir.mkdir(exist_ok=True)
red_emb_root_dir = cached_dir / "reduced_embeddings"
red_emb_root_dir.mkdir(exist_ok=True)
collage_root_dir = cached_dir / "collages"
collage_root_dir.mkdir(exist_ok=True)
corr_map_root_dir = cached_dir / "correlation_maps"
corr_map_root_dir.mkdir(exist_ok=True)
emb_root_dir = cached_dir / "embeddings"
emb_root_dir.mkdir(exist_ok=True)
raw_img_paths = sorted(list(raw_dir.glob("*.tif")), key=int_sort)
gt_img_root_dir = xprize_dir / "filtered_gt_patches"
if not gt_img_root_dir.exists():
    st.error(f"{gt_img_root_dir} does not exist")
    st.stop()
gt_npy_root_dir = emb_root_dir / gt_img_root_dir.stem
gt_npy_root_dir.mkdir(exist_ok=True)

# Class names
class_names = set(i.stem for i in gt_img_root_dir.glob("*") if i.is_dir())
class_to_idx = {k: i for i, k in enumerate(class_names)}

# Get the paths for the ground truth images and embeddings
gt_img_paths_dict: Dict[str, List[Path]] = {k: [] for k in class_names}
for class_name in class_names:
    gt_img_dir = gt_img_root_dir / class_name
    gt_img_paths_dict[class_name] = sorted(gt_img_dir.glob("*.png"), key=split_sort)

gt_emb_paths_dict: Dict[str, List[Path]] = {k: [] for k in class_names}
for class_name in class_names:
    gt_emb_dir = gt_npy_root_dir / class_name
    gt_emb_paths_dict[class_name] = sorted(gt_emb_dir.glob("*.npy"), key=split_sort)

# Get the paths for the raw images
with col1:
    st.subheader("Selection")
    raw_img_path: Path = st.selectbox(
        "Select a satellite image",
        raw_img_paths,
        format_func=lambda x: x.stem,
        index=2,
    )

# Split the image if it has not been split
split_img_dir = split_dir / raw_img_path.stem
if not split_img_dir.exists():
    with col1:
        with st.spinner("Splitting image..."):
            split_image_cv2(raw_img_path, (128, 128), split_img_dir)

# Get the paths for the split images and embeddings
split_img_paths = sorted(split_img_dir.glob("*.png"), key=split_sort)
corr_map_dir = corr_map_root_dir / raw_img_path.stem
corr_map_dir.mkdir(exist_ok=True)
split_emb_dir = emb_root_dir / raw_img_path.stem
split_emb_dir.mkdir(exist_ok=True, parents=True)
split_emb_paths = sorted(split_emb_dir.glob("*.npy"), key=split_sort)

# Get the embeddings for the split images and the ground truth images
rerun = False
with col1:
    if len(split_emb_paths) < len(split_img_paths):
        with st.spinner(f"Creating embeddings for `{raw_img_path.name}`"):
            infer_all_patches(split_img_paths, split_emb_dir, model_path)
            rerun = True

    for class_name in class_names:
        gt_img_paths = gt_img_paths_dict[class_name]
        gt_npy_paths = gt_emb_paths_dict[class_name]
        if len(gt_npy_paths) < len(gt_img_paths):
            gt_emb_dir = gt_npy_root_dir / class_name
            gt_emb_dir.mkdir(exist_ok=True)
            with st.spinner(f"Creating embeddings for `{class_name}`"):
                infer_all_patches(gt_img_paths, gt_emb_dir, model_path)
                rerun = True
if rerun:
    st.rerun()


# Recompute the paths for the embeddings, now that they have been created (not optimal, to fix)
split_emb_paths = sorted(split_emb_dir.glob("*.npy"), key=split_sort)
gt_emb_paths_dict: Dict[str, List[Path]] = {k: [] for k in class_names}
for class_name in class_names:
    gt_emb_dir = gt_npy_root_dir / class_name
    gt_emb_paths_dict[class_name] = sorted(gt_emb_dir.glob("*.npy"), key=split_sort)

# Stack the embeddings for all the split images
stack_split_emb_path = split_emb_dir.parent / f"{split_emb_dir.stem}_stacked.npy"
if not stack_split_emb_path.exists():
    with st.spinner("Stacking embeddings..."):
        stacked_split_embs = []
        for path in split_emb_paths:
            stacked_split_embs.append(load_emb(path))
        stacked_split_embs = np.stack(stacked_split_embs)
        np.save(stack_split_emb_path, stacked_split_embs)

stacked_split_embs = np.load(stack_split_emb_path)

# Stack the embeddings for all the ground truth images
stack_gt_emb_path_dict = {k: gt_npy_root_dir / f"{k}_stacked.npy" for k in class_names}
for class_name in class_names:
    stack_gt_emb_path = stack_gt_emb_path_dict[class_name]
    if not stack_gt_emb_path.exists():
        with st.spinner(f"Stacking embeddings for `{class_name}`"):
            gt_emb_paths = gt_emb_paths_dict[class_name]
            stacked_gt_embs = []
            for gt_emb_path in gt_emb_paths:
                stacked_gt_embs.append(load_emb(gt_emb_path))
            stacked_gt_embs = np.stack(stacked_gt_embs)
            np.save(stack_gt_emb_path, stacked_gt_embs)

stacked_gt_embs_dict = {k: np.load(v) for k, v in stack_gt_emb_path_dict.items()}

# Create a collage
with col1:
    downscale_factor = st.number_input("Downscale factor", 5, 100, 10)
collage_path = collage_root_dir / f"{raw_img_path.stem}_{downscale_factor}x.png"
if not collage_path.exists():
    with st.spinner("Creating collage..."):
        make_collage(split_img_dir, collage_path, 128, downscale_factor)

collage = cv2.imread(str(collage_path))


with col3:
    st.subheader("Few Shot Learning")
    st.caption("Select the patches you want to have as training data.")
    cols = st.columns(len(class_names))
    sel_gt_img_paths_dict: Dict[str, List[Path]] = {k: [] for k in class_names}
    sel_idx_dict: Dict[str, List[int]] = {k: [] for k in class_names}
    for i, (col, class_name) in enumerate(zip(cols, class_names)):
        # select the ground truth images
        sel_gt_img_paths = col.multiselect(
            f"`{class_name}`",
            gt_img_paths_dict[class_name],
            format_func=lambda x: x.stem,
            default=gt_img_paths_dict[class_name][:3],
        )

        # add the selected paths to the dictionary
        sel_gt_img_paths_dict[class_name] = sel_gt_img_paths

        # add the selected indices to the dictionary
        sel_idx_dict[class_name] = [
            gt_img_paths_dict[class_name].index(i) for i in sel_gt_img_paths
        ]

        # display the images
        for sel_split_img_path in sel_gt_img_paths_dict[class_name]:
            col.image(str(sel_split_img_path), caption=sel_split_img_path.stem)

# Get the embeddings for the selected ground truth images from the stacked embeddings
sel_gt_embs = {k: [] for k in class_names}
for class_name in class_names:
    sel_idx = sel_idx_dict[class_name]
    sel_gt_embs[class_name] = stacked_gt_embs_dict[class_name][sel_idx]

# create x_train and y_train
x_train, y_train = [], []
for k, v in sel_gt_embs.items():
    x_train.extend(v)
    y_train.extend([class_to_idx[k]] * len(v))
x_train = np.stack(x_train)
y_train = np.array(y_train)
pos_class = "brazil_nut_tree_patches"
pos_idx = y_train == class_to_idx[pos_class]

# with col3:
#     st.write(f"{x_train.shape=}, {y_train.shape=}")
#     st.write(f"{x_train[:,0]=}, {y_train=}")

# Create a collage
with col2:
    st.subheader("Collage")
    st.image(
        collage,
        use_column_width=True,
        caption=f"Number of patches: {len(split_img_paths):,}",
    )


with col4:
    st.subheader("Correlation")
    img_placeholder = st.empty()
    sel_idx_str = ""
    for k, v in sel_idx_dict.items():
        sel_idx_str += f"{k}-{''.join(map(str, v))}_"
    corr_map_path = corr_map_dir / f"{sel_idx_str}.png"
    # st.write(f"{pos_idx=}")
    x_pred = stacked_split_embs
    n, d = x_pred.shape
    m, d_ = x_train.shape
    assert d == d_, "x_pred.shape[1] != x_train.shape[1]"

    lda = LinearDiscriminantAnalysis()
    lda.fit(x_train, y_train)
    x_train = lda.transform(x_train)  # (m, 2)
    x_pred = lda.transform(x_pred)  # (n, 2)
    assert x_train.shape == (m, 2), f"{x_train.shape=}"
    assert x_pred.shape == (n, 2), f"{x_pred.shape=}"

    if not corr_map_path.exists():
        with st.spinner("Generating correlation map..."):
            generate_correlation_map(
                x_pred=x_pred,
                x_train=x_train[pos_idx],
                source_img_paths=split_img_paths,
                step=128,
                downscale_factor=downscale_factor,
                pos_idx=pos_idx,
                # metric=metric,
                output_path=corr_map_path,
                # aggregation=aggregation,
                y_train=y_train,
            )

    img_placeholder.image(
        str(corr_map_path),
        use_column_width=True,
        caption="""Correlation map using LDA for dimensionality reduction and 
        Mahalanobis distance as similarity measure.""",
    )


with col5:
    st.subheader("Thresholding")
    # whatever has higher correlation than the threshold will be shown in red with alpha=0.5 on top of the correlation map
    img_placeholder = st.empty()
    th_corr_map = cv2.imread(str(corr_map_path))
    # th_corr_map = cv2.cvtColor(th_corr_map, cv2.COLOR_BGR2RGB)

    # Set the threshold value using a slider
    threshold = st.slider("Threshold", 0.5, 1.0, 0.95, 0.01)

    # Thresholding
    gray_corr_map = cv2.cvtColor(th_corr_map, cv2.COLOR_RGB2GRAY)
    mask = (gray_corr_map / 255.0) > threshold

    # Create a red overlay where the mask is True
    overlay = np.zeros_like(th_corr_map)
    overlay[mask] = [255, 0, 0]

    # Combine the original image with the overlay
    th_corr_map_with_overlay = cv2.addWeighted(th_corr_map, 0.5, overlay, 0.5, 0)

    # Display the image
    img_placeholder.image(th_corr_map_with_overlay, use_column_width=True)


with col1:
    st.subheader("Embeddings")
    plt.figure(figsize=(10, 10))
    red_emb_dir = red_emb_root_dir / raw_img_path.stem
    red_emb_dir.mkdir(exist_ok=True)
    red_emb_path = red_emb_dir / f"{raw_img_path.stem}_stacked.npy"
    red_emd_gt_dir = red_emb_root_dir / gt_img_root_dir.stem
    red_emd_gt_dir.mkdir(exist_ok=True)
    red_emb_gt_path_dict = {k: red_emd_gt_dir / f"{k}_stacked.npy" for k in class_names}
    stacked_red_emb_gt: Dict[str, np.ndarray] = {}

    plt.scatter(
        x_pred[:, 0],
        x_pred[:, 1],
        alpha=0.1,
        s=10,
    )

    for class_name in class_names:
        x = x_train[y_train == class_to_idx[class_name], 0]
        y = x_train[y_train == class_to_idx[class_name], 1]
        plt.scatter(x, y, s=200, lw=2, marker="x", label=class_name)

    plt.grid(True, linestyle="--")
    plt.legend()
    st.pyplot(plt)
    st.caption(
        """
    LDA projection of the embeddings.
    Blue dots are the patches from the selected classes.
    Crosses are the patches from the selected training classes.
    """
    )
    plt.close()

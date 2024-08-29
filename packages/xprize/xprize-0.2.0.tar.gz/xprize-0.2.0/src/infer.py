from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import onnxruntime as rt
import streamlit as st
from tqdm import tqdm

from src.utils import f2s, timer


def _preprocess_image(img_path: Path, shape: Tuple[int]) -> np.ndarray:
    img = cv2.imread(str(img_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0
    img = np.transpose(img, (2, 0, 1))
    return np.expand_dims(img, axis=0)


def _get_session_from_model(model_path: Path) -> rt.InferenceSession:
    # Enable parallelism in ONNX Runtime
    session_options = rt.SessionOptions()
    session_options.intra_op_num_threads = 4
    session_options.inter_op_num_threads = 2
    session_options.execution_mode = rt.ExecutionMode.ORT_PARALLEL

    providers = rt.get_available_providers()
    session = rt.InferenceSession(
        model_path.as_posix(),
        providers=providers,
        sess_options=session_options,
    )
    return session


def infer_single_patch(image_path: Path, model_path: Path) -> np.ndarray:
    session = _get_session_from_model(model_path)
    input_shape = session.get_inputs()[0].shape
    input_name = session.get_inputs()[0].name

    input_shape = (1,) + tuple(input_shape[1:])
    preprocessed_array = _preprocess_image(image_path, input_shape)
    result = session.run(None, {input_name: preprocessed_array})[0]
    return result


def infer_all_patches(
    split_paths: Path,
    npy_dir: Path,
    model_path: Path,
    batch_size: int = 256,
) -> np.ndarray:
    # split_paths = list(split_dir.glob("*.png"))
    # print(f"Found {len(split_paths):,} images in {split_dir}")

    # Get input shape and name
    session = _get_session_from_model(model_path)
    input_shape = session.get_inputs()[0].shape
    input_name = session.get_inputs()[0].name
    input_shape = (len(split_paths),) + tuple(input_shape[1:])

    # Preprocess images
    preprocessed_arrays = np.zeros(input_shape, dtype="float32")
    pbar = tqdm(total=len(split_paths), desc="Preprocessing images")
    progress = st.progress(0)
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = {
            executor.submit(_preprocess_image, path, input_shape): i
            for i, path in enumerate(split_paths)
        }
        for future in as_completed(futures):
            i = futures[future]
            preprocessed_arrays[i] = future.result()
            pbar.update(1)
            if i % 100 == 0:
                elapsed_time = pbar.format_dict["elapsed"]
                eta = elapsed_time / pbar.n * (pbar.total - pbar.n)
                progress.progress(pbar.n / pbar.total, f"{pbar.desc} | ETA: {f2s(eta)}")
    pbar.close()
    progress.progress(
        1.0, f"{pbar.desc} | Total elapsed time: {f2s(pbar.format_dict['elapsed'])}"
    )

    def _infer_batch(batch):
        return session.run(None, {input_name: batch})[0]

    batches = [
        preprocessed_arrays[i : i + batch_size]
        for i in range(0, len(preprocessed_arrays), batch_size)
    ]

    result_list = []
    pbar = tqdm(total=len(batches), desc="Running inference")
    progress = st.progress(0)
    for i, batch in enumerate(batches):
        result = _infer_batch(batch)
        result_list.append(result)
        pbar.update(1)
        elapsed_time = pbar.format_dict["elapsed"]
        eta = elapsed_time / pbar.n * (pbar.total - pbar.n)
        progress.progress(pbar.n / pbar.total, f"{pbar.desc} | ETA: {f2s(eta)}")

    pbar.close()
    progress.progress(
        1.0, f"{pbar.desc} | Total elapsed time: {f2s(pbar.format_dict['elapsed'])}"
    )
    result = np.concatenate(result_list, axis=0)

    # Save embeddings
    pbar = tqdm(total=len(result), desc="Saving embeddings")
    progress = st.progress(0)
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = {
            executor.submit(
                np.save, npy_dir / f"{split_paths[i].stem}.npy", np.squeeze(r)
            ): i
            for i, r in enumerate(result)
        }
        for future in as_completed(futures):
            pbar.update(1)
            if i % 100 == 0:
                elapsed_time = pbar.format_dict["elapsed"]
                eta = elapsed_time / pbar.n * (pbar.total - pbar.n)
                progress.progress(pbar.n / pbar.total, f"{pbar.desc} | ETA: {f2s(eta)}")
    pbar.close()
    progress.progress(
        1.0, f"{pbar.desc} | Total elapsed time: {f2s(pbar.format_dict['elapsed'])}"
    )

    return result


if __name__ == "__main__":
    model_path = Path("models") / "v13_encoder.onnx"
    assert model_path.exists(), f"Model {model_path} does not exist"

    image_dir = Path().home() / "xprize_data" / "split_images" / "1"
    assert image_dir.exists(), f"Image directory {image_dir} does not exist"

    npy_dir = image_dir.parents[1] / "embeddings_test" / image_dir.stem
    npy_dir.mkdir(parents=True, exist_ok=True)

    for batch_size in [32, 64, 128, 256, 512]:
        t0 = timer()
        result = infer_all_patches(image_dir, npy_dir, model_path, batch_size)
        t1 = timer()
        print("-" * 80)
        print(f"Batch size: {batch_size}, elapsed time: {f2s(t1 - t0)}")

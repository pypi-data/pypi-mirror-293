import asyncio
import time
from pathlib import Path

import aiofiles
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None
timer = time.perf_counter

# Paths
xprize_dir = Path().home() / "xprize_data"
image_path = xprize_dir / "raw_images" / "3.tif"
output_dir_async_pil = xprize_dir / "split_images_pil"
output_dir_async_cv2 = xprize_dir / "split_images_cv2"


async def _save_patch_async_pil(patch, patch_path):
    async with aiofiles.open(patch_path, mode="wb") as f:
        await f.write(patch)


async def _split_image_async_pil(
    image_path, patch_size, output_dir, max_concurrent_tasks=100
):
    t0 = timer()
    img = Image.open(image_path)
    t1 = timer()
    print(f"Loaded image with PIL in {t1 - t0:.2f} seconds")
    img_width, img_height = img.size
    patch_width, patch_height = patch_size

    output_dir.mkdir(exist_ok=True, parents=True)

    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    pbar = tqdm(total=(img_width // patch_width) * (img_height // patch_height))
    for j, y in enumerate(range(0, img_height, patch_height)):
        for i, x in enumerate(range(0, img_width, patch_width)):
            pbar.update(1)
            patch_coords = (x, y, x + patch_width, y + patch_height)
            patch = img.crop(patch_coords)
            # check if the patch has any alpha channel that is 0
            if patch.getchannel("A").getbbox() is None:
                continue
            # convert to RGB if the image is RGBA
            patch = patch.convert("RGB")
            patch_path = output_dir / f"patch_{i}_{j}.png"
            patch_data = patch.tobytes()
            tasks.append(
                _save_patch_async_pil_with_semaphore(patch_data, patch_path, semaphore)
            )

    for f in tqdm(asyncio.as_completed(tasks), desc="pillow", total=len(tasks)):
        await f


async def _save_patch_async_pil_with_semaphore(patch_data, patch_path, semaphore):
    async with semaphore:
        await _save_patch_async_pil(patch_data, patch_path)


async def save_patch_cv2_async(patch, patch_path):
    async with aiofiles.open(patch_path, mode="wb") as f:
        is_success, buffer = cv2.imencode(".png", patch)
        if is_success:
            await f.write(buffer.tobytes())


def split_image_cv2(image_path, patch_size, output_dir) -> None:
    return asyncio.run(
        split_image_async_cv2(
            image_path, patch_size, output_dir, max_concurrent_tasks=100
        )
    )


async def split_image_async_cv2(
    image_path, patch_size, output_dir, max_concurrent_tasks=100
) -> None:
    t0 = timer()
    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    t1 = timer()
    print(f"Loaded image with cv2 in {t1 - t0:.2f} seconds")
    img_height, img_width = img.shape[:2]
    patch_width, patch_height = patch_size

    output_dir.mkdir(exist_ok=True, parents=True)

    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    for j, y in enumerate(range(0, img_height, patch_height)):
        for i, x in enumerate(range(0, img_width, patch_width)):
            patch = img[y : y + patch_height, x : x + patch_width]
            # check if the patch has any alpha channel that is 0
            if np.any(patch[:, :, 3] == 0):
                continue
            patch_path = output_dir / f"split_{i}_{j}.png"
            tasks.append(
                save_patch_cv2_async_with_semaphore(patch, patch_path, semaphore)
            )

    for f in tqdm(asyncio.as_completed(tasks), desc="cv2", total=len(tasks)):
        await f


async def save_patch_cv2_async_with_semaphore(patch, patch_path, semaphore):
    async with semaphore:
        await save_patch_cv2_async(patch, patch_path)


def benchmark():
    patch_size = (128, 128)

    # Async benchmark using cv2
    start_time = timer()
    asyncio.run(split_image_async_cv2(image_path, patch_size, output_dir_async_cv2))
    end_time = timer()
    print(f"Async approach with cv2 took {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    benchmark()

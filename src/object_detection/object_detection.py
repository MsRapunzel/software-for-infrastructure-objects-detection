"""Module for detecting objects using machine learning."""
from pathlib import Path

from cv2 import GaussianBlur, threshold, THRESH_BINARY
from fastai.vision.all import load_learner, PILImage, Learner
from imantics import Mask
from numpy import ones, uint8
from scipy.ndimage import label

# from utils.helpers import get_resource_path
from utils.logger_config import logger


def label_func(fname: Path) -> Path:
    """
    Returns the corresponding label file path by replacing
    'image' with 'label' in the filename, assuming the label
    is in the same directory.

    Example:
        Input:  Path(".../AOI_3_Paris_image_001.tif")
        Output: Path(".../AOI_3_Paris_label_001.tif")
    """
    return fname.parent / fname.name.replace("image", "label")


def get_model(model_path: str) -> Learner:
    """
    Load custom FastAI model.
    Ensures `label_func` is in scope when unpickling.
    """
    learn = load_learner(model_path)
    return learn


def predict_polygons(path_to_img, model=None, progress_callback=None):
    """
    Detect objects on image with `path_to_img` using `model`

    :returns: Polygons representation
    :rtype: :class:`Polygons`
    """
    progress_callback(40)

    img = PILImage.create(path_to_img)
    img = img.resize((256, 256))

    if model is None:
        model = get_model()

    progress_callback(50)

    pred_mask, _, _ = model.predict(img)

    progress_callback(70)

    mask_np = pred_mask.cpu().numpy().squeeze()
    mask_np = smooth_polygons(mask_np)
    coverage_pct, num_features = predict_coverage(mask_np)
    polygons = Mask(mask_np).polygons()
    return polygons, coverage_pct, num_features


def predict_coverage(mask_np):
    total_pixels = mask_np.size
    building_pixels = (mask_np == 1).sum()
    coverage_pct = (building_pixels / total_pixels) * 100
    logger.info(f"Estimated building coverage: {coverage_pct:.2f}%")

    structure = ones((3, 3), dtype=int)
    _, num_features = label(mask_np, structure=structure)
    logger.info(f"Estimated number of separate buildings: {num_features}")

    return coverage_pct, num_features


def smooth_polygons(mask_np):
    if mask_np.max() <= 1.0:
        mask_np = (mask_np * 255).astype(uint8)
    else:
        mask_np = mask_np.astype(uint8)

    smoothed_mask = GaussianBlur(mask_np, (5, 5), 0)

    _, smoothed_mask = threshold(smoothed_mask, 127, 255, THRESH_BINARY)

    smoothed_mask = smoothed_mask.astype(bool)
    return smoothed_mask

# TODO: Implement calculate percentage of land covered by buildings
# TODO: Implement count number of distinct buildings
# TODO: Implement polygons regularization

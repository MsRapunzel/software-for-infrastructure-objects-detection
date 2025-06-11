"""Module for detecting objects using machine learning."""
from pathlib import Path

from fastai.vision.all import load_learner, PILImage, Learner
from imantics import Mask

from utils.helpers import get_resource_path


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


def get_model() -> Learner:
    """Load custom FastAI model. Ensures `label_func` is in scope when unpickling."""
    model_path = get_resource_path('resources/model/building_segmentation.pkl')
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
    polygons = Mask(mask_np).polygons()
    return polygons

# TODO: Implement calculate percentage of land covered by buildings
# TODO: Implement count number of distinct buildings
# TODO: Implement polygons regularization

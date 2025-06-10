"""Module for detecting objects using machine learning."""
from typing import Any
from pathlib import Path

from fastai.vision.all import load_learner, PILImage
from imantics import Mask

from utils.helpers import get_resource_path, get_file

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

# def get_model1(self):
#     """Slot. Select an image from a file dialog and add it to the `QGraphicsScene`."""
#     initial_dir = get_resource_path('demo_images')
#     filters = "PyTorch models (*.pkl)"
#     model_path = get_file(self.parent, initial_dir, filters)
#     learn = load_learner(model_path)
#     return learn
    
def get_model() -> Any:
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
    # mask_np = smooth_polygons(mask_np)
    polygons = Mask(mask_np).polygons()
    return polygons

# def smooth_polygons1(mask_np):
#     if mask_np.max() <= 1.0:
#         mask_np = (mask_np * 255).astype(np.uint8)
#     else:
#         mask_np = mask_np.astype(np.uint8)

#     # Apply Gaussian blur
#     smoothed_mask = cv2.GaussianBlur(mask_np, (3, 3), 0)

#     # Convert back to binary
#     _, smoothed_mask = cv2.threshold(smoothed_mask, 127, 255, cv2.THRESH_BINARY)

#     # Convert to boolean mask if needed
#     smoothed_mask = smoothed_mask.astype(bool)
#     return smoothed_mask

# def smooth_polygons(mask_np):
#     # Convert to 8-bit
#     if mask_np.max() <= 1.0:
#         mask_np = (mask_np * 255).astype(np.uint8)
#     else:
#         mask_np = mask_np.astype(np.uint8)

#     # Threshold to binary
#     _, binary = cv2.threshold(mask_np, 127, 255, cv2.THRESH_BINARY)

#     # Find contours
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     result_polygons = []

#     for cnt in contours:
#         if cv2.contourArea(cnt) < 10:
#             continue

#         # Approximate contour shape
#         epsilon = 0.005 * cv2.arcLength(cnt, True)
#         approx = cv2.approxPolyDP(cnt, epsilon, True)

#         # Convert to shapely polygon
#         approx_points = approx[:, 0, :]  # Nx2
#         poly = Polygon(approx_points)

#         # Regularize angles to 90 degrees
#         rectified_poly = orthogonalize_polygon(poly)
#         if rectified_poly is not None:
#             result_polygons.append(rectified_poly)

#     # Merge polygons and rasterize again to mask
#     union = unary_union(result_polygons)
#     mask_out = polygon_to_mask(union, mask_np.shape)

#     return mask_out.astype(bool)

# def orthogonalize_polygon(poly: Polygon):
#     """Adjust polygon edges to follow right angles."""
#     if not poly.is_valid or poly.area < 10:
#         return None

#     coords = list(poly.exterior.coords[:-1])  # ignore closing point
#     if len(coords) < 3:
#         return None

#     new_coords = []
#     for i in range(len(coords)):
#         p1 = np.array(coords[i - 1])
#         p2 = np.array(coords[i])
#         p3 = np.array(coords[(i + 1) % len(coords)])

#         # Vectors
#         v1 = p2 - p1
#         v2 = p3 - p2

#         # Snap direction (to axis)
#         delta = p3 - p2
#         if abs(delta[0]) > abs(delta[1]):
#             new_point = np.array([p3[0], p2[1]])  # horizontal
#         else:
#             new_point = np.array([p2[0], p3[1]])  # vertical

#         new_coords.append(tuple(p2))
#         new_coords.append(tuple(new_point))

#     # Remove duplicates
#     cleaned_coords = []
#     for pt in new_coords:
#         if len(cleaned_coords) == 0 or not np.allclose(pt, cleaned_coords[-1]):
#             cleaned_coords.append(pt)

#     # Close the loop
#     if len(cleaned_coords) < 3:
#         return None
#     if cleaned_coords[0] != cleaned_coords[-1]:
#         cleaned_coords.append(cleaned_coords[0])

#     if len(cleaned_coords) < 4:
#         return None  # too small to form a polygon

#     new_poly = Polygon(cleaned_coords)
#     return new_poly if new_poly.is_valid and new_poly.area > 1.0 else None

# def polygon_to_mask(poly, shape):
#     """Rasterize polygon back to mask"""
#     mask = np.zeros(shape, dtype=np.uint8)
#     if poly.is_empty:
#         return mask
#     if poly.geom_type == 'Polygon':
#         polys = [poly]
#     else:
#         polys = list(poly.geoms)

#     for p in polys:
#         pts = np.array(p.exterior.coords, dtype=np.int32)
#         cv2.fillPoly(mask, [pts], 255)
#     return mask

# def predict_coverage(mask_np):
#     total_pixels = mask_np.size
#     building_pixels = (mask_np == 1).sum()
#     coverage_pct = (building_pixels / total_pixels) * 100
#     print(f"Estimated building coverage: {coverage_pct:.2f}%")

#     structure = np.ones((3, 3), dtype=int)
#     labeled_array, num_features = label(mask_np, structure=structure)
#     print(f"Estimated number of separate buildings: {num_features}")

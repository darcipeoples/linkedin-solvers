from PIL import Image
import numpy as np
import cv2

# Check if inner box is contained in the outer box
def is_contained(inner, outer):
    x1, y1, x2, y2 = inner
    ox1, oy1, ox2, oy2 = outer
    return x1 >= ox1 and y1 >= oy1 and x2 <= ox2 and y2 <= oy2

# Check if two boxes overlap
def are_overlapping(rect_a, rect_b):
    ax1, ay1, ax2, ay2 = rect_a
    bx1, by1, bx2, by2 = rect_b
    return (ax1 <= bx1 <= ax2 and ay1 <= by1 <= ay2) or (ax1 <= bx2 <= ax2 and ay1 <= by2 <= ay2)

# Remove boxes that are nested within each other
def remove_nested_boxes(boxes):
    filtered = []
    for i, box in enumerate(boxes):
        if not any(i != j and is_contained(box, other) for j, other in enumerate(boxes)):
            filtered.append(box)
    return filtered

# Merge together overlapping boxes
# TODO: Not very efficient
def merge_overlapping_boxes(boxes):
    while True:
        new_boxes = set()
        overlapping_boxes = set()
        # Iterate over first boxes
        for i, box_a in enumerate(boxes):
            # Iterate over second boxes
            for j in range(i + 1, len(boxes)):
                box_b = boxes[j]
                # Check if the boxes overlap
                if are_overlapping(box_a, box_b):
                    overlapping_boxes.add(box_a)
                    overlapping_boxes.add(box_b)
                    # Add the merged box to our new list
                    new_boxes.add((min(box_a[0], box_b[0]), min(box_a[1], box_b[1]), max(box_a[2], box_b[2]), max(box_a[3], box_b[3])))
                    break
            # Add box A to our new list, if it wasn't merged
            if box_a not in overlapping_boxes:
                new_boxes.add(tuple(box_a))
        boxes = list(new_boxes)
        # Stop trying to merge if we didn't find any
        if not overlapping_boxes:
            break
    return boxes

# Find bounding boxes around contours made of the given colors
# Optional: Filter by size, draw on a debug image, merge overlapping boxes, remove nested boxes
def find_boxes(image_np, target_colors=[], min_size=0, remove_nested=False, max_size=float("inf"), draw=None, box_color='magenta', tolerance=2, merge_overlapping=False, width=1):
    # In the image, find pixels close enough to any of the target colors
    mask = None
    for target_color in target_colors:
        target_color = np.array(target_color)
        dist = np.linalg.norm(image_np - target_color, axis=2)
        new_mask = np.array(dist < tolerance).astype(np.uint8) * 255
        if mask is None:
            mask = new_mask
        else:
            mask |= new_mask

    # Create contours around the matching pixels
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Compute bounding boxes for the contours. Filter boxes by size.
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if max_size >= w >= min_size and max_size >= h >= min_size:
            boxes.append((x, y, x + w, y + h))
    
    # Remove nested boxes
    if remove_nested:
        boxes = remove_nested_boxes(boxes)

    # Merge overlapping boxes
    if merge_overlapping:
        boxes = merge_overlapping_boxes(boxes)

    # Draw the boxes
    if draw is not None:
        for box in boxes:
            draw.rectangle(box, outline=box_color, width=width)

    return boxes

# Draw boxes on the debug image
def draw_boxes(boxes, box_color, draw, width=1):
    if draw is None:
        return
    for box in boxes:
        draw.rectangle(box, outline=box_color, width=width)

# Convert an image greyscale and normalize to [0, 1]
def normalize_greyscale(img):
    return np.array(img.convert("L")) / 255.0

# Load a mask in normalized greyscale
def load_mask(path):
    return normalize_greyscale(Image.open(path))

# Load multiple masks, in normalized greyscale
def load_masks(paths):
    return [load_mask(path) for path in paths]

# Find distance between the image and the mask (resize the mask)
# TODO: rename
def distance_to_mask(img_np, mask_np):
    # Scale mask to image size
    mask_resized = Image.fromarray((mask_np * 255).astype(np.uint8)).resize(img_np.shape[::-1], Image.Resampling.BILINEAR)
    # Convert to normalized array
    mask_resized_np = np.array(mask_resized) / 255.0
    # Calculate the L2 distance between the mask and image
    return np.linalg.norm(img_np - mask_resized_np)

# Return the label of the mask that matches the image best
# TODO: rename
def classify_symbol(img, masks):
    img_np = normalize_greyscale(img)
    scores = {label: float("inf") for label in masks}
    for label, mask_nps in masks.items():
        for mask_np in mask_nps:
            score = distance_to_mask(img_np, mask_np)
            scores[label] = min(score, scores[label])
    closest = min(scores, key=scores.get)
    return closest, scores
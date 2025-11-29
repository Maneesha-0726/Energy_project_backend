from ultralytics import YOLO
import numpy as np
from PIL import Image

# Load YOLO models once
primary_model = YOLO("best.pt")
snow_model = YOLO("snow.pt")
panel_model = YOLO("panel_detect.pt")

FAULT_LOSS = {
    "Non-Defective": (0.00, 0.00),
    "Clean": (0.00, 0.00),
    "Bird-drop": (0.121, 0.221),
    "Dusty": (0.115, 0.150),
    "Snow-Covered": (0.10, 0.34),
    "Physical Damage": (0.25, 0.50),
    "Electrical-Damage": (0.30, 0.70),
}

def normalize_label(raw_label):
    if not raw_label:
        return "Unknown"
    key = raw_label.strip().lower()
    mapping = {
        "bird": "Bird-drop",
        "clean": "Non-Defective",
        "dusty": "Dusty",
        "snow": "Snow-Covered",
        "physical damage": "Physical Damage",
        "electrical-damage": "Electrical-Damage",
    }
    return mapping.get(key, raw_label)

def detect_faults(pil_img, conf_thresh=0.4):
    """Runs YOLO fault detection"""
    res1 = primary_model.predict(pil_img, conf=conf_thresh, verbose=False)[0]
    dets1 = [(normalize_label(res1.names[int(b.cls[0])]),
              float(b.conf[0]),
              tuple(map(int, b.xyxy[0]))) for b in res1.boxes]

    # if clean, fallback to snow model
    meaningful = [d for d in dets1 if d[0] not in ("Clean", "Non-Defective")]
    if meaningful:
        return dets1, np.asarray(res1.plot()).astype(np.uint8)

    res2 = snow_model.predict(pil_img, conf=conf_thresh, verbose=False)[0]
    dets2 = [(normalize_label(res2.names[int(b.cls[0])]),
              float(b.conf[0]),
              tuple(map(int, b.xyxy[0]))) for b in res2.boxes]
    return dets2, np.asarray(res2.plot()).astype(np.uint8)

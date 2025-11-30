from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from PIL import Image
import uuid
import io
import os

from .models import GrayscaleImage, YOLOOutput

# ---------------- ENERGY LOSS CONSTANTS ----------------
FAULT_LOSS = {
    "Non-Defective": 0.00,
    "Dusty": 0.12,
    "Bird-drop": 0.18,
    "Snow-Covered": 0.28,
    "Physical Damage": 0.40,
    "Electrical-Damage": 0.55,
}

# ---------------- LABEL NORMALIZATION ----------------
def normalize(lbl):
    lbl = lbl.strip().lower()
    mapping = {
        "clean": "Non-Defective",
        "non-defective": "Non-Defective",
        "dusty": "Dusty",
        "bird": "Bird-drop",
        "bird-drop": "Bird-drop",
        "snow": "Snow-Covered",
        "physical damage": "Physical Damage",
        "faulty_solar_panel": "Physical Damage",
        "electrical-damage": "Electrical-Damage",
    }
    return mapping.get(lbl, lbl.title())


# ---------------- LOAD YOLO MODELS (ONCE) ----------------
from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

print("⚡ Loading YOLO models ONCE...")

best_model = YOLO(os.path.join(MODEL_DIR, "best.pt"))
snow_model = YOLO(os.path.join(MODEL_DIR, "snow.pt"))
panel_model = YOLO(os.path.join(MODEL_DIR, "panel_detect.pt"))

print("✅ YOLO Models Loaded Successfully!")


# ---------------- UTIL: DOWNSCALE IMAGE (RAM SAFE) ----------------
def save_temp_small_image(image_path):
    """Resize image to 640px for low RAM inference"""
    pil = Image.open(image_path).convert("RGB")

    # Resize to max 640px (YOLO recommended)
    pil.thumbnail((640, 640))

    buffer = io.BytesIO()
    pil.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    temp_path = os.path.join(os.path.dirname(image_path), "temp_small.jpg")
    with open(temp_path, "wb") as f:
        f.write(buffer.getvalue())

    return temp_path


# ---------------- MAIN VIEW ----------------
@method_decorator(csrf_exempt, name='dispatch')
class Index(View):

    def get(self, request):
        return JsonResponse({"status": "Backend is live"}, status=200)

    def post(self, request):

        # IMAGE VALIDATION
        if "greyImage" not in request.FILES:
            return JsonResponse({"error": "No image uploaded"}, status=400)

        # USER INPUTS
        location = request.POST.get("location", "Home")
        capacity = float(request.POST.get("capacity", 5))
        sun_hours = float(request.POST.get("sunHours", 5))

        SYSTEM_CAPACITY = max(capacity, 0.1)
        SUNLIGHT = max(sun_hours, 0.1)
        max_possible_energy = SYSTEM_CAPACITY * SUNLIGHT

        # SAVE ORIGINAL IMAGE
        uploaded = request.FILES["greyImage"]
        img_obj = GrayscaleImage.objects.create(
            image=uploaded,
            location=location,
            capacity=SYSTEM_CAPACITY,
            sunlight_hours=SUNLIGHT
        )
        image_path = img_obj.image.path

        # ---------------- DOWNSCALE IMAGE (VERY IMPORTANT) ----------------
        small_img_path = save_temp_small_image(image_path)

        # ---------------- RUN MODELS ON SMALL IMAGE ----------------
        # MAIN
        best_res = best_model.predict(small_img_path, conf=0.25, verbose=False)[0]

        detections = []
        for b in best_res.boxes:
            lbl = normalize(best_res.names[int(b.cls[0])])
            conf = float(b.conf[0])
            box = list(map(int, b.xyxy[0].tolist()))
            detections.append((lbl, conf, box))

        # FALLBACK TO SNOW MODEL
        if not any(lbl != "Non-Defective" for lbl, _, _ in detections):
            snow_res = snow_model.predict(small_img_path, conf=0.25, verbose=False)[0]
            detections = []
            for b in snow_res.boxes:
                lbl = normalize(snow_res.names[int(b.cls[0])])
                conf = float(b.conf[0])
                box = list(map(int, b.xyxy[0].tolist()))
                detections.append((lbl, conf, box))
            final_res = snow_res
        else:
            final_res = best_res

        # PANEL MODEL
        panel_res = panel_model.predict(small_img_path, conf=0.25, verbose=False)[0]
        panels = [list(map(int, b.xyxy[0].tolist())) for b in panel_res.boxes]
        if not panels:
            panels = [(0, 0, 640, 640)]

        # ---------------- ENERGY LOSS CALCULATIONS ----------------
        total_daily_loss = 0
        panel_summary = []

        for idx, (px1, py1, px2, py2) in enumerate(panels, start=1):

            panel_area = max(1, (px2 - px1) * (py2 - py1))
            panel_loss = 0
            faults = []

            for lbl, conf, (fx1, fy1, fx2, fy2) in detections:

                # Intersection
                ix1, iy1 = max(px1, fx1), max(py1, fy1)
                ix2, iy2 = min(px2, fx2), min(py2, fy2)

                if ix2 > ix1 and iy2 > iy1:

                    fa = (ix2 - ix1) * (iy2 - iy1)
                    loss_fraction = FAULT_LOSS.get(lbl, 0) * (fa / panel_area)
                    daily_loss = loss_fraction * SYSTEM_CAPACITY * SUNLIGHT

                    faults.append({
                        "fault": lbl,
                        "confidence": conf,
                        "affected_area": round((fa / panel_area) * 100, 2),
                        "loss_percentage": round(loss_fraction * 100, 2),
                        "daily_loss": round(daily_loss, 3),
                    })

                    panel_loss += daily_loss

            total_daily_loss += panel_loss

            panel_summary.append({
                "panel_number": idx,
                "faults": faults,
                "panel_loss_kwh": round(panel_loss, 3),
            })

        final_energy = max(max_possible_energy - total_daily_loss, 0)

        # ---------------- SAVE ANNOTATED IMAGE ----------------
        annotated = final_res.plot()
        pil_img = Image.fromarray(annotated).convert("RGB")

        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        filename = f"result_{uuid.uuid4()}.jpg"
        saved_path = default_storage.save("yolo_outputs/" + filename, ContentFile(buffer.getvalue()))

        # REMOVE TEMP IMAGE
        try:
            os.remove(small_img_path)
        except:
            pass

        # ---------------- RESPONSE ----------------
        return JsonResponse({
            "message": "Energy Loss Analysis Completed",
            "summary": {
                "location": location,
                "total_panels": len(panels),
                "system_capacity_kw": SYSTEM_CAPACITY,
                "sunlight_hours": SUNLIGHT,
                "max_possible_energy": round(max_possible_energy, 3),
                "final_energy": round(final_energy, 3),
                "total_daily_loss_kwh": round(total_daily_loss, 3),
                "overall_loss_percentage":
                    round((total_daily_loss / max_possible_energy) * 100, 2),
            },

            "panel_analysis": panel_summary,
            "download_url": saved_path,
            "file_name": filename
        })

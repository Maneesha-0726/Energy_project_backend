from django.db import models
import uuid

# =====================================================
# Stores the uploaded original image
# =====================================================
class GrayscaleImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW FIELDS TO STORE USER INPUT
    location = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.FloatField(null=True, blank=True)
    sunlight_hours = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.signature)


# =====================================================
# Optional resized version storage
# =====================================================
class ResizedImage(models.Model):
    grayscale_image = models.OneToOneField(GrayscaleImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resized_images/')

    def __str__(self):
        return f"Resized image for {self.grayscale_image.signature}"


# =====================================================
# Stores YOLO ANNOTATED OUTPUT IMAGE
# =====================================================
class YOLOOutput(models.Model):
    input_image = models.ForeignKey(GrayscaleImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='yolo_outputs/')
    download_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields added for energy summary
    total_panels = models.IntegerField(null=True, blank=True)
    total_daily_loss_kwh = models.FloatField(null=True, blank=True)
    loss_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.download_token)


# =====================================================
# Stores PANEL-WISE results (One image may have 4–10 panels)
# =====================================================
class PanelAnalysis(models.Model):
    yolo_output = models.ForeignKey(YOLOOutput, on_delete=models.CASCADE, related_name="panels")

    panel_number = models.IntegerField()
    panel_loss_kwh = models.FloatField()

    def __str__(self):
        return f"Panel {self.panel_number} | Loss {self.panel_loss_kwh} kWh"


# =====================================================
# Stores EACH FAULT inside a panel
# =====================================================
class FaultDetail(models.Model):
    panel = models.ForeignKey(PanelAnalysis, on_delete=models.CASCADE, related_name="faults")

    fault_name = models.CharField(max_length=200)
    confidence = models.FloatField()
    affected_area = models.FloatField()
    loss_percentage = models.FloatField()
    daily_loss = models.FloatField()

    def __str__(self):
        return f"{self.fault_name} ({self.daily_loss} kWh)"

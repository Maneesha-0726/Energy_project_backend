from django.db import models

class GrayscaleImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    location = models.CharField(max_length=100)
    capacity = models.FloatField()
    sunlight_hours = models.FloatField()
    uploaded = models.DateTimeField(auto_now_add=True)

class YOLOOutput(models.Model):
    input_image = models.ForeignKey(GrayscaleImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="yolo_outputs/")
    total_panels = models.IntegerField()
    total_daily_loss_kwh = models.FloatField()
    loss_percentage = models.FloatField()

from django.contrib import admin
from detection.models import Detection, Camera
from django.utils.html import format_html


class DetectionAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "count", "camera_name", "camera_location", "precision", "image_tag")
    readonly_fields = ("time", "count", "camera", "precision", "image", "camera_name", "camera_location")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>'.format(obj.image.url))
        return "(No image)"
    image_tag.short_description = "Image Preview"

    def camera_name(self, obj):
        return obj.camera.name if obj.camera else "No Camera"
    camera_name.short_description = "Camera Name"

    def camera_location(self, obj):
        return obj.camera.location if obj.camera else "No Location"
    camera_location.short_description = "Camera Location"

admin.site.register(Detection, DetectionAdmin)

admin.site.register(Camera)

from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


# Create your models here.
class QR_code(models.Model):
    data = models.CharField(max_length=250)
    qr_code = models.ImageField(upload_to="qr_code", null=True, blank=True)

    def save(self, *args, **kwargs):  # Override save to generate a QR image before storing this model.
        qr_image = qrcode.make(self.data).get_image()  # Get the PIL image underlying the generated QR code.
        file_name = f"qr_code-{uuid.uuid4().hex}.png"  # Use a unique filename that is safe on every filesystem.
        buffer = BytesIO()  # Create an in-memory buffer for the PNG image.
        qr_image.save(buffer, "PNG")  # Encode the complete QR image as PNG into the buffer.
        buffer.seek(0)  # Rewind the buffer so Django can read the image data.
        self.qr_code.save(file_name, File(buffer), save=False)  # Attach the PNG to the image field without saving the model yet.
        qr_image.close()  # Release the QR image resources.
        return super().save(*args, **kwargs)  # Persist the model using Django's default save implementation.

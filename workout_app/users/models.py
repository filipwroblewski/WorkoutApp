from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile

class PremiumAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        """
        Check if the premium account is currently active.
        """
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"Premium Account for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    premium_account = models.OneToOneField(PremiumAccount, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Check if the instance has an existing primary key
        if self.pk:
            # Get the previous instance from the database
            try:
                prev_instance = UserProfile.objects.get(pk=self.pk)
            except UserProfile.DoesNotExist:
                prev_instance = None

            # Delete the previous photo if it exists and it's different from the new photo
            if prev_instance and prev_instance.profile_picture and self.profile_picture != prev_instance.profile_picture:
                prev_instance.profile_picture.delete(save=False)

        # Save the new profile picture
        if self.profile_picture:
            # Open the uploaded image
            img = Image.open(self.profile_picture)

            # Crop the image to a square
            cropped_img = crop_image(img)

            # Resize the cropped image
            resized_img = resize_image(cropped_img, (360, 360))

            # Save the modified image to a BytesIO object
            temp_buffer = BytesIO()
            resized_img.save(temp_buffer, format='PNG')
            temp_buffer.seek(0)

            # Update the profile_picture field with the resized image
            self.profile_picture.save(self.profile_picture.name, ImageFile(temp_buffer), save=False)

            # Close the BytesIO buffer
            temp_buffer.close()

        # Save the new profile picture and other fields
        super().save(*args, **kwargs)

def crop_image(image):
    """
    Crop the given image to make it a square.
    """
    # Get the image dimensions
    width, height = image.size

    # Calculate the size of the square
    size = min(width, height)

    # Calculate the cropping box to make it a square
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2

    # Crop the image to the square
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image

def resize_image(image, desired_size):
    """
    Resize the given image to the desired dimensions.
    """
    # Resize the image to the desired dimensions with LANCZOS filter for anti-aliasing
    resized_image = image.resize(desired_size, Image.LANCZOS)

    return resized_image

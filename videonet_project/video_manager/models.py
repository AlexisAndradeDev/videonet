from django.db import models
from azure.storage.blob import BlobServiceClient
from django.conf import settings
import uuid
import os

from lib.azure.blob_storage import delete_blob

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        """Override the delete method to remove file from Azure Blob Storage
        when the instance of the model is deleted."""
        if not settings.USE_AZURE:
            super().delete(*args, **kwargs)
            return
        
        if self._delete_blob_from_storage(self.video_file.name):
            # the blob must be succesfully deleted in order to delete the 
            # instance from the database
            super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """Override the save method to delete the previous file if it's changed."""
        # Change filename to a unique hash
        if not settings.USE_AZURE:
            self.video_file.name = self._generate_unique_filename()
            if self.thumbnail.name:
                self.thumbnail.name = self._generate_unique_filename()
            super().save(*args, **kwargs)
            return
                
        if self.pk: # if the object already exists
            old_video = Video.objects.get(pk=self.pk)
            can_be_saved = True

            # Not the same video file
            if self.video_file.name != old_video.video_file.name:
                # Replace video
                if not self._delete_blob_from_storage(old_video.video_file.name):
                    self.video_file.name = self._generate_unique_filename()
                    can_be_saved = False

            # Not the same thumbnail file
            if can_be_saved and self.thumbnail.name != old_video.thumbnail.name:
                # Replace thumbnail
                if not self._delete_blob_from_storage(old_video.thumbnail.name):
                    self.thumbnail.name = self._generate_unique_filename()
                    can_be_saved = False

            if can_be_saved:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def _generate_unique_filename(self):
        """Returns a unique filename."""
        filename = uuid.uuid4().hex[:30]
        return filename

    def _delete_blob_from_storage(self, file_name: str) -> bool:
        """Delete file from Azure Blob Storage."""
        try:
            delete_blob(file_name, settings.STORAGES["default"]["OPTIONS"]["connection_string"])
        except Exception as e:
            print(f"Failed to delete file '{file_name}' from Azure Blob Storage: {e}")
            return False
        return True

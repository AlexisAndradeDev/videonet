from django.db import models
from azure.storage.blob import BlobServiceClient
from django.conf import settings

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
        if self._delete_blob_from_storage(self.video_file.name):
            # the blob must be succesfully deleted in order to delete the 
            # instance from the database
            super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """Override the save method to delete the previous file if it's changed."""
        if self.pk: # if the object already exists
            if self._replace_file():
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
    
    def _delete_blob_from_storage(self, file_name: str) -> bool:
        """Delete file from Azure Blob Storage."""
        try:
            delete_blob(file_name, settings.STORAGES["default"]["OPTIONS"]["connection_string"])
        except Exception as e:
            print(f"Failed to delete file '{file_name}' from Azure Blob Storage: {e}")
            return False
        return True
    
    def _replace_file(self) -> bool:
        """
        Delete the previous file if it exists and is being replaced.

        Returns:
            bool: True if the instance of the model can be saved; else, False.
        """        
        old_video = Video.objects.get(pk=self.pk)
        if old_video.video_file != self.video_file:
            if not self._delete_blob_from_storage(old_video.video_file.name):
                # the file was replaced by the user but couldn't be
                # deleted from Azure Blob Storage
                return False
        return True

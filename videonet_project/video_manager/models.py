from django.db import models
from azure.storage.blob import BlobServiceClient
from django.conf import settings
import uuid
import os
from util.azure.blob_storage import delete_blob
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/", validators=[FileExtensionValidator(['mp4', 'avi', 'mov', 'mkv'])])
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """Override the delete method to remove files from Azure Blob Storage
        when the instance of the model is deleted.
        
        If there's an error when trying to delete some file, the register
        is deleted from the database anyway. This way, the user can delete
        videos from the database even if there's a problem with Azure Blob
        Storage, and remaining files would have to be deleted manually."""
        if self.thumbnail.name:
            # Delete thumbnail file
            if settings.USE_AZURE:
                self._delete_blob_from_storage(self.thumbnail.name)
            else:
                try:
                    self.thumbnail.delete(save=False)
                except:
                    pass

        # Delete video file
        if settings.USE_AZURE:
            self._delete_blob_from_storage(self.video_file.name)
        else:
            try:
                self.video_file.delete(save=False)
            except:
                pass

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Override the save method to update or create, managing files in Azure/Local storage."""
        if self.pk:
            self._update(*args, **kwargs)
        else:
            self._create(*args, **kwargs)

    def _update(self, *args, **kwargs):
        """Deletes the old files and creates the new ones in Azure/Local storage.
        
        If there's an error when trying to delete some file, the register
        is updated in the database anyway. This way, the user can update
        videos even if there's a problem with Azure Blob Storage, and remaining
        files would have to be deleted manually."""
        old_video = Video.objects.get(pk=self.pk)
        
        upload_thumbnail_name, old_thumbnail_name = self.thumbnail.name, old_video.thumbnail.name

        # Not the same thumbnail file
        if old_thumbnail_name: # Delete blob only if a thumbnail existed
            if upload_thumbnail_name != old_thumbnail_name:
                # Replace thumbnail
                if settings.USE_AZURE:
                    self._delete_blob_from_storage(old_thumbnail_name)
                else:
                    try:
                        old_video.thumbnail.delete(save=False)
                    except Exception as e:
                        print(f"Failed to delete file '{old_thumbnail_name}' from Local Storage: {e}")

        upload_video_name, old_video_name = self.video_file.name, old_video.video_file.name

        # Not the same video file
        if upload_video_name != old_video_name:
            # Replace video
            if settings.USE_AZURE:
                self._delete_blob_from_storage(old_video_name)
            else:
                try:
                    old_video.video_file.delete(save=False)
                except Exception as e:
                    print(f"Failed to delete file '{old_video_name}' from Local Storage: {e}")

        if upload_video_name != old_video_name:
            self.video_file.name = self._generate_unique_filename(upload_video_name)
        if upload_thumbnail_name != old_thumbnail_name:
            self.thumbnail.name = self._generate_unique_filename(upload_thumbnail_name)
        super().save(*args, **kwargs)

    def _create(self, *args, **kwargs):
        # Generate unique names for new files
        self.video_file.name = self._generate_unique_filename(self.video_file.name)
        if self.thumbnail.name:
            self.thumbnail.name = self._generate_unique_filename(self.thumbnail.name)
        super().save(*args, **kwargs)

    def _generate_unique_filename(self, original_filename):
        """Returns a unique filename with the original extension."""
        extension = os.path.splitext(original_filename)[1]
        filename = uuid.uuid4().hex[:30] + extension
        return filename

    def _delete_blob_from_storage(self, file_name: str) -> bool:
        """Delete file from Azure Blob Storage."""
        try:
            delete_blob(file_name, settings.STORAGES["default"]["OPTIONS"]["connection_string"])
        except Exception as e:
            print(f"Failed to delete file '{file_name}' from Azure Blob Storage: {e}")
            return False
        return True

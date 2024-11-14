from django.test import TestCase
from django.contrib.auth.models import User
from .models import Video

class VideoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.video = Video.objects.create(
            title='Video Test',
            description='Descripcion del video de prueba.',
            video_file='videos/test_vid.mp4',
            thumbnail='thumbnails/test_img.jpg',
            user=self.user
        )

    def test_video_creation(self):
        self.assertEqual(self.video.title, 'Video Test')
        self.assertEqual(self.video.description, 'Descripcion del video de prueba.')
        self.assertEqual(self.video.user.username, 'testuser')

    def test_video_delete(self):
        video_id = self.video.id
        self.video.delete()
        with self.assertRaises(Video.DoesNotExist):
            Video.objects.get(id=video_id)

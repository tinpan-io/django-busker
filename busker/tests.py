import os
import tempfile
from uuid import uuid4

from django.core.files import File
from django.test import TestCase
from PIL import Image

from .models import Artist, File as BuskerFile, DownloadableWork, DownloadCode, Batch, work_file_path, work_image_path


# Create your tests here.
class BuskerTestCase(TestCase):

    def setUp(self):
        # Create a couple of images to use for the downloadable work and BuskerFile objects
        self.img = Image.new("RGB", (1200, 1200), "#990000")
        self.img_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        self.img_basename = os.path.split(self.img_file.name)[-1]
        self.img.save(self.img_file, format="JPEG")

        self.img2 = Image.new("RGB", (5000, 5000), "#336699")
        self.img2_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        self.img2_basename = os.path.split(self.img2_file.name)[-1]
        self.img2.save(self.img2_file, format="PNG")

        self.artist = Artist.objects.create(name="Conrad Poohs", url="https://magicians.band")
        self.work_file = File(self.img_file)
        self.work = DownloadableWork(artist=self.artist, title="Dancing Teeth", published=True, image=self.work_file)
        self.work.image.save(name=self.img_basename, content=self.img_file)
        self.work.save()

        self.busker_file_attachment = File(self.img2_file)
        self.busker_file = BuskerFile(work=self.work, description="", file=self.busker_file_attachment)
        self.busker_file.file.save(name=self.img2_basename, content=self.img2_file)
        self.busker_file.save()
        self.batch = Batch.objects.create(
                                     work=self.work,
                                     label="Conrad Poohs Test Batch",
                                     private_note="Batch for unit testing",
                                     public_message="#Thank You\nThis is a message with *markdown* **formatting**.",
                                     number_of_codes=10
                                     )

    def tearDown(self):
        os.unlink(self.img_file.name)
        os.unlink(self.img2_file.name)

    def test_work_image_path(self):
        """
        Tests the expected upload_to value when attaching an image to a DownloadableWork object.
        """
        # (File objects' upload_to method gets called with the base filename)
        img_base_name = os.path.split(self.img_file.name)[-1]
        expected_path = f"busker/downloadable_work_images/{self.work.id}/{img_base_name}"
        self.assertEquals(work_image_path(self.work, img_base_name),
                          expected_path,
                          "Image upload paths should use the format `busker/downloadable_work_images/[downloadable "
                          "work id]/[uploaded img file name]`")

    def test_work_file_path(self):
        """
        Tests the expected upload_to value when attaching a file to a BuskerFile object.
        """
        # (File objects' upload_to method gets called with the base filename)
        file_base_name = os.path.split(self.busker_file_attachment.name)[-1]
        expected_path = f"busker/files/{self.busker_file.id}/{file_base_name}"
        self.assertEquals(work_file_path(self.busker_file, file_base_name),
                          expected_path,
                          "BuskerFile upload paths should use the format `busker/files/[busker file object id]/["
                          "uploaded img file name]`")

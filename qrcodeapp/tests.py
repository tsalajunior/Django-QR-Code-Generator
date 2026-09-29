from tempfile import TemporaryDirectory

from django.test import TestCase, override_settings

from .models import QR_code

# Create your tests here.
class QRGeneratorViewTests(TestCase):
	def setUp(self):
		self.media_dir = TemporaryDirectory()
		self.addCleanup(self.media_dir.cleanup)
		settings_override = override_settings(MEDIA_ROOT=self.media_dir.name)
		settings_override.enable()
		self.addCleanup(settings_override.disable)

	def test_post_generates_and_stores_qr_code(self):
		response = self.client.post("/", {"data": "hello"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["qr_code"].data, "hello")
		self.assertTrue(response.context["qr_code"].qr_code.storage.exists(
			response.context["qr_code"].qr_code.name
		))

	def test_post_generates_qr_code_for_https_url(self):
		response = self.client.post("/", {"data": "https://aiesec.org/"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["qr_code"].data, "https://aiesec.org/")
		self.assertTrue(response.context["qr_code"].qr_code.storage.exists(
			response.context["qr_code"].qr_code.name
		))

	def test_post_rejects_empty_text(self):
		response = self.client.post("/", {"data": "   "})

		self.assertEqual(response.status_code, 200)
		self.assertIn("error", response.context)
		self.assertEqual(QR_code.objects.count(), 0)

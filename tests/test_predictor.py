import unittest
from unittest.mock import patch, mock_open, MagicMock
import base64

from modelstudio_sdk.predictor import ModelStudioPredictor


class TestPredictor(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("requests.post")
    def test_prediction(self, mock_post, mock_file):
        """ test the interface """
        # Set test params
        ms_url = "some-url"
        ms_key = "some-key"
        ms_timeout = 1
        fn_img = "fake_path.jpg"
        result = {"prediction": "fake_result"}
        fake_image_data = b"fake_image_data"

        expected_image_b64 = base64.b64encode(fake_image_data).decode("utf-8")
        expected_payload = {"image_b64": expected_image_b64,  "api_token": ms_key}

        # Prepare context
        mock_file.return_value.read.return_value = fake_image_data
        mock_response = MagicMock()
        mock_response.json.return_value = result
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        predictor = ModelStudioPredictor(ms_url, ms_key, timeout=ms_timeout)

        # Act
        result = predictor.predict(fn_img)

        # Test
        mock_file.assert_called_once_with(fn_img, "rb")
        mock_post.assert_called_once_with(ms_url, json=expected_payload, timeout=ms_timeout)
        self.assertEqual(result, result)

if __name__ == "__main__":
    unittest.main()
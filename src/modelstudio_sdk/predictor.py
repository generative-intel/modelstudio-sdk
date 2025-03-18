import logging
import requests
import base64
import os
import time


logger = logging.getLogger(__name__)


class ModelStudioPredictor:
    def __init__(self, url, api_key, timeout=10, max_retries=3, base_delay=2):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay

    def predict(self, image_path):
        with open(image_path, "rb") as img_file:
            image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

        payload = {
            "api_token": self.api_key,
            "image_b64": image_b64,
        }

        logger.debug("Sending request to %s for: %s", self.url, image_path)

        timeout = self.timeout

        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.url, json=payload, timeout=timeout)
                response.raise_for_status()
                logger.debug("Received response: %s", response.text)
                return response.json()

            except requests.exceptions.Timeout as err:
                timeout *= 2
                logger.error("Request timed out. Adapting timeout: %s", timeout)

            except requests.exceptions.RequestException as err:
                logger.warning("Attempt %d/%d failed: %s", attempt + 1, self.max_retries, err)

            # Retry with exponential backoff
            if attempt < self.max_retries - 1:
                sleep_time = self.base_delay * (2 ** attempt)
                logger.debug("Retrying in %d seconds", sleep_time)
                time.sleep(sleep_time)
                continue

        logger.error("Max retries reached. Request failed.")
        return {"error": f"An error occurred after {attempt} attempts."}


def read_images(image_paths):
    for image_path in image_paths:
        yield os.path.basename(image_path), image_path

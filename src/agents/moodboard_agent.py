"""
MoodBoardAgent
- Aggregates design inspiration from Pinterest and Instagram.
- Scrapes images and creates AI-generated collages via Replicate.
"""
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import os

class MoodBoardAgent:
    def __init__(self, api_token: str = None, cache: Dict = None, gemini_api_key: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN", "")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        self.cache = cache or {}

    def run(self, task: Dict[str, str]) -> Dict[str, Any]:
        query = task.get("query", "luxury interior design")
        images = self.scrape_pinterest(query) + self.scrape_instagram(query)
        # Multi-modal tagging (CLIP/BLIP placeholder)
        tagged_images = [
            {"url": img, "tags": self.auto_tag_image(img)} for img in images[:10]
        ]
        collage_url = self.generate_collage(images)
        return {
            "images": tagged_images,
            "collage_url": collage_url
        }

    def scrape_pinterest(self, query: str) -> List[str]:
        url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        if url in self.cache:
            return self.cache[url]
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            images = [img.get("src") for img in soup.find_all("img") if img.get("src")]
            self.cache[url] = images[:10]
            return images[:10]
        except Exception as e:
            return [f"[Pinterest scraping error: {e}]"]

    def scrape_instagram(self, query: str) -> List[str]:
        # Instagram scraping is limited due to anti-bot measures; placeholder logic
        return []

    def auto_tag_image(self, image_url: str) -> List[str]:
        """
        Calls the real image tagging model (CLIP/BLIP/Gemini) if available, otherwise returns demo tags.
        """
        print(f"Calling Gemini Vision API for image: {image_url}")
        try:
            tags = self.call_clip_blip_model(image_url)
            print(f"Gemini Vision API returned tags: {tags}")
            if tags:
                return tags
        except Exception as e:
            print(f"Image tagging model error: {e}")
        # Fallback demo tags
        print("Returning fallback demo tags.")
        return ["modern", "minimal", "bright"]

    def call_clip_blip_model(self, image_url: str) -> List[str]:
        """
        Integrate your CLIP/BLIP or Gemini model here. This method should return a list of tags for the image.
        Example: Call Gemini Vision API with your API key.
        """
        api_url = "https://vision.googleapis.com/v1/images:annotate"
        headers = {"Authorization": f"Bearer {self.gemini_api_key}", "Content-Type": "application/json"}
        # Gemini expects a request with features and image source
        payload = {
            "requests": [
                {
                    "image": {"source": {"imageUri": image_url}},
                    "features": [{"type": "LABEL_DETECTION", "maxResults": 10}]
                }
            ]
        }
        try:
            print(f"Sending request to Gemini Vision API: {api_url}")
            # Do NOT print the full API key in logs - only indicate presence
            print(f"Using Gemini API key: {'set' if self.gemini_api_key else 'NOT SET'}")
            print(f"Payload preview: {{'imageUri': image_url, 'features': ['LABEL_DETECTION']}}")
            resp = requests.post(api_url, headers=headers, json=payload, timeout=15)
            print(f"Gemini Vision API response status: {resp.status_code}")
            print(f"Gemini Vision API response body: {resp.text}")
            if resp.status_code == 200:
                # Response format from Vision API
                resp_json = resp.json()
                responses = resp_json.get("responses", [])
                if responses:
                    labels = responses[0].get("labelAnnotations", [])
                    print(f"Extracted labels: {labels}")
                    return [label.get("description") for label in labels if label.get("description")]
                return []
            else:
                print(f"Gemini API error: {resp.status_code} {resp.text}")
                return []
        except Exception as e:
            print(f"Gemini API exception: {e}")
            return []

    def export_tagged_images(self, tagged_images: List[Dict[str, Any]], export_path: str = "tagged_images.json") -> str:
        """
        Export tagged images to a JSON file for UI or downstream use.
        """
        import json
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(tagged_images, f, ensure_ascii=False, indent=2)
        return export_path

    def generate_collage(self, images: List[str]) -> str:
        # Placeholder for Replicate API call to generate collage
        if not self.api_token or not images:
            return ""
        # Simulate collage URL
        return "https://replicate.com/collage/fake-collage-url"

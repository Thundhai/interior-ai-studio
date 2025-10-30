"""
VisualizationAgent
- Generates 2D/3D renders and moodboards.
- Integrates with Replicate Stable Diffusion API.
- Suggests materials, colors, textures.
"""

import os
import requests
from typing import Dict, Any, List
from bs4 import BeautifulSoup


class VisualizationAgent:
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN", "")
        self.model_version = "db21e45e1c1e6b6e8a6e3c7e3e8e3c7e3e8e3c7e3e8e3c7e"  # Example version

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        prompt = task.get("prompt", "Luxury interior moodboard")
        # Real API call to Replicate Stable Diffusion
        try:
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": f"Token {self.api_token}",
                "Content-Type": "application/json"
            }
            data = {
                "version": self.model_version,
                "input": {"prompt": prompt}
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            prediction = resp.json()
            image_url = prediction.get("urls", {}).get("get", "[No image URL]")
        except Exception as e:
            image_url = f"[Replicate error: {e}]"
        # Scrape Pinterest for reference images and trending styles
        scraped = self.scrape_pinterest_inspiration(prompt)
        # Suggest materials/colors/textures (placeholder)
        return {
            "image_url": image_url,
            "scraped_images": scraped["images"],
            "trending_styles": scraped["styles"],
            "materials": ["marble", "velvet", "brass"],
            "colors": ["cream", "navy", "gold"],
            "textures": ["smooth", "matte", "glossy"]
        }

    def scrape_pinterest_inspiration(self, query: str) -> Dict[str, List[str]]:
        """
        Scrape Pinterest for room images and trending styles (public search, not API).
        Returns dict with 'images' and 'styles' (style tags found in alt text).
        """
        search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
        try:
            resp = requests.get(search_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            images = []
            styles = set()
            for img in soup.find_all("img"):
                src = img.get("src")
                alt = img.get("alt", "")
                if src and "236x" in src:  # Pinterest thumbnails
                    images.append(src)
                # Extract style tags from alt text
                for style in ["Scandinavian", "Minimalist", "Afrocentric", "Modern", "Boho", "Industrial", "Traditional"]:
                    if style.lower() in alt.lower():
                        styles.add(style)
            return {"images": images[:10], "styles": list(styles)}
        except Exception as e:
            return {"images": [], "styles": [f"[Scraping error: {e}]"]}

"""
FurnitureAdvisorAgent
- Scrapes Wayfair and IKEA for trending furniture, price ranges, and availability.
- Returns structured JSON with product info.
"""
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class FurnitureAdvisorAgent:
    def __init__(self, cache: Dict = None):
        self.cache = cache or {}

    def run(self, task: Dict[str, str]) -> Dict[str, Any]:
        return {
            "wayfair": self.scrape_wayfair(),
            "ikea": self.scrape_ikea()
        }

    def scrape_wayfair(self) -> List[Dict[str, str]]:
        url = "https://www.wayfair.com/furniture/cat/furniture-c45974.html"
        if url in self.cache:
            return self.cache[url]
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            products = []
            for item in soup.select("div.ProductCard-details"):
                title = item.find("a", class_="ProductCard-title")
                price = item.find("span", class_="ProductCard-price")
                if title and price:
                    products.append({
                        "name": title.get_text(strip=True),
                        "url": title.get("href"),
                        "price": price.get_text(strip=True)
                    })
            self.cache[url] = products[:10]
            return products[:10]
        except Exception as e:
            return [{"error": f"[Wayfair scraping error: {e}]"}]

    def scrape_ikea(self) -> List[Dict[str, str]]:
        url = "https://www.ikea.com/us/en/cat/furniture-fu001/"
        if url in self.cache:
            return self.cache[url]
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            products = []
            for item in soup.select("div.range-revamp-product-compact"):
                name = item.find("span", class_="range-revamp-header-section__title--small")
                price = item.find("span", class_="range-revamp-price__integer")
                link = item.find("a")
                if name and price and link:
                    products.append({
                        "name": name.get_text(strip=True),
                        "url": "https://www.ikea.com" + link.get("href"),
                        "price": price.get_text(strip=True)
                    })
            self.cache[url] = products[:10]
            return products[:10]
        except Exception as e:
            return [{"error": f"[IKEA scraping error: {e}]"}]

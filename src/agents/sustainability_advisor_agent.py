"""
SustainabilityAdvisorAgent
- Scrapes ArchDaily and EcoWatch for eco-friendly materials, sustainability trends, and green certifications.
- Returns structured JSON with articles and certifications.
"""
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class SustainabilityAdvisorAgent:
    def __init__(self, cache: Dict = None):
        self.cache = cache or {}

    def run(self, task: Dict[str, str]) -> Dict[str, Any]:
        topic = task.get("topic", "sustainability")
        return {
            "archdaily": self.scrape_archdaily(),
            "ecowatch": self.scrape_ecowatch()
        }

    def scrape_archdaily(self) -> List[Dict[str, str]]:
        url = "https://www.archdaily.com/search/projects/categories/sustainability"
        if url in self.cache:
            return self.cache[url]
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = []
            for item in soup.select("li.afd-search-list__item"):
                title = item.get_text(strip=True)
                link = item.find("a")
                if title and link and link.get("href"):
                    articles.append({"title": title, "url": link["href"]})
            self.cache[url] = articles[:10]
            return articles[:10]
        except Exception as e:
            return [{"error": f"[ArchDaily scraping error: {e}]"}]

    def scrape_ecowatch(self) -> List[Dict[str, str]]:
        url = "https://www.ecowatch.com/sustainable-living"
        if url in self.cache:
            return self.cache[url]
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = []
            for item in soup.select("article h2 a"):
                title = item.get_text(strip=True)
                link = item.get("href")
                if title and link:
                    articles.append({"title": title, "url": link})
            self.cache[url] = articles[:10]
            return articles[:10]
        except Exception as e:
            return [{"error": f"[EcoWatch scraping error: {e}]"}]

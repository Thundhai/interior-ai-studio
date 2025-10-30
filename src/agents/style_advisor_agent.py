"""
StyleAdvisorAgent
- Scrapes lifestyle/fashion sites for seasonal trends and color psychology articles.
- Returns trend titles, links, and color advice.
"""
import requests
from typing import List, Dict
from bs4 import BeautifulSoup

class StyleAdvisorAgent:
    def run(self, task: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
        """
        Args:
            task: dict with 'topic' (e.g., 'color psychology', 'lifestyle trends')
        Returns:
            Dict with 'trends' and 'color_psychology' lists
        """
        return {
            "trends": self.scrape_vogue_trends(),
            "color_psychology": self.scrape_color_psychology_articles()
        }

    def scrape_vogue_trends(self) -> List[Dict[str, str]]:
        """
        Scrape Vogue's fashion trends page for latest trend articles.
        """
        url = "https://www.vogue.com/fashion/trends"
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            trends = []
            for item in soup.select("article a"):  # Simplified selector
                title = item.get_text(strip=True)
                link = item.get("href")
                if title and isinstance(link, str) and link.startswith("/article"):
                    trends.append({"title": title, "url": f"https://www.vogue.com{link}"})
            return trends[:10]
        except Exception as e:
            return [{"error": f"[Scraping error: {e}]"}]

    def scrape_color_psychology_articles(self) -> List[Dict[str, str]]:
        """
        Scrape color psychology articles from verywellmind.com.
        """
        url = "https://www.verywellmind.com/color-psychology-2795824"
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = []
            for item in soup.select("a[data-analytics-link='article']"):
                title = item.get_text(strip=True)
                link = item.get("href")
                if title and isinstance(link, str) and link.startswith("/article"):
                    articles.append({"title": title, "url": f"https://www.verywellmind.com{link}"})
            return articles[:10]
        except Exception as e:
            return [{"error": f"[Scraping error: {e}]"}]

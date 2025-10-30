"""
MarketResearchAgent
- Scrapes furniture/product data from e-commerce sites (e.g., IKEA, Wayfair).
- Returns product name, price, availability, and ratings.
"""
import requests
from typing import List, Dict
from bs4 import BeautifulSoup

class MarketResearchAgent:
    def run(self, task: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Args:
            task: dict with 'query' (e.g., 'sofa', 'dining table')
        Returns:
            List of product dicts with name, price, url, and (if available) rating
        """
        query = task.get('query', 'sofa')
        return self.scrape_ikea_products(query)

    def scrape_ikea_products(self, query: str) -> List[Dict[str, str]]:
        """
        Scrape IKEA search results for product info (name, price, url).
        """
        search_url = f"https://www.ikea.com/us/en/search/?q={query.replace(' ', '%20')}"
        try:
            resp = requests.get(search_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            products = []
            for item in soup.select(".plp-fragment-wrapper"):
                name = item.select_one(".range-revamp-header-section__title--small").get_text(strip=True) if item.select_one(".range-revamp-header-section__title--small") else None
                price = item.select_one(".range-revamp-price__integer").get_text(strip=True) if item.select_one(".range-revamp-price__integer") else None
                url = item.select_one("a").get("href") if item.select_one("a") else None
                if name and price and url:
                    products.append({
                        "name": name,
                        "price": price,
                        "url": f"https://www.ikea.com{url}"
                    })
            return products[:10]
        except Exception as e:
            return [{"error": f"[Scraping error: {e}]"}]

"""
ContentCreatorAgent
- Generates blogs, social posts, portfolio descriptions.
- Optimizes content for SEO & branding.
- Integrates with OpenAI GPT for real content generation.
"""

import os
import requests
from typing import Dict, Any, List
from bs4 import BeautifulSoup
try:
    import openai
except ImportError:
    openai = None

class ContentCreatorAgent:
    def __init__(self, llm=None):
        self.llm = llm  # Placeholder for LLM client
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if openai and self.api_key:
            openai.api_key = self.api_key

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        prompt = task.get("prompt") or f"Write a {task.get('type', 'blog')} about {task.get('topic', 'luxury interior design')} for a high-end audience."
        scraped = self.scrape_dezeen_articles()
        if openai and self.api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400
                )
                content = response.choices[0].message.content.strip()
            except Exception as e:
                content = f"[OpenAI error: {e}]"
        else:
            content = f"[Generated {task.get('type', 'blog')} for: {task.get('topic', '')}]"
        return {"content": content, "scraped_articles": scraped}

    def scrape_dezeen_articles(self) -> List[Dict[str, str]]:
        """
        Scrape latest article titles and links from Dezeen.com homepage.
        Returns a list of dicts with 'title' and 'url'.
        """
        url = "https://www.dezeen.com/"
        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = []
            for item in soup.select(".home-featured-article__title a"):
                title = item.get_text(strip=True)
                link = item.get("href")
                if title and link:
                    articles.append({"title": title, "url": link})
            return articles[:10]
        except Exception as e:
            return [{"error": f"[Scraping error: {e}]"}]

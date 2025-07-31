import feedparser

def get_news_from_rss(keywords: list[str]) -> list[dict]:
    """Fetches news from RSS feeds based on a list of keywords."""
    urls = [
        "https://www.wired.com/feed/category/business/latest/rss",
        "https://feeds.arstechnica.com/arstechnica/index/",
        "http://feeds.feedburner.com/TechCrunch/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.infoq.com/feed/ai-ml-dl/",
        "https://www.zdnet.com/blog/ai/rss.xml",
        "https://venturebeat.com/category/ai/feed/",
        "https://www.techrepublic.com/rssfeeds/topic/artificial-intelligence/",
        "https://developer.nvidia.com/blog/feed/",
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/newsroom/rss.xml",
        "https://deepmind.google/blog/rss/"
    ]
    all_news = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            for keyword in keywords:
                if keyword.lower() in entry.title.lower() or (hasattr(entry, 'summary') and keyword.lower() in entry.summary.lower()):
                    all_news.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary if hasattr(entry, 'summary') else '',
                        "published": entry.published if hasattr(entry, 'published') else ''
                    })
                    break # Move to the next entry once a keyword is found
    return all_news

"""
Fetch the top 5 global news headlines and write them to README.md.

Source: BBC News - World RSS feed (no API key required).
Designed to be run daily by a GitHub Actions workflow.
"""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"
OUTPUT_FILE = "README.md"
TOP_N = 5


def fetch_top_news():
    """Fetch and parse the RSS feed, returning the top N news items."""
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        data = response.read()

    root = ET.fromstring(data)
    items = root.findall("./channel/item")[:TOP_N]

    news = []
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = (item.findtext("description") or "").strip()
        news.append(
            {
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "description": description,
            }
        )
    return news


def write_markdown(news):
    """Write the fetched news items to a Markdown file."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# Top {TOP_N} Global News — {today}", ""]

    for i, article in enumerate(news, start=1):
        lines.append(f"{i}. [{article['title']}]({article['link']})")
        if article["description"]:
            lines.append(f"   - {article['description']}")
        if article["pub_date"]:
            lines.append(f"   - Published: {article['pub_date']}")
        lines.append("")

    lines.append(f"_Last updated: {datetime.now(timezone.utc).isoformat()} UTC_")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    news = fetch_top_news()
    if not news:
        raise SystemExit("No news items were fetched — aborting.")
    write_markdown(news)
    print(f"Wrote {len(news)} articles to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

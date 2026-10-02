from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path

import feedparser
import requests
from jinja2 import Environment, PackageLoader, select_autoescape


@dataclass(frozen=True)
class Article:
    title: str
    summary: str
    link: str
    source: str
    published: str
    score: int


def keyword_score(text: str, keywords: list[str]) -> int:
    lowered = text.casefold()
    return sum(1 for keyword in keywords if keyword.strip() and keyword.casefold() in lowered)


def fetch_articles(feeds: list[str], keywords: list[str], limit: int = 20) -> list[Article]:
    articles: list[Article] = []
    seen: set[str] = set()
    for url in feeds:
        response = requests.get(url, timeout=12, headers={"User-Agent": "PersonalTechDigest/1.0"})
        response.raise_for_status()
        parsed = feedparser.parse(response.content)
        source = str(parsed.feed.get("title", url))
        for item in parsed.entries:
            link = str(item.get("link", ""))
            if not link or link in seen:
                continue
            seen.add(link)
            title = str(item.get("title", "Untitled"))
            summary = str(item.get("summary", item.get("description", "")))
            published = str(item.get("published", item.get("updated", "")))
            articles.append(Article(title, summary, link, source, published,
                                    keyword_score(f"{title} {summary}", keywords)))
    return sorted(articles, key=lambda article: (-article.score, article.published, article.title.casefold()))[:limit]


def render_html(articles: list[Article], title: str = "Your technology digest") -> str:
    env = Environment(loader=PackageLoader("tech_digest", "templates"),
                      autoescape=select_autoescape(["html", "xml"]))
    return env.get_template("digest.html").render(title=title, articles=articles)


def send_email(html_body: str, *, host: str, port: int, username: str,
               password: str, sender: str, recipient: str, timeout: float = 15) -> None:
    message = EmailMessage()
    message["Subject"] = "Your technology digest"
    message["From"] = sender
    message["To"] = recipient
    message["Date"] = formatdate(localtime=True)
    message.set_content("Your email client does not support HTML. Open the attached digest in a browser.")
    message.add_alternative(html_body, subtype="html")
    with smtplib.SMTP_SSL(host, port, timeout=timeout) as server:
        server.login(username, password)
        server.send_message(message)

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from .digest import fetch_articles, render_html, send_email


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Create a local RSS digest, optionally send it by email.")
    parser.add_argument("--feed", action="append", required=True)
    parser.add_argument("--keywords", default="python,ai,security")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--html", type=Path, default=Path("digest.html"))
    parser.add_argument("--send", action="store_true", help="send using SMTP settings in .env")
    args = parser.parse_args(argv)
    try:
        articles = fetch_articles(args.feed, [word.strip() for word in args.keywords.split(",")], args.limit)
        document = render_html(articles)
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(document, encoding="utf-8")
        if args.send:
            settings = {key: os.getenv(key, "") for key in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "EMAIL_FROM", "EMAIL_TO")}
            if not all(settings.values()):
                raise ValueError("SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, and EMAIL_TO are required with --send")
            send_email(document, host=settings["SMTP_HOST"], port=int(os.getenv("SMTP_PORT", "465")),
                       username=settings["SMTP_USER"], password=settings["SMTP_PASSWORD"],
                       sender=settings["EMAIL_FROM"], recipient=settings["EMAIL_TO"])
    except Exception as error:
        parser.error(str(error))
    print(f"Rendered {len(articles)} article(s) to {args.html}" + (" and sent email." if args.send else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

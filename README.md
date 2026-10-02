# Personal Tech Daily Digest

Collect articles from the RSS/Atom feeds you choose, rank them by topic keywords, render an HTML email, and optionally deliver it through SMTP. It can also save the HTML locally without sending anything.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
tech-digest --feed https://news.ycombinator.com/rss --keywords python,ai,security --html digest.html
```

To send, copy `.env.example` to `.env`, fill in your SMTP app credentials, then add `--send`. Prefer an app password or dedicated mail account, keep `.env` private, and do not use your normal account password.

## Privacy and behavior

Network fetching happens only for feed URLs you provide. Email sending happens only with the explicit `--send` flag. Feed text is treated as untrusted and escaped by the HTML template.

## Learning notes

Practice RSS parsing, simple relevance scoring, Jinja templates, MIME email composition, SMTP over TLS, and keeping the message-sending step opt-in.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).

from tech_digest.digest import Article, keyword_score, render_html


def test_keyword_score_counts_matching_terms():
    assert keyword_score("Python security news", ["python", "security", "ai"]) == 2


def test_template_escapes_untrusted_article_titles():
    page = render_html([Article("<script>alert(1)</script>", "summary", "https://example.org", "feed", "", 1)])
    assert "&lt;script&gt;" in page

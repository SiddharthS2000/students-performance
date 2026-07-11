from html import escape


def sanitize_text(value: str | None) -> str:
    text = value or ""
    try:
        from bleach import clean

        return clean(text, tags=[], attributes={}, strip=True)
    except ModuleNotFoundError:
        return escape(text)

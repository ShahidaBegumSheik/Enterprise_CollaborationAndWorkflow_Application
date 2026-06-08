import bleach


def clean_text(value: str | None):
    if value is None:
        return None

    return bleach.clean(value.strip(), tags=[], attributes={}, strip=True)


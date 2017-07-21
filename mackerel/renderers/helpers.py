from markupsafe import Markup


def strip_tags(text: str) -> str:
    """Strip the html tags of the given string."""
    return Markup(text).striptags()

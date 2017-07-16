class MackerelError(Exception):
    """Base class for mackerel's exceptions"""


class DocumentError(MackerelError):
    """Exception raised for errors in the content document"""


class RenderingError(MackerelError):
    """Exception raised for rendering errors"""

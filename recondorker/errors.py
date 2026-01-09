class ReconDorkerError(Exception):
    """Base exception for ReconDorker"""
    pass

class SearchError(ReconDorkerError):
    """Raised when search fails"""
    pass

class RateLimitError(SearchError):
    """Raised when rate limited by search engine"""
    pass

class CaptchaError(SearchError):
    """Raised when a Captcha is detected"""
    pass

class ParsingError(ReconDorkerError):
    """Raised when results cannot be parsed"""
    pass

import playwright.sync_api
from playwright.sync_api import Page

# we use a global playwright instance
_PLAYWRIGHT = None
BROWSERGYM_ID_ATTRIBUTE = "bid"  # Playwright's default is "data-testid", see: get_by_test_id


def _get_global_playwright() -> playwright.sync_api.Playwright:
    # This is important because sometimes we have two different sessions on the same machine
    # e.g. (APIGated) Browser and LocalChatSession, but sync playwright can only be started once as the second
    # instance would already have an async loop taken by the first
    global _PLAYWRIGHT
    if not _PLAYWRIGHT:
        _PLAYWRIGHT = playwright.sync_api.sync_playwright().start()

    # IMPORTANT: change playwright's test id attribute from "data-testid" to "bid"
    # This is used to identify elements in the browser by get_by_test_id
    _PLAYWRIGHT.selectors.set_test_id_attribute(BROWSERGYM_ID_ATTRIBUTE)
    return _PLAYWRIGHT


def connect_to_local_session(host: str, port: int) -> Page:
    pw = _get_global_playwright()
    chromium = pw.chromium
    browser2 = chromium.connect_over_cdp(f"http://{host}:{port}")
    context2, = browser2.contexts
    page, = context2.pages
    return page

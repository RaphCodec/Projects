from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://insideairbnb.com/get-the-data/")
    with page.expect_download() as download_info:
        page.get_by_role("row", name="Amsterdam listings.csv.gz Detailed Listings data").get_by_role("link").click()
    download = download_info.value
    download.save_as('test.csv.gz')

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

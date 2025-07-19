import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

async def scrape_chapter():
    print("🚀 Starting scrape from Wikisource...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        print("🌐 Page loaded:", URL)

        await page.screenshot(path="chapter_1.png", full_page=True)
        print("📸 Screenshot saved: chapter_1.png")

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        print("❌ Could not find 'mw-parser-output'")
        return

    paragraphs = content_div.find_all("p")
    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    if not text:
        print("❌ No paragraph text found")
        return

    with open("chapter_1.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Chapter content saved: chapter_1.txt")

if __name__ == "__main__":
    asyncio.run(scrape_chapter())

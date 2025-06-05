from playwright.sync_api import sync_playwright
import pandas as pd
import time
import asyncio

async def scrape_tokopedia_reviews_async():
    from playwright.async_api import async_playwright
    
    url = "https://play.google.com/store/apps/details?id=com.tokopedia.tkpd&hl=id"
    data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        
        try:
            # Wait for and click the "See all reviews" button
            see_all_button = await page.wait_for_selector("//button[.//span[text()='Lihat semua ulasan']]", timeout=10000)
            await see_all_button.click()
            print("Tombol 'See all reviews' berhasil diklik.")
            
        except Exception as e:
            print("Gagal klik tombol:", e)
            await browser.close()
            return
        
        # Wait for the scrollable div to appear
        await page.wait_for_selector('div[jsname="bN97Pc"]', timeout=10000)
        
        # Scroll within the reviews popup
        scroll_count = 2
        
        for i in range(scroll_count):
            await page.evaluate('''
                const scrollableDiv = document.querySelector('div[jsname="bN97Pc"]');
                if (scrollableDiv) {
                    scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
                }
            ''')
            print(f"Scroll ke-{i+1} di dalam pop-up")
            await page.wait_for_timeout(1000)  # 1 second delay
        
        # Extract review data
        containers = await page.query_selector_all('div.RHo1pe')
        
        for container in containers:
            try:
                # Extract review text
                review_element = await container.query_selector('div.h3YV2d')
                review = await review_element.inner_text() if review_element else ""
                
                # Extract rating
                rating_div = await container.query_selector('div.iXRFPc')
                if rating_div:
                    rating_text = await rating_div.get_attribute('aria-label')
                    rating = int(rating_text.split(' ')[2]) if rating_text else 0
                else:
                    rating = 0
                
                # Extract date
                date_span = await container.query_selector('span.bp9Aid')
                review_date = await date_span.inner_text() if date_span else ""
                review_date = review_date.strip()
                
                if review and rating and review_date:
                    data.append((review_date, rating, review))
                    
            except (AttributeError, ValueError, IndexError):
                continue
        
        print(f"{len(data)} reviews collected.")
        
        # Save to CSV
        df = pd.DataFrame(data, columns=['Date', 'Rating', 'Review'])
        df.to_csv('tokped_reviews.csv', index=False, encoding='utf-8-sig')
        
        await browser.close()
        
        return data

# Run the scraper
if __name__ == "__main__":
    
    # Or use async version (uncomment below and comment above)
    # 
    reviews = asyncio.run(scrape_tokopedia_reviews_async())
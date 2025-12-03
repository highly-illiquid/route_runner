from playwright.async_api import async_playwright, Page
from src.models import BillOfLading
import asyncio

class PortalBot:
    def __init__(self):
        # Credentials would typically come from env vars too
        # self.portal_user = os.environ.get("PORTAL_USER")
        pass

    async def upload_invoice(self, data: BillOfLading):
        """
        Launches a headless browser, logs in, and enters the invoice data.
        """
        async with async_playwright() as p:
            # Launch browser (headless=True for serverless/CI)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await self.login(page)
                await self.navigate_to_create(page)
                await self.fill_form(page, data)
                await self.submit(page)
                print(f"Successfully uploaded BOL: {data.shippers_bol_number}")
                
            except Exception as e:
                print(f"Browser Automation Error for {data.shippers_bol_number}: {e}")
                # Take a screenshot for debugging if something fails
                # await page.screenshot(path=f"error_{data.shippers_bol_number}.png")
                raise e
            finally:
                await browser.close()

    async def login(self, page: Page):
        # TODO: Replace with actual URL and selectors
        print("  Logging in...")
        # await page.goto("https://portal.infocon.com/login")
        # await page.fill("#username", "myuser")
        # await page.fill("#password", "mypass")
        # await page.click("button[type=submit]")
        # await page.wait_for_selector("#dashboard")
        await asyncio.sleep(1) # Mock delay

    async def navigate_to_create(self, page: Page):
        print("  Navigating to 'Create Invoice'...")
        # await page.click("text=New Invoice")
        await asyncio.sleep(0.5)

    async def fill_form(self, page: Page, data: BillOfLading):
        print(f"  Filling form for BOL {data.shippers_bol_number}...")
        
        # Example of how filling would look:
        # await page.fill("#bol_field", data.shippers_bol_number)
        # await page.fill("#date_field", data.date)
        # await page.fill("#shipper_field", data.company_name_from)
        
        # Handling dynamic rows (Line Items)
        for i, item in enumerate(data.shipment_details):
            # Assume there's an 'Add Row' button for subsequent items
            if i > 0:
                # await page.click("#add_row_btn")
                pass
                
            # Selectors would likely use index, e.g., name="desc_0", name="desc_1"
            print(f"    - Item: {item.description} | {item.pieces} pcs | {item.weight}")
            # await page.fill(f"input[name='desc_{i}']", item.description)
            # await page.fill(f"input[name='pcs_{i}']", str(item.pieces))
            # await page.fill(f"input[name='wgt_{i}']", item.weight)

    async def submit(self, page: Page):
        print("  Submitting form...")
        # await page.click("#save_button")
        # await page.wait_for_selector(".success-toast")
        await asyncio.sleep(1)
"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
"© 2026 Punksm4ck. All rights reserved."
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright

app = FastAPI(title="AEGIS Shadow-Apply Engine v2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApplicationPayload(BaseModel):
    job_id: str
    job_url: str
    target_platform: str

async def handle_usajobs(page, url):
    print(f"[AEGIS] Engaging USAJOBS Federal Protocol...")
    await page.goto(url)

    apply_btn = page.locator("a[id='joa-apply-button'], button:has-text('Apply')").first
    if await apply_btn.is_visible():
        await apply_btn.click()
        print("[AEGIS] Initiated USAJOBS handoff. Pausing for Login.gov auth...")

        await asyncio.sleep(5)
        return True
    return False

async def handle_adzuna_redirects(page, url):
    print(f"[AEGIS] Tracing Adzuna redirect path...")
    await page.goto(url, wait_until="networkidle")

    # Loop to handle intermediary Adzuna pages until we leave the domain
    attempts = 0
    while "adzuna.com" in page.url and attempts < 3:
        print(f"[AEGIS] Currently on: {page.url}")
        apply_btn = page.locator("a:has-text('Apply on company site'), a.apply-button, .ad-details__apply-button").first

        if await apply_btn.is_visible():
            print("[AEGIS] Adzuna Details page detected. Force-clicking redirect...")
            # Using dispatch_event to bypass potential overlay blocks
            await apply_btn.dispatch_event("click")
            # Wait for the navigation to a different domain
            try:
                await page.wait_for_url(lambda u: "adzuna.com" not in u, timeout=5000)
            except:
                pass
        attempts += 1

    current_url = page.url
    print(f"[AEGIS] Final destination reached: {current_url}")

    if any(x in current_url for x in ["greenhouse.io", "lever.co", "workday", "icims"]):
        print(f"[AEGIS] Recognized ATS detected: {current_url}")
        return True
    elif "adzuna.com" not in current_url:
        print(f"[AEGIS] Custom employer portal detected: {current_url}")
        return True

    print("[AEGIS] Failed to break out of Adzuna redirect loop.")
    return False

async def execute_headless_apply(payload: ApplicationPayload):
    print(f"\n[AEGIS TELEMETRY] Spawning shadow instance for {payload.target_platform}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            success = False
            if payload.target_platform == "USAJobs":
                success = await handle_usajobs(page, payload.job_url)
            elif payload.target_platform == "Adzuna":
                success = await handle_adzuna_redirects(page, payload.job_url)
            else:
                print(f"[AEGIS] Platform {payload.target_platform} not yet mapped.")

            if success:
                print(f"[AEGIS] Shadow-Apply sequence completed for {payload.job_id}.")
                return {"status": "success", "job_id": payload.job_id}
            else:
                return {"status": "error", "reason": "Failed to map target DOM elements."}

        except Exception as e:
            print(f"[AEGIS] Shadow-Apply critical failure: {str(e)}")
            return {"status": "error", "reason": str(e)}
        finally:
            await asyncio.sleep(3)
            await browser.close()

@app.post("/api/shadow-apply")
async def trigger_shadow_apply(payload: ApplicationPayload):
    asyncio.create_task(execute_headless_apply(payload))
    return {"message": "AEGIS Telemetry Received: Shadow-Apply initiated.", "job_id": payload.job_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3457)

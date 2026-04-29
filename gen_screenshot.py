from playwright.sync_api import sync_playwright
import subprocess
import time

server = subprocess.Popen(
    ['python3', '-m', 'http.server', '8766'],
    cwd='/root/.openclaw2/workspace',
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    )
    context = browser.new_context(
        viewport={'width': 480, 'height': 1600},
        device_scale_factor=3
    )
    page = context.new_page()
    page.goto('http://localhost:8766/hn-consulting-article-phone.html', wait_until='networkidle')
    page.wait_for_timeout(3000)
    output = '/root/.openclaw/media/qqbot/downloads/article_long.png'
    page.screenshot(path=output, full_page=True, type='png')
    print(f"Saved: {output}")
    browser.close()

server.terminate()

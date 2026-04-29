from playwright.sync_api import sync_playwright
import subprocess
import time

server = subprocess.Popen(
    ['python3', '-m', 'http.server', '8767'],
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
        viewport={'width': 520, 'height': 1600},
        device_scale_factor=3
    )
    page = context.new_page()
    page.goto('http://localhost:8767/hn-review-article-phone.html', wait_until='networkidle')
    page.wait_for_timeout(3000)
    output = '/root/.openclaw/media/qqbot/downloads/review_article_final.png'
    page.screenshot(path=output, full_page=True, type='png')
    print(f"Saved PNG: {output}")
    browser.close()

server.terminate()

# Convert to optimized JPG
from PIL import Image
img = Image.open('/root/.openclaw/media/qqbot/downloads/review_article_final.png')
w, h = img.size
print(f"PNG size: {w}x{h}")
new_w = 1080
new_h = int(h * (new_w / w))
resized = img.resize((new_w, new_h), Image.LANCZOS).convert('RGB')
out_jpg = '/root/.openclaw/media/qqbot/downloads/review_article_final.jpg'
resized.save(out_jpg, 'JPEG', quality=92, optimize=True)
print(f"JPG saved: {new_w}x{new_h}")

#!/usr/bin/env python3
"""
Finviz Map Canvas Screenshot - Playwright Version
使用 Playwright 替代 Selenium，提供更好的 headless 模式支援
"""

import argparse
import sys
import subprocess
import time
import os
import io
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_dependencies():
    """Check if required packages are installed, install if not."""
    packages = []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        packages.append("playwright")
    
    try:
        from PIL import Image
    except ImportError:
        packages.append("Pillow")

    if packages:
        print(f"📦 Installing required packages: {', '.join(packages)}...")
        install_cmd = [sys.executable, "-m", "pip", "install"]
        if sys.platform != 'win32':
            install_cmd.append("--break-system-packages")
        install_cmd.extend(packages)
        subprocess.run(install_cmd, check=True)
        
        # Install Playwright browsers
        if "playwright" in packages:
            print("📦 Installing Playwright browsers...")
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def capture_finviz_canvas_playwright(map_type="sec", output_path="spy.png", headless=True):
    """
    Capture Finviz map canvas element as screenshot using Playwright.

    Args:
        map_type: Type of map (sec, world, etf, crypto)
        output_path: Path to save the screenshot
        headless: Run in headless mode (default: True)

    Returns:
        True if successful, False otherwise
    """
    check_dependencies()

    from playwright.sync_api import sync_playwright
    from PIL import Image
    import io as iolib

    # Map type URLs
    map_urls = {
        "sec": "https://finviz.com/map.ashx",
        "world": "https://finviz.com/map.ashx?t=geo",
        "etf": "https://finviz.com/map.ashx?t=etf",
        "crypto": "https://finviz.com/map.ashx?t=crypto"
    }

    url = map_urls.get(map_type, map_urls["sec"])

    print(f"📊 Finviz Canvas Screenshot (Playwright)")
    print(f"Map type: {map_type}")
    print(f"URL: {url}")
    print(f"Output: {output_path}")
    print(f"Headless: {headless}\n")

    try:
        with sync_playwright() as p:
            # Launch browser with anti-detection settings
            print("🔧 Launching Chromium browser...")
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                ]
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation'],
                color_scheme='dark',
            )
            
            # Additional anti-detection measures
            context.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Mock languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """)
            
            page = context.new_page()
            
            # Navigate to Finviz map
            print("🌐 Loading Finviz map page...")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Wait for Cloudflare verification
            print("⏳ Waiting for Cloudflare verification (45 seconds)...")
            time.sleep(45)
            
            # Check if page loaded successfully
            try:
                page_title = page.title()
                print(f"✓ Page loaded: {page_title}")
            except:
                print("⚠️  Could not get page title")
            
            # Wait for canvas element
            print("🔍 Looking for canvas element...")
            try:
                # Try multiple selectors
                canvas = page.wait_for_selector(
                    'canvas, #canvas-wrapper canvas, .canvas-wrapper canvas',
                    timeout=20000
                )
                print("✓ Found canvas element")
            except:
                print("❌ Could not find canvas element")
                browser.close()
                return False
            
            # Scroll canvas into view
            canvas.scroll_into_view_if_needed()
            time.sleep(2)
            
            # Clear any hover effects
            print("🧹 Clearing hover effects and tooltips...")
            page.evaluate("""
                // Hide all high z-index elements (tooltips, popups)
                document.querySelectorAll('*').forEach(el => {
                    const style = window.getComputedStyle(el);
                    const zIndex = parseInt(style.zIndex) || 0;
                    if (zIndex > 100) {
                        el.style.display = 'none';
                    }
                });
                
                // Trigger mouseout on canvas
                const canvas = document.querySelector('canvas');
                if (canvas) {
                    const event = new MouseEvent('mouseout', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    canvas.dispatchEvent(event);
                }
            """)
            time.sleep(2)
            
            # Move mouse away from canvas
            page.mouse.move(10, 10)
            time.sleep(1)
            
            # Take screenshot of canvas element
            print("📸 Capturing canvas screenshot...")
            canvas_screenshot = canvas.screenshot(type='png')
            
            # Save screenshot
            with open(output_path, 'wb') as f:
                f.write(canvas_screenshot)
            
            file_size = os.path.getsize(output_path)
            print(f"✓ Screenshot saved: {output_path}")
            print(f"✓ File size: {file_size:,} bytes")
            
            # Clean up
            browser.close()
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_html(html_path, png_filename="spy.png", map_type="sec"):
    """Create simple HTML to display the screenshot."""
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finviz Market Map</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
    </style>
</head>
<body>
    <img src="{png_filename}" alt="Finviz Market Map">
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML created: {html_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Capture Finviz map canvas as screenshot using Playwright"
    )
    parser.add_argument(
        "-t", "--type",
        default="sec",
        choices=["sec", "world", "etf", "crypto"],
        help="Map type (default: sec)"
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Don't create HTML file, only save screenshot"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run with visible browser (for debugging)"
    )

    args = parser.parse_args()

    # Output paths - root directory
    script_dir = Path(__file__).parent.parent.parent.parent

    # Map type to filename mapping
    filename_map = {
        "sec": "spy.png",      # S&P 500 -> SPY ETF ticker
        "world": "world.png",
        "etf": "etf.png",
        "crypto": "crypto.png"
    }

    # Generate filename based on map type
    png_filename = filename_map.get(args.type, f"{args.type}.png")
    png_path = script_dir / png_filename
    html_path = script_dir / "index.html"
    
    print(f"📁 Output directory: {script_dir}\n")

    # Capture canvas screenshot
    headless = not args.no_headless
    success = capture_finviz_canvas_playwright(args.type, str(png_path), headless=headless)

    if not success:
        print("\n❌ Failed to capture screenshot")
        sys.exit(1)

    # Create HTML if requested
    if not args.no_html:
        print()
        create_html(str(html_path), png_filename, args.type)

    print(f"\n🎉 Done!")
    print(f"✓ PNG: {png_path}")
    if not args.no_html:
        print(f"✓ HTML: {html_path}")
        print(f"\n📖 Open {html_path} in your browser to view the map.")

    sys.exit(0)


if __name__ == "__main__":
    main()

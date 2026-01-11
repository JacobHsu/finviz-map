#!/usr/bin/env python3
"""
Finviz Map Canvas Screenshot
直接截取 Finviz 地圖的 canvas 元素並保存為圖片
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
        import undetected_chromedriver
    except ImportError:
        packages.append("undetected-chromedriver")
    
    try:
        from PIL import Image
    except ImportError:
        packages.append("Pillow")

    if packages:
        print(f"Installing required packages: {', '.join(packages)}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages"] + packages,
            check=True
        )


def capture_finviz_canvas(map_type="sec", output_path="spy.png", headless=False):
    """
    Capture Finviz map canvas element as screenshot.

    Args:
        map_type: Type of map (sec, world, etf, crypto)
        output_path: Path to save the screenshot
        headless: Run in headless mode (for CI/CD environments)

    Returns:
        True if successful, False otherwise
    """
    check_dependencies()

    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from PIL import Image
    import io as iolib

    # Setup Chrome options
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Headless mode for CI/CD environments
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-extensions")
    else:
        options.add_argument("--start-maximized")

    # Map type URLs
    map_urls = {
        "sec": "https://finviz.com/map.ashx",
        "world": "https://finviz.com/map.ashx?t=geo",
        "etf": "https://finviz.com/map.ashx?t=etf",
        "crypto": "https://finviz.com/map.ashx?t=crypto"
    }

    url = map_urls.get(map_type, map_urls["sec"])

    print(f"📊 Finviz Canvas Screenshot")
    print(f"Map type: {map_type}")
    print(f"URL: {url}")
    print(f"Output: {output_path}\n")

    driver = None
    try:
        # Initialize Chrome driver
        print("🔧 Initializing Chrome driver...")
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
        
        # Navigate to Finviz map
        print("🌐 Loading Finviz map page...")
        driver.get(url)

        # Wait for Cloudflare
        print("⏳ Waiting for Cloudflare verification (35-40 seconds)...")
        time.sleep(40)

        # Check page loaded
        try:
            page_title = driver.title
            print(f"✓ Page loaded: {page_title}")
        except:
            print("⚠️  Could not get page title")

        # Wait for canvas element
        print("🔍 Looking for canvas element...")
        canvas = None
        
        # Try to find canvas-wrapper or canvas element
        try:
            # Method 1: Find by ID or class
            canvas = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#canvas-wrapper canvas, .canvas-wrapper canvas, canvas"))
            )
            print("✓ Found canvas element")
        except:
            print("⚠️  Could not find canvas element, trying alternative...")
            try:
                canvas = driver.find_element(By.TAG_NAME, "canvas")
                print("✓ Found canvas by tag name")
            except:
                raise Exception("Could not find canvas element")

        # Scroll to canvas
        driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
        time.sleep(2)

        # Clear any hover effects and tooltips
        print("🧹 Clearing hover effects and tooltips...")

        # Aggressively hide all overlay elements with JavaScript
        driver.execute_script("""
            // Remove all absolute/fixed positioned elements that might be tooltips
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                const position = style.position;
                const zIndex = parseInt(style.zIndex) || 0;

                // Hide high z-index elements (likely popups/tooltips)
                if (zIndex > 100) {
                    el.style.display = 'none';
                }

                // Hide elements with tooltip-like properties
                if (position === 'absolute' || position === 'fixed') {
                    const classes = el.className.toString().toLowerCase();
                    const id = el.id.toString().toLowerCase();
                    if (classes.includes('tooltip') || classes.includes('popup') ||
                        classes.includes('info') || classes.includes('detail') ||
                        id.includes('tooltip') || id.includes('popup')) {
                        el.style.display = 'none';
                    }
                }
            });

            // Also try to trigger mouseout events on canvas
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

        # Move mouse completely off the canvas area
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(driver)
        # Move to page header (far from canvas)
        try:
            header = driver.find_element(By.TAG_NAME, "header")
            actions.move_to_element(header).perform()
        except:
            # If no header, move to top-left
            body = driver.find_element(By.TAG_NAME, "body")
            actions.move_to_element_with_offset(body, 5, 5).perform()

        time.sleep(2)

        # Get canvas screenshot
        print("📸 Capturing canvas screenshot...")
        
        # Method 1: Try element screenshot
        try:
            canvas_png = canvas.screenshot_as_png
            
            # Save the image
            with open(output_path, 'wb') as f:
                f.write(canvas_png)
            
            file_size = os.path.getsize(output_path)
            print(f"✓ Screenshot saved: {output_path}")
            print(f"✓ File size: {file_size:,} bytes")
            
            # Clean up
            try:
                driver.quit()
                driver = None
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"⚠️  Element screenshot failed: {e}")
            print("📸 Trying full page screenshot...")
            
            # Method 2: Full page screenshot and crop
            screenshot_png = driver.get_screenshot_as_png()
            
            # Get canvas location and size
            location = canvas.location
            size = canvas.size
            
            # Open screenshot with PIL
            image = Image.open(iolib.BytesIO(screenshot_png))
            
            # Crop to canvas area
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            
            canvas_image = image.crop((left, top, right, bottom))
            
            # Save cropped image
            canvas_image.save(output_path)
            
            file_size = os.path.getsize(output_path)
            print(f"✓ Screenshot saved (cropped): {output_path}")
            print(f"✓ File size: {file_size:,} bytes")
            
            # Clean up
            try:
                driver.quit()
                driver = None
            except:
                pass
            
            return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


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
        description="Capture Finviz map canvas as screenshot"
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
        "--headless",
        action="store_true",
        help="Run in headless mode (for CI/CD environments)"
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
    success = capture_finviz_canvas(args.type, str(png_path), headless=args.headless)

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

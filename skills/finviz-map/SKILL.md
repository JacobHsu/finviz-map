---
name: finviz-map
description: Capture Finviz market map screenshots and save them as PNG images. Use this skill when the user wants to download Finviz market map visualizations. Supports S&P 500 sectors, world markets, ETFs, and cryptocurrency maps.
---

# Finviz Market Map Screenshot Tool

Automatically capture Finviz.com market maps as high-quality PNG screenshots and optionally create HTML files to display them.

## Quick Start

The simplest way to capture the S&P 500 map and create an HTML file:

```bash
python scripts/capture_canvas.py
```

This will:
1. Capture the current S&P 500 sector map from Finviz
2. Save it as `spy.png` in the project root directory
3. Create an `index.html` file to display the map

## Options

### Map Types

Use `-t` or `--type` to specify which map to capture:

- `sec` (default): S&P 500 stocks by sector and industry
- `world`: Global markets by country
- `etf`: Exchange-traded funds
- `crypto`: Cryptocurrency market

Example:
```bash
python scripts/capture_canvas.py -t world
```

### Skip HTML Creation

Use `--no-html` to only save the PNG screenshot without creating an HTML file:

```bash
python scripts/capture_canvas.py --no-html
```

This will save only the PNG file without generating the accompanying HTML viewer.

## Complete Examples

1. Capture S&P 500 map with HTML:
```bash
python scripts/capture_canvas.py
```

2. Capture world markets map:
```bash
python scripts/capture_canvas.py -t world
```

3. Capture cryptocurrency map without HTML:
```bash
python scripts/capture_canvas.py -t crypto --no-html
```

4. Capture ETF map:
```bash
python scripts/capture_canvas.py -t etf
```

## How It Works

The skill uses undetected-chromedriver to:
1. Navigate to the Finviz map page
2. Wait for Cloudflare verification to complete (35-40 seconds)
3. Locate the canvas element containing the market map
4. Capture a screenshot of the canvas element
5. Save the screenshot as a PNG file (named by map type: `spy.png`, `world.png`, etc.)
6. Optionally create an HTML file to display the image

**Output Files:**
- **PNG Screenshot**: Saved in the project root directory, named by map type (e.g., `spy.png`, `world.png`)
- **HTML Viewer** (optional): Simple, dark-themed HTML file (`index.html`) that displays the PNG image

The generated HTML file includes:
- Responsive design that centers the image
- Dark background (#000) for better viewing
- Simple, clean styling with no external dependencies

## Requirements

- **undetected-chromedriver**: Automatically installed if not present
- **Pillow (PIL)**: Automatically installed if not present for image processing
- **Chrome/Chromium**: Required for the browser automation

**Note**: This script will open a visible Chrome window (not headless mode) to bypass Cloudflare protection that Finviz uses. The window will close automatically after the screenshot is captured.

## Important Notes

- The script opens a visible Chrome window for 35-40 seconds (to bypass Cloudflare)
- Screenshots capture the current market data at the time of execution
- PNG files are saved in the project root directory
- File naming: `spy.png` (S&P 500), `world.png`, `etf.png`, or `crypto.png` based on map type
- Images are high-resolution canvas captures
- Maps show real-time market data from Finviz
- Color coding: Green = gains, Red = losses
- HTML file is always named `index.html` and references the appropriate PNG file

## Map Types Explained

### S&P 500 Sectors (`sec`)
- Shows all S&P 500 stocks grouped by sector and industry
- Size represents market capitalization
- Color represents daily performance

### World Markets (`world`)
- Global stock market performance by country
- Size represents market size
- Color represents daily performance

### ETFs (`etf`)
- Exchange-traded fund performance
- Grouped by category
- Shows sector and strategy ETFs

### Cryptocurrency (`crypto`)
- Major cryptocurrency performance
- Size represents market cap
- Color represents 24-hour price change

## Troubleshooting

**Cloudflare verification issues:**
- The script will open a visible Chrome window to bypass Cloudflare
- Wait for the browser window to complete the verification (usually 35-40 seconds)
- The window will close automatically after screenshot is captured

**Screenshot capture fails:**
- Check your internet connection
- Finviz may be temporarily unavailable
- Try increasing the wait time in the script if Cloudflare takes longer to verify
- Try running the script again - sometimes it works on the second attempt

**Canvas element not found:**
- The script will try multiple methods to locate the canvas element
- If the first method fails, it will automatically fall back to alternative approaches
- The browser window may stay open longer if fallback methods are needed

**Browser window appears and disappears quickly:**
- This is normal - the script runs quickly once Cloudflare verification passes
- The screenshot will be saved even if the window closes fast

**Permission errors:**
- Ensure the project root directory is writable
- On Windows, avoid running from system-protected directories

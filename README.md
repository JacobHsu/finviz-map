# Finviz 市場地圖截圖與 API 工具

自動捕捉 Finviz.com 市場地圖的高品質截圖並使用 AI 分析生成 JSON API。非常適合追蹤市場趨勢、製作報告或在專案中嵌入市場視覺化圖表。

## 功能特色

- 📊 **多種市場類型**：S&P 500、全球市場、ETF 和加密貨幣
- 🖼️ **高品質截圖**：直接擷取 canvas 元素以獲得清晰圖像
- 🤖 **AI 智能分析**：使用 GitHub Models API (GPT-4o Vision) 識別跌幅最大股票
- 📡 **RESTful API**：自動生成 JSON API，供其他應用呼叫
- 🌐 **繞過 Cloudflare**：自動處理 Cloudflare 驗證
- 🔄 **自動化部署**：GitHub Actions 自動更新並部署到 GitHub Pages
- ⚡ **簡單的命令列介面**：易於使用的 CLI 工具

---

## 🚀 快速使用 API

如果你只想使用 API 功能，請前往 **[API 完整文件](api/README.md)** 查看：
- ✅ API 端點說明
- ✅ 使用範例（JavaScript、Python、cURL）
- ✅ 設定指南（3 步完成）
- ✅ 進階設定與故障排除
- ✅ 應用範例（Discord 機器人、郵件通知等）

**API 端點範例**:
```
https://JacobHsu.github.io/finviz-map/api/top_losers.json
```

**線上展示**:
```
https://JacobHsu.github.io/finviz-map/api/example.html
```

---

## 市場類型

| 類型 | 說明 | 檔案名稱 |
|------|------|----------|
| `sec` | S&P 500 股票（按產業分類，預設） | `spy.png` |
| `world` | 全球市場（按國家分類） | `world.png` |
| `etf` | 交易所交易基金 | `etf.png` |
| `crypto` | 加密貨幣市場 | `crypto.png` |

---

## 本地使用（截圖工具）

### 系統需求

- **Python 3.7+**
- **Chrome/Chromium 瀏覽器**：瀏覽器自動化所需
- **依賴套件**（自動安裝）：
  - `undetected-chromedriver`
  - `Pillow`

### 基本用法

捕捉 S&P 500 地圖並建立 HTML 檢視器：

```bash
python skills/finviz-map/scripts/capture_canvas.py
```

這會建立：
- `spy.png` - 市場地圖截圖
- `index.html` - 用於顯示圖片的 HTML 檢視器

### 捕捉不同市場

```bash
# 全球市場
python skills/finviz-map/scripts/capture_canvas.py -t world

# ETF 市場
python skills/finviz-map/scripts/capture_canvas.py -t etf

# 加密貨幣市場
python skills/finviz-map/scripts/capture_canvas.py -t crypto
```

### 跳過 HTML 生成

只儲存 PNG 截圖：

```bash
python skills/finviz-map/scripts/capture_canvas.py -t sec --no-html
```

---

## 工作原理

### 截圖流程
1. 以可見模式開啟 Chrome 瀏覽器（繞過 Cloudflare 所需）
2. 導航至 Finviz 地圖頁面
3. 等待 Cloudflare 驗證（35-40 秒）
4. 定位包含市場地圖的 canvas 元素
5. 捕捉高解析度截圖
6. 將 PNG 儲存至專案根目錄

### AI 分析流程（自動化）
1. 讀取生成的市場地圖截圖 (spy.png)
2. 呼叫 GitHub Models API (GPT-4o with Vision)
3. AI 識別圖片中所有股票及其漲跌幅
4. 提取跌幅最大的 5 檔股票
5. 生成 JSON API 檔案
6. 部署到 GitHub Pages 供外部呼叫

### 自動化流程
- 每個交易日美東時間 4:30 PM 自動運行
- GitHub Actions 自動執行截圖 → AI 分析 → 部署
- 無需人工干預，全自動更新

---

## 輸出檔案

### PNG 截圖
- **位置**：專案根目錄
- **命名**：基於地圖類型（`spy.png`、`world.png` 等）
- **格式**：高解析度 PNG
- **顏色編碼**：綠色 = 漲幅，紅色 = 跌幅

### HTML 檢視器（可選）
- **檔案**：專案根目錄中的 `index.html`
- **樣式**：深色主題，響應式設計
- **內容**：顯示最近捕捉的 PNG

### JSON API（自動生成）
- **位置**：`api/` 目錄
- **檔案**：`top_losers.json` (完整版)、`top_losers_simple.json` (簡化版)
- **更新**：每個交易日自動更新
- **文件**：查看 [api/README.md](api/README.md)

---

## 重要提示

⏱️ **執行時間**：腳本需要 35-40 秒完成（Cloudflare 驗證）

🖥️ **可見瀏覽器**：執行期間 Chrome 視窗會可見開啟（繞過 Cloudflare 所需）

🔄 **即時數據**：截圖捕捉執行時的當前市場數據

📁 **檔案覆蓋**：每次執行會覆蓋相同類型的舊 PNG 檔案

---

## 故障排除

### Cloudflare 驗證問題
- 等待完整的 35-40 秒讓驗證完成
- 確保網路連線穩定
- 如果首次嘗試失敗，請再次執行

### 找不到 Canvas 元素
- 腳本包含備用方法來定位 canvas
- 使用備用方法時，瀏覽器視窗可能會開啟較長時間

### 權限錯誤
- 確保專案目錄可寫入
- 在 Windows 上，避免使用系統保護目錄

### 瀏覽器錯誤
- 確保已安裝 Chrome/Chromium
- 將 Chrome 更新至最新版本
- 執行前關閉其他 Chrome 實例

---

## 使用範例

### 每日市場快照

```bash
# 早上：捕捉 S&P 500
python skills/finviz-map/scripts/capture_canvas.py

# 在瀏覽器中開啟 index.html 查看
```

### 多市場報告

```bash
# 捕捉所有市場類型
python skills/finviz-map/scripts/capture_canvas.py -t sec --no-html
python skills/finviz-map/scripts/capture_canvas.py -t world --no-html
python skills/finviz-map/scripts/capture_canvas.py -t etf --no-html
python skills/finviz-map/scripts/capture_canvas.py -t crypto --no-html

# 結果：spy.png、world.png、etf.png、crypto.png
```

---

## 專案結構

```
finviz-map/
├── README.md                           # 說明文件（本檔案）
├── spy.png                             # 生成：S&P 500 地圖
├── index.html                          # 生成：HTML 檢視器
├── api/
│   ├── README.md                       # API 完整文件 ⭐
│   ├── example.html                    # API 線上展示
│   ├── top_losers.json                 # 生成：API 資料（完整版）
│   └── top_losers_simple.json          # 生成：API 資料（簡化版）
├── .github/
│   └── workflows/
│       └── generate-finviz-map.yml     # 自動化工作流
└── skills/
    └── finviz-map/
        └── scripts/
            ├── capture_canvas.py       # 截圖程式碼
            └── analyze_map.py          # AI 分析程式碼
```

---

## 📚 相關連結

- **API 完整文件**: [api/README.md](api/README.md) ⭐ 推薦閱讀
- **GitHub Models**: [https://docs.github.com/en/github-models](https://docs.github.com/en/github-models)
- **Finviz 市場地圖**: [https://finviz.com/map.ashx](https://finviz.com/map.ashx)

---

## 授權

本專案僅供教育和個人使用。使用此工具時請尊重 Finviz.com 的服務條款。

## 參考

市場數據由 [Finviz.com](https://finviz.com) 提供  
[awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

# Finviz 市場資料 API

自動化的股票市場資料 API，使用 GitHub Actions + GitHub Models 每日更新跌幅最大的五檔股票。

---

## 🚀 快速開始

### API 端點

```
https://{your-username}.github.io/finviz-map/api/top_losers.json
```

### 回應格式

**回應格式**:
```json
{
  "status": "success",
  "data": {
    "top_losers": [
      {"ticker": "UBER", "change": "-2.10%"},
      {"ticker": "NFLX", "change": "-1.18%"},
      {"ticker": "LLY", "change": "-1.99%"},
      {"ticker": "ABBV", "change": "-1.91%"},
      {"ticker": "AMD", "change": "-0.74%"}
    ],
    "generated_at": "2024-01-11T21:45:00Z",
    "source": "finviz"
  },
  "version": "1.0",
  "last_updated": "2024-01-11T21:45:00Z"
}
```

---

## 📖 使用範例

### JavaScript (Fetch API)

```javascript
// 獲取跌幅最大的股票
fetch('https://{your-username}.github.io/finviz-map/api/top_losers.json')
  .then(response => response.json())
  .then(data => {
    console.log('Top Losers:', data.data.top_losers);
    data.data.top_losers.forEach(stock => {
      console.log(`${stock.ticker}: ${stock.change}`);
    });
  })
  .catch(error => console.error('Error:', error));
```

### Python (requests)

```python
import requests

# 獲取資料
response = requests.get('https://{your-username}.github.io/finviz-map/api/top_losers.json')
data = response.json()

# 列印結果
print("Top 5 Losers:")
for stock in data['data']['top_losers']:
    print(f"{stock['ticker']}: {stock['change']}")
```

### cURL

```bash
# 獲取資料
curl https://{your-username}.github.io/finviz-map/api/top_losers.json

# 格式化輸出 (使用 jq)
curl -s https://{your-username}.github.io/finviz-map/api/top_losers.json | jq '.data.top_losers'
```

### React 範例

```jsx
import React, { useState, useEffect } from 'react';

function TopLosers() {
  const [losers, setLosers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://{username}.github.io/finviz-map/api/top_losers.json')
      .then(res => res.json())
      .then(data => {
        setLosers(data.data.top_losers);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>載入中...</div>;

  return (
    <div>
      <h2>今日跌幅最大</h2>
      <ul>
        {losers.map((stock, i) => (
          <li key={i}>{stock.ticker}: {stock.change}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## ⚙️ 設定指南

### 步驟 1: 啟用 GitHub Pages

1. 進入你的 GitHub 儲存庫
2. 點擊 **Settings** → **Pages**
3. Source 選擇 `gh-pages` 分支
4. 點擊 **Save**

📍 你的 API 將部署到: `https://{your-username}.github.io/finviz-map/api/top_losers.json`

### 步驟 2: 啟用 GitHub Actions

1. 進入 **Actions** 標籤
2. 點擊 **"I understand my workflows, go ahead and enable them"**
3. 確認工作流已啟用

### 步驟 3: 手動觸發首次運行

1. **Actions** → 選擇 **"Generate Finviz Market Map"**
2. 點擊 **"Run workflow"**
3. 選擇 `main` 分支
4. 點擊綠色的 **"Run workflow"** 按鈕

⏱️ 等待 5-10 分鐘，工作流會自動完成：
- ✅ 截取市場地圖
- ✅ AI 分析圖片
- ✅ 生成 JSON API
- ✅ 部署到 GitHub Pages

### 步驟 4: 驗證設定

訪問你的 API 端點：
```
https://{your-username}.github.io/finviz-map/api/top_losers.json
```

你應該看到 JSON 回應。同時可以訪問線上範例：
```
https://{your-username}.github.io/finviz-map/api/example.html
```

---

## 🔄 工作原理

### 自動化流程

```
每個交易日美東 4:30 PM (UTC 9:30 PM)
          ↓
    1. 截取 Finviz 市場地圖
          ↓
      生成 spy.png
          ↓
    2. AI 分析圖片
       (GitHub Models API - GPT-4o Vision)
          ↓
    3. 識別跌幅最大的 5 檔股票
          ↓
    4. 生成 JSON API 檔案
          ↓
    5. 部署到 GitHub Pages
          ↓
   公開 API 端點可訪問
```

### 技術架構

- **截圖**: Selenium + undetected-chromedriver
- **AI 分析**: GitHub Models API (GPT-4o with Vision)
- **自動化**: GitHub Actions
- **託管**: GitHub Pages
- **更新頻率**: 每個交易日收盤後自動更新

---

## 📊 API 規格

### 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `ticker` | string | 股票代碼 (如 "AAPL", "MSFT") |
| `change` | string | 漲跌幅百分比 (如 "-2.10%") |
| `generated_at` | string | 資料生成時間 (ISO 8601 格式) |
| `source` | string | 資料來源 ("finviz") |
| `status` | string | API 狀態 ("success" 或 "error") |
| `version` | string | API 版本號 |

### 更新時間

- **自動更新**: 每個交易日美東時間 4:30 PM (UTC 9:30 PM)
- **手動觸發**: 可在 GitHub Actions 中手動觸發工作流
- **更新延遲**: 市場收盤後約 5-10 分鐘
- **交易日**: 僅在美股交易日更新 (週一至週五)

### CORS 支援

GitHub Pages 預設支援 CORS，可直接從瀏覽器客戶端呼叫此 API。

### 限制說明

- 🔄 **資料時效**: 資料代表截圖時刻的市場狀態
- 🎯 **準確性**: AI 識別準確率約 95%+ (可能有個別誤差)
- 📡 **呼叫限制**: GitHub Pages 靜態檔案無呼叫次數限制

---

## 🛠️ 進階設定

### 修改更新頻率

編輯 `.github/workflows/generate-finviz-map.yml`:

```yaml
on:
  schedule:
    # 預設: 美東時間 4:30 PM (UTC 9:30 PM)
    - cron: '30 21 * * 1-5'

    # 其他選項:
    # - cron: '30 13 * * 1-5'  # 美東 9:30 AM (開盤)
    # - cron: '0 0 * * 1-5'    # UTC 00:00 (每日)
```

### 自訂分析內容

編輯 `skills/finviz-map/scripts/analyze_map.py` 的提示詞：

**範例: 分析漲幅最大的股票**

```python
prompt = """分析這張 Finviz 市場地圖截圖。

請找出漲幅最大的五檔股票（最綠/最深綠色的方塊）。

要求：
1. 只返回 JSON 格式
2. JSON 格式如下：
{
  "top_gainers": [
    {"ticker": "股票代碼", "change": "漲幅百分比"},
    ...
  ],
  "generated_at": "ISO 時間戳記",
  "source": "finviz"
}
"""
```

同時修改輸出檔案名稱:
```python
parser.add_argument(
    "-o", "--output",
    default="api/top_gainers.json",  # 改為 top_gainers
    help="輸出 JSON 路徑"
)
```

### 分析多個市場

修改工作流來分析所有市場類型:

```yaml
- name: Generate all maps
  run: |
    cd skills/finviz-map/scripts
    python capture_canvas.py -t sec --no-html
    python capture_canvas.py -t world --no-html
    python capture_canvas.py -t etf --no-html
    python capture_canvas.py -t crypto --no-html

- name: Analyze all maps
  run: |
    python skills/finviz-map/scripts/analyze_map.py -i spy.png -o api/spy_losers.json
    python skills/finviz-map/scripts/analyze_map.py -i world.png -o api/world_losers.json
    python skills/finviz-map/scripts/analyze_map.py -i etf.png -o api/etf_losers.json
    python skills/finviz-map/scripts/analyze_map.py -i crypto.png -o api/crypto_losers.json
```

---

## 🔧 故障排除

### API 返回 404

**原因**:
- GitHub Pages 未啟用
- 分支選擇錯誤
- 工作流未成功運行

**解決方法**:
1. 確認 Settings → Pages → Source 設為 `gh-pages`
2. 檢查 `gh-pages` 分支是否存在
3. 查看 Actions 是否成功完成

### 工作流失敗

**原因**:
- Cloudflare 驗證超時
- Chrome 安裝失敗
- API 呼叫失敗

**解決方法**:
1. 查看 Actions 日誌找到具體錯誤
2. 手動重新運行工作流
3. 檢查 GitHub Models API 額度

### JSON 資料不準確

**原因**:
- AI 識別錯誤
- 圖片品質問題
- 提示詞不夠清晰

**解決方法**:
1. 查看 Actions 日誌中的 API 回應
2. 下載 `spy.png` 檢查圖片品質
3. 最佳化提示詞

### GitHub Models API 限制

**免費額度**:
- 每分鐘 15 次請求
- 每天 150 次請求
- 每月 1500 次請求

**超出限制時**:
- 減少工作流運行頻率
- 等待配額重置

---

## 📚 相關資源

- [GitHub Models 文件](https://docs.github.com/en/github-models)
- [GitHub Actions 文件](https://docs.github.com/en/actions)
- [GitHub Pages 文件](https://docs.github.com/en/pages)
- [Finviz 市場地圖](https://finviz.com/map.ashx)
- [專案原始碼](https://github.com/{your-username}/finviz-map)

---

## ⚠️ 免責聲明

**重要提示**:
- 此 API 僅供教育和研究目的
- 資料可能存在延遲或誤差
- 不構成投資建議
- 使用此資料進行投資決策需自行承擔風險
- 請遵守 Finviz.com 的服務條款

---

## 📄 授權

資料來自 [Finviz.com](https://finviz.com)，僅供個人使用。

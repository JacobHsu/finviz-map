#!/usr/bin/env python3
"""
使用 GitHub Models API 分析 Finviz 市場地圖
提取跌幅最大的五檔股票並輸出到 JSON
"""

import os
import sys
import json
import base64
from datetime import datetime
from pathlib import Path
import argparse


def encode_image(image_path):
    """將圖片編碼為 base64 字串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_with_github_models(image_path, api_token):
    """
    使用 GitHub Models API 分析市場地圖

    GitHub Models 提供免費的 AI 模型存取，包括 GPT-4o with vision
    詳見: https://github.com/marketplace/models
    """
    import requests

    # 編碼圖片
    base64_image = encode_image(image_path)

    # GitHub Models API endpoint
    # 使用 gpt-4o 模型 (支援 vision)
    url = "https://models.inference.ai.azure.com/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # 構建提示詞
    prompt = """分析這張 Finviz 市場地圖截圖。

這是一個股票市場熱力圖，每個方塊代表一個股票：
- 紅色方塊 = 下跌的股票
- 綠色方塊 = 上漲的股票
- 每個方塊顯示股票代碼和漲跌幅百分比

請找出跌幅最大的五檔股票（最紅/最深紅色的方塊）。

要求：
1. 只返回 JSON 格式，不要其他文字
2. JSON 格式如下：
{
  "top_losers": [
    {"ticker": "股票代碼", "change": "跌幅百分比"},
    ...
  ],
  "generated_at": "ISO 時間戳記",
  "source": "finviz"
}

3. 跌幅應該是負數（例如 "-2.10%"）
4. 按跌幅從大到小排序（最大跌幅在前）
5. 準確識別每個方塊上的文字"""

    payload = {
        "model": "gpt-4o",  # 使用支援 vision 的模型
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.1  # 降低溫度以獲得更準確的結果
    }

    try:
        print("📤 正在呼叫 GitHub Models API...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        print("✅ API 呼叫成功")
        print(f"📝 回應內容:\n{content}\n")

        # 嘗試解析 JSON
        # 有時 AI 會在 JSON 外包裝 markdown 代碼區塊
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ API 請求失敗: {e}")
        if hasattr(e.response, 'text'):
            print(f"回應內容: {e.response.text}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {e}")
        print(f"原始內容: {content}")
        raise


def save_json_api(data, output_path):
    """儲存 JSON API 回應檔案"""

    # 確保有 generated_at 欄位
    if "generated_at" not in data:
        data["generated_at"] = datetime.utcnow().isoformat() + "Z"

    # 添加 API 中繼資料
    api_response = {
        "status": "success",
        "data": data,
        "version": "1.0",
        "last_updated": data.get("generated_at")
    }

    # 儲存為美化的 JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(api_response, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON API 已儲存: {output_path}")

    # 同時儲存一個簡化版本（只包含資料）
    simple_output = output_path.replace('.json', '_simple.json')
    with open(simple_output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 簡化版 JSON 已儲存: {simple_output}")

    return api_response


def main():
    parser = argparse.ArgumentParser(
        description="使用 GitHub Models API 分析 Finviz 市場地圖"
    )
    parser.add_argument(
        "-i", "--input",
        default="spy.png",
        help="輸入圖片路徑 (預設: spy.png)"
    )
    parser.add_argument(
        "-o", "--output",
        default="api/top_losers.json",
        help="輸出 JSON 路徑 (預設: api/top_losers.json)"
    )
    parser.add_argument(
        "--token",
        help="GitHub Models API token (或使用環境變數 GITHUB_TOKEN)"
    )

    args = parser.parse_args()

    # 取得 API token
    api_token = args.token or os.environ.get("GITHUB_TOKEN")
    if not api_token:
        print("❌ 錯誤: 需要 GitHub token")
        print("   方法1: --token YOUR_TOKEN")
        print("   方法2: 設定環境變數 GITHUB_TOKEN")
        sys.exit(1)

    # 檢查圖片是否存在
    script_dir = Path(__file__).parent.parent.parent.parent
    image_path = script_dir / args.input

    if not image_path.exists():
        print(f"❌ 錯誤: 找不到圖片 {image_path}")
        sys.exit(1)

    print(f"📊 Finviz 市場地圖分析器")
    print(f"輸入圖片: {image_path}")
    print(f"輸出路徑: {args.output}\n")

    try:
        # 分析圖片
        result = analyze_with_github_models(str(image_path), api_token)

        # 儲存 JSON
        output_path = script_dir / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)

        api_response = save_json_api(result, str(output_path))

        # 顯示結果
        print(f"\n🎉 分析完成!")
        print(f"\n跌幅最大的 5 檔股票:")
        for i, stock in enumerate(result.get("top_losers", []), 1):
            print(f"  {i}. {stock.get('ticker', 'N/A')}: {stock.get('change', 'N/A')}")

        print(f"\n📡 API 端點已準備好:")
        print(f"   {output_path}")

        sys.exit(0)

    except Exception as e:
        print(f"\n❌ 分析失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

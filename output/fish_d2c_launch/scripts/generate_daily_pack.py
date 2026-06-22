#!/usr/bin/env python3
import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "automation_config.json"
RUNS_DIR = ROOT / "daily_runs"


CONTENT_ROTATION = [
    {
        "theme": "乾煎魚",
        "asset": "social_images/fried-fish-square-1080.jpg",
        "hook": "今晚就煎一盤魚",
        "post": "魚擦乾、鍋燒熱、兩面煎到金黃。每尾約 300g，小家庭一餐一尾剛剛好。",
        "line": "今天主題是乾煎魚。想看第一波預購規格，回覆「預購」。",
        "cta": "私訊「家庭包」看本週規格"
    },
    {
        "theme": "鮮魚豆腐湯",
        "asset": "social_images/fish-soup-square-1080.jpg",
        "hook": "一尾魚，一碗家常熱湯",
        "post": "一尾魚、一盒豆腐、幾片薑，煮成一碗很台灣的家常味。",
        "line": "今天主題是鮮魚豆腐湯。想領料理小卡，回覆「魚湯」。",
        "cta": "留言「魚湯」領料理小卡"
    },
    {
        "theme": "保存與退冰",
        "asset": "social_images/fried-fish-fit-square-1080.jpg",
        "hook": "魚好吃，退冰先做對",
        "post": "收到後請依包裝標示低溫保存。退冰後不建議再次冷凍，料理前擦乾更好煎。",
        "line": "今天整理退冰與保存 FAQ。遇到破包、失溫請先拍照保留包裝。",
        "cta": "回覆「保存」看 FAQ"
    },
    {
        "theme": "團購招募",
        "asset": "social_images/fish-soup-fit-square-1080.jpg",
        "hook": "社區、公司、親友可以一起開團",
        "post": "每尾約 300g，好分配、好料理。20 尾團購箱適合社區、公司、親友團。",
        "line": "想開團請回覆「團購」，客服會確認規格、價格、配送與出貨日。",
        "cta": "私訊「開團」索取圖文包"
    }
]


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def missing_required(config):
    product = config["product"]
    missing = []
    if product["species"].startswith("待確認"):
        missing.append("魚種")
    if product["origin"].startswith("待確認"):
        missing.append("產地")
    if product["storage_type"].startswith("待確認"):
        missing.append("保存型態")
    for sku in config["skus"]:
        if sku["price"] is None:
            missing.append(f"{sku['name']}售價")
    return missing


def render_markdown(config, date_str, item, missing):
    units_estimate = int(config["product"]["total_inventory_kg"] * 1000 / config["product"]["unit_weight_g"])
    missing_text = "\n".join(f"- [ ] {x}" for x in missing) if missing else "- [x] 基礎上架資料已填齊"
    sku_lines = "\n".join(
        f"| {sku['name']} | {sku['units']} 尾 | 約 {sku['weight_kg']}kg | {sku['role']} | {'待確認' if sku['price'] is None else 'NT$' + str(sku['price'])} |"
        for sku in config["skus"]
    )
    return f"""# 每日自動行銷作戰包：{date_str}

品牌：{config['brand_name']}  
今日主題：{item['theme']}  
今日素材：`{item['asset']}`  
庫存假設：約 {config['product']['total_inventory_kg']}kg，約 {units_estimate} 尾。

## 今日紅線檢查

以下資料未補齊前，不可正式對外發布、群發、收款或承諾出貨：

{missing_text}

## 今日社群貼文草稿

{item['hook']}

{item['post']}

{item['cta']}

需人工確認：魚種、產地、售價、出貨日、LINE/下單連結。

## 今日 LINE 草稿

{item['line']}

提醒：低溫商品請確認可收貨時間；正式價格與出貨日由客服確認後成立。

## 今日短影音腳本

- 0-3 秒：料理成品或商品近拍。字幕：{item['hook']}
- 4-8 秒：筷子夾魚/熱湯/餐桌畫面。字幕：每尾約 300g，一餐剛剛好
- 9-15 秒：包裝或家庭餐桌。字幕：乾煎、清蒸、煮湯都方便
- 結尾：{item['cta']}

## 今日 SKU 狀態

| SKU | 內容 | 重量 | 用途 | 售價 |
|---|---:|---:|---|---:|
{sku_lines}

## 今日 AI Agent 任務

| Agent | 任務 | 輸出 |
|---|---|---|
| 資料整理 | 更新庫存、售價、出貨日、缺漏欄位 | 商品資料包 |
| 市場洞察 | 整理昨日留言/私訊問題 | 今日內容角度 |
| 商品企劃 | 推薦主推 SKU | 組合與免運建議 |
| 內容企劃 | 產出社群/LINE/短影音草稿 | 待審文案 |
| 素材產製 | 指定素材與版型 | 設計 brief |
| 合規審核 | 掃描高風險宣稱 | 審核報告 |
| 排程成效 | 產出待發布清單 | 人工發布 checklist |

## 人工待辦

- [ ] 補齊今日紅線檢查項目。
- [ ] 決定今日是否發布社群貼文。
- [ ] 決定是否 LINE 群發，並確認收件分眾。
- [ ] 確認是否開放預購與可售數量。
- [ ] 收集今日詢問、成交、客訴，明日回填。
"""


def write_csv_summary(config, date_str, item, missing, run_dir):
    path = run_dir / "today_tasks.csv"
    rows = [
        ["priority", "owner", "task", "approval_required"],
        ["P0", "營運", "補齊魚種、產地、保存型態、售價、出貨日", "是"],
        ["P1", "小編", f"使用素材 {item['asset']} 製作今日 {item['theme']} 貼文", "是"],
        ["P1", "LINE 客服", "把 LINE 草稿放入後台草稿區", "是"],
        ["P1", "團購窗口", "接觸 5 位團購主，僅提供資料包不承諾價格", "是"],
        ["P2", "成效 Agent", "記錄詢問數、LINE 新好友、成交數、客訴原因", "否"]
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)


def main():
    config = load_config()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    day_index = int(now.strftime("%j")) % len(CONTENT_ROTATION)
    item = CONTENT_ROTATION[day_index]
    missing = missing_required(config)
    run_dir = RUNS_DIR / date_str
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "daily_pack.md").write_text(render_markdown(config, date_str, item, missing), encoding="utf-8")
    write_csv_summary(config, date_str, item, missing, run_dir)
    latest = ROOT / "latest_daily_pack.md"
    latest.write_text((run_dir / "daily_pack.md").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Generated {run_dir / 'daily_pack.md'}")
    print(f"Generated {run_dir / 'today_tasks.csv'}")
    print(f"Updated {latest}")


if __name__ == "__main__":
    main()


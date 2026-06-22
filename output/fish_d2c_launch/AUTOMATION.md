# 全程自動化操作說明

這套自動化採「自動產出、人工發布」模式。  
目的：每天自動產出可執行的行銷作戰包，同時避免食品標示、價格、出貨與廣告投放的風險。

## 自動化會做

- 產出每日社群貼文草稿。
- 產出每日 LINE 草稿。
- 產出短影音腳本。
- 產出 SKU 與庫存提醒。
- 產出 7 組 AI agent 任務表。
- 產出人工待辦清單。

## 自動化不會做

- 自動發 FB/IG/TikTok。
- 自動 LINE 群發。
- 自動私訊客戶。
- 自動投放廣告或調整預算。
- 自動改價或承諾庫存。
- 自動宣稱魚種、產地、檢驗、食品安全。

## 本機產出指令

```bash
python3 output/fish_d2c_launch/scripts/generate_daily_pack.py
```

產出位置：

- `output/fish_d2c_launch/latest_daily_pack.md`
- `output/fish_d2c_launch/daily_runs/YYYY-MM-DD/daily_pack.md`
- `output/fish_d2c_launch/daily_runs/YYYY-MM-DD/today_tasks.csv`

## 每天人工只要看三件事

1. `latest_daily_pack.md`：今天要發什麼、要推哪個主題。
2. `approval_checklist.md`：是否可以對外發布。
3. `today_tasks.csv`：小編、客服、團購、營運今天做什麼。


# 自動化控制中心

狀態：已啟動  
建立日期：2026-06-23  
Codex automation id：`d2c`  
名稱：台灣魚貨D2C每日自動行銷作戰包  
頻率：每日早上自動執行  

## GitHub / Render 部署紀錄

- GitHub repo：https://github.com/809540023-lgtm/taiwan-fish-d2c-launch-record
- Render service：https://dashboard.render.com/static/srv-d8so5b3sq97s73e2s5qg
- Render public URL：https://taiwan-fish-d2c-launch-record.onrender.com
- Render deploy：https://dashboard.render.com/static/srv-d8so5b3sq97s73e2s5qg/deploys/dep-d8so5bbsq97s73e2s620
- 初次部署 commit：`5a1cbb770ee5c415c7e82b65fd8cf4b7a05657ad`

## 每日自動執行內容

Codex 每天會在 workspace：

`/Users/linemily/Documents/STARBIT`

執行：

```bash
python3 output/fish_d2c_launch/scripts/generate_daily_pack.py
```

並更新：

- `output/fish_d2c_launch/latest_daily_pack.md`
- `output/fish_d2c_launch/daily_runs/YYYY-MM-DD/daily_pack.md`
- `output/fish_d2c_launch/daily_runs/YYYY-MM-DD/today_tasks.csv`

## 已自動化

- 每日社群貼文草稿。
- 每日 LINE 草稿。
- 每日短影音腳本。
- 每日素材選用。
- 每日 7 組 AI agent 任務。
- 每日人工待辦。
- 紅線資料缺漏檢查。

## 暫不自動化，需人工確認

- 發布 FB/IG/TikTok/Reels。
- LINE 群發。
- 私訊客戶。
- 投放廣告或調整預算。
- 修改售價。
- 承諾庫存或出貨日。
- 宣稱魚種、產地、檢驗、食品安全。

## 進入全自動發布前必備資料

以下資料補齊後，才適合進一步串接 Meta、LINE OA、蝦皮/官網、Google Sheets 或 n8n/Make：

- 魚種。
- 產地。
- 保存型態。
- 有效日期。
- 食品業者登錄與加工/分裝資訊。
- 各 SKU 售價。
- 運費與免運門檻。
- 固定出貨日。
- 可售庫存與安全庫存。
- 客服退換貨政策。
- LINE OA、Meta Business、電商平台權限。

## 下一階段可串接

1. Google Sheets：自動讀取庫存、訂單、售價。
2. LINE OA：自動產生草稿與標籤分類，送出前人工確認。
3. Meta Business Suite：自動建立草稿貼文，發布前人工確認。
4. n8n/Make：串接每日資料流與通知。
5. 電商平台：自動比對庫存與訂單，但改價和上架仍需人工審批。

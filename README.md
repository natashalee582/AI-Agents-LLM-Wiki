# AI Agents LLM Wiki｜HTML 教學簡報

本作業包含：5 份經來源核對的官方文件筆記、9 個可搜尋 Wiki 知識節點、12 張具有來源追溯的 HTML 教學投影片、流程設計與測試／反思紀錄。

## 直接瀏覽（無需安裝）

1. 解壓縮整個資料夾，保持檔案相對位置。
2. 雙擊 `index.html` 作為入口。
3. 點「開啟 LLM Wiki」或「開始學習 12 頁簡報」。
4. 簡報可以按左右箭頭、按鈕、End/Home；手機可左右滑動。

> 建議用 Chrome / Safari 開啟。首頁、Wiki、簡報都不依賴 CDN 或外部 JS。只有官方來源 URL 在點擊後需要網路。

## 檔案用途

- `index.html`：專案首頁。
- `wiki.html`：含搜尋及來源對照的 Wiki 成果。
- `slides.html`：12 頁 HTML 簡報。
- `report.html`：可直接看的作業報告，涵蓋老師要求的六項繳交內容。
- `繳交內容.txt`：可貼入學校繳交系統的文字說明。
- `sources/S01.md` ～ `S05.md`：五份原創來源摘要筆記。
- `data/source_manifest.json`：可驗證的 ingest 記錄、來源 URL、SHA-256。
- `data/knowledge_base.json`：已結構化的 Wiki 知識庫。
- `workflow.md`：Graph / Loop 設計、實作過程與反思。
- `scripts/build.py`：產生 Wiki、簡報、資料庫與首頁。
- `scripts/validate.py`：驗證來源引用、數量與 HTML 結構。
- `tests/`：實際執行與瀏覽器操作檢查紀錄及截圖。

## 重跑（選用，需要 Python 3）

```bash
python scripts/build.py
python scripts/validate.py
```

`validate.py` 需要 `beautifulsoup4`：`python -m pip install beautifulsoup4`。

## 作業繳交

本作業可以用課程平台的「檔案上傳」繳交完整 ZIP；ZIP 裡的 `index.html` 是主入口。若老師要求**公開網址**，請把整個資料夾內容上傳 GitHub repository 的根目錄，並啟用 GitHub Pages（Settings → Pages → Deploy from a branch → main / root）。設定完成後，把 `https://<使用者>.github.io/<repo>/wiki.html` 和 `/slides.html` 寫入繳交欄位。這份離線檔案本身沒有自動產生公開部署網址。

**學校／學號／系級／姓名需自行填入**；本專案不會擅自使用個人資料。

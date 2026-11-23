#!/usr/bin/env python3
"""Browser interaction checks using locally installed Chromium and HTML document contents.
This test uses page.set_content because the sandbox's Chromium blocks file:// navigation.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
results=[]
def ck(name,cond):
    results.append((name,bool(cond)))
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':900})
    page.set_content((R/'slides.html').read_text(encoding='utf8'))
    ck('簡報初始頁載入',page.locator('#page').inner_text()=='1 / 12' and page.locator('.slide.active').count()==1)
    page.locator('#next').click();ck('下一頁按鈕',page.locator('#page').inner_text()=='2 / 12')
    page.keyboard.press('End');ck('鍵盤 End 前往最後一頁',page.locator('#page').inner_text()=='12 / 12')
    page.keyboard.press('ArrowLeft');ck('鍵盤箭頭回上一頁',page.locator('#page').inner_text()=='11 / 12')
    page.keyboard.press('Home');
    for _ in range(10): page.locator('#next').click()
    page.locator('[data-reveal]').click();ck('測驗答案顯示',page.locator('.answer.visible').count()==1)
    page.set_content((R/'wiki.html').read_text(encoding='utf8'))
    page.locator('#search').fill('Graph');ck('Wiki 搜尋篩選',page.locator('.concept:visible').count()==1)
    page.locator('#search').fill('no_search_results_000');ck('Wiki 無結果提示',page.locator('#no-results').is_visible() and page.locator('.concept:visible').count()==0)
    page.locator('#search').fill('');page.screenshot(path=str(R/'tests/wiki_screenshot.png'),full_page=True)
    page.set_content((R/'slides.html').read_text(encoding='utf8'));page.wait_for_timeout(450)
    page.screenshot(path=str(R/'tests/slides_screenshot.png'))
    browser.close()
log='\n'.join(('[PASS]' if ok else '[FAIL]')+' '+name for name,ok in results)+f'\nBROWSER_RESULT {sum(ok for _,ok in results)}/{len(results)}\n'
(R/'tests/04_browser_validation.txt').write_text(log,encoding='utf8')
print(log)
assert all(ok for _,ok in results)

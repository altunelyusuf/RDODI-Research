import json, os
from playwright.sync_api import sync_playwright

with open("widget_records.json") as f:
    widgets = json.load(f)
page_path = "file://" + os.path.abspath("code_abundance_page_v1_0_0.html")
console_errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: console_errors.append(str(exc)))
    page.goto(page_path)
    print(f"Stage4.C: console errors = {len(console_errors)}")
    dialog_selector = "[role='dialog']"
    dialogs = page.eval_on_selector_all(dialog_selector, "els => els.length")
    print(f"Stage4.D-structural: dialogs = {dialogs}")
    nav = page.eval_on_selector_all("nav.pillbar a.pill", "els => els.length")
    print(f"Stage4.E/F: nav pills = {nav} (need 21)")
    passed, failed = 0, 0
    for w in widgets:
        hb = page.eval_on_selector(f"#{w['detail_id']}", "el => el.hasAttribute('hidden')")
        page.click(f"#{w['btn_id']}")
        ha = page.eval_on_selector(f"#{w['detail_id']}", "el => el.hasAttribute('hidden')")
        if hb and not ha:
            passed += 1
        else:
            failed += 1
    print(f"Widget interaction test: {passed}/{len(widgets)} passed")
    browser.close()

from playwright.sync_api import sync_playwright
import time
import requests
from bs4 import BeautifulSoup


# main処理
def run(playwright, year):
    # ブラウザ設定
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # 新しいページを開く
    page = context.new_page()

    # URL「https://db.netkeiba.com/?pid=race_search_detail」にアクセス
    page.goto("https://db.netkeiba.com/?pid=race_search_detail")
    time.sleep(1)

    # 検索条件を設定
    # 期間
    # 開始年(start_year) = year
    page.select_option(
        "#db_search_detail_form > form > table > tbody > tr:nth-child(3) > td > select:nth-child(1)", year)
    # 終了年(end_year) = year
    page.select_option(
        "#db_search_detail_form > form > table > tbody > tr:nth-child(3) > td > select:nth-child(3)", year)

    # 競馬場
    # Click text="札幌"
    page.click("text=\"札幌\"")
    # Click text="函館"
    page.click("text=\"函館\"")
    # Click text="福島"
    page.click("text=\"福島\"")
    # Click text="新潟"
    page.click("text=\"新潟\"")
    # Click text="東京"
    page.click("text=\"東京\"")
    # Click text="中山"
    page.click("text=\"中山\"")
    # Click text="中京"
    page.click("text=\"中京\"")
    # Click text="京都"
    page.click("text=\"京都\"")
    # Click text="阪神"
    page.click("text=\"阪神\"")
    # Click text="小倉"
    page.click("text=\"小倉\"")

    # 表示件数
    page.select_option(
        "#db_search_detail_form > form > table > tbody > tr:nth-child(11) > td > select", "100")
    time.sleep(2)

    # 検索ボタンを選択
    page.click("div[id=\"db_search_detail_form\"] input[type=\"submit\"]")
    # assert page.url == "https://db.netkeiba.com/"
    time.sleep(1)

    # レースIDを取得
    # ページング件数を取得
    result_count_str = page.inner_text(
        "#contents_liquid > div.search_result_box > div.pager").split("件中")
    count_str = result_count_str[0].replace(",", "")
    count = int(count_str)
    race_id_args = []

    # ページング件数分、処理を繰り返してレースIDを取得
    while_num = count
    while 0 < while_num:
        print(page.inner_text(
            "#contents_liquid > div.search_result_box > div.pager"))
        # レースIDを取得
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        a_link = soup.select(
            "#contents_liquid > table > tbody > tr > td:nth-child(5) > a")
        for a in a_link:
            race_id_args.append(a.get('href').replace(
                "/race/", "").replace("/", ""))
        time.sleep(3)
        while_num = while_num - 100
        if while_num > 0:
            page.click("text=\"次\"")

    # 開いたページを閉じる
    page.close()

    # ---------------------
    # クローズ処理
    context.close()
    browser.close()

    # テキスト出力
    d = "\n".join(race_id_args)
    with open('data/' + year + '_race_id.txt', 'w') as f:
        f.write(d)


# main処理を実行
with sync_playwright() as playwright:
    run(playwright, "2020")
    run(playwright, "2019")
    run(playwright, "2018")
    run(playwright, "2017")
    run(playwright, "2016")
    run(playwright, "2015")
    run(playwright, "2014")
    run(playwright, "2013")
    run(playwright, "2012")
    run(playwright, "2011")
    run(playwright, "2010")

from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import csv
import math
import numpy as np
import difflib
import string
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
driver = webdriver.Chrome(options=options)

data_array = []
CsvReadData = []
with open("他媒体求人マッチング用.csv", encoding="SHIFT-JIS") as csvfile:
    # change contents to floats
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:  # each row is a list

        CsvReadData.append(row)
arr = np.array(CsvReadData)
tempArray = np.array(CsvReadData)
csvArray = tempArray[:, 1]

csvArray = np.unique(csvArray)


def getInformationFromAruNavi(baseUrl, bookmarkedUrl, fileName):

    print("Start get Information From AruNavi")
    driver.get(baseUrl)
    dataUrl = driver.find_elements_by_css_selector('[alt="求人詳細を見る"]')
    url_per_page = len(dataUrl)
    page1 = requests.get(baseUrl)
    soup1 = BeautifulSoup(page1.content, "html.parser")
    data_count = soup1.find_all("div", class_="result-count")
    for d in range(0, len(data_count)):
        total_data = str(data_count[d].find("p").text).split("該当する求人数")[1].split("件")[0]
    loopcount = math.ceil(int(total_data) / url_per_page)
    print("Total Data: " + total_data)
    print("Total pagination for main page: " + str(loopcount))
    temp = baseUrl
    for a in range(0, 1):
        counter = 0
        driver.get(temp)
        if loopcount > 1 and a > 0:
            nextButton = driver.find_elements_by_class_name("utility-module-paginate")

            nextButtonClick = (
                nextButton[1]
                .find_element_by_css_selector("ul")
                .find_elements_by_css_selector("li a")
            )
            temp = baseUrl
            nextButton = driver.find_elements_by_class_name("utility-module-paginate")
            nextButtonClick = (
                nextButton[1]
                .find_element_by_css_selector("ul")
                .find_elements_by_css_selector("li a")
            )
            for click in range(0, len(nextButtonClick)):
                if nextButtonClick[click].text == "次へ »":
                    nextButtonClick[click].get_attribute("href")
                    time.sleep(2)
                    temp = nextButtonClick[click].get_attribute("href")
                    driver.get(temp)

        print("Pagination starting: " + str(a + 1))
        like = driver.find_elements_by_class_name("bookmark-action")
        for x in range(0, len(like)):
            if like[x].is_displayed():
                like[x].click()
                counter += 1
                time.sleep(1)
        time.sleep(5)
        print("Bookmarked completed " + str(counter))
        data1 = ""
        data2 = ""
        data3 = ""
        data4 = ""
        data5 = ""
        data6 = ""
        data7 = ""
        data8 = ""
        name = []
        driver.get(bookmarkedUrl)
        bookAll = driver.find_elements_by_css_selector('[alt="求人詳細を見る"]')
        loopCount2 = math.ceil(counter / len(bookAll))
        print("loop count for bookmark pagination: " + str(loopCount2))
        name = []
        for c in range(0, loopCount2):
            print("bookmarked pagination no:" + str(c + 1))
            driver.get(bookmarkedUrl)
            time.sleep(3)
            nameAll = driver.find_elements_by_class_name("clinic")
            for y in range(0, len(nameAll)):
                name.append(nameAll[y].text)
            print("name count: " + str(len(nameAll)))
            jobAll = driver.find_elements_by_css_selector('[alt="求人詳細を見る"]')
            matching = 0
            for info in range(0, len(jobAll)):

                data1 = name[info]
                data_url = (
                    jobAll[info].find_element_by_xpath("..").get_attribute("href")
                )
                page = requests.get(data_url)
                soup = BeautifulSoup(page.content, "html.parser")
                tb = soup.find_all("table", class_="detail-entry-info")
                for single_table in tb:
                    tb_head = single_table.find("td", class_="title").find(
                        "span", class_="left"
                    )
                    if tb_head.text == "勤務日時":
                        trs = single_table.find_all("tr")
                        for single_tr in trs:
                            if "勤務日時" not in single_tr.text:
                                single_tr_th = single_tr.find("th")
                                if single_tr_th is not None:
                                    if "勤務日" in single_tr_th.text:
                                        # print(single_tr.text)
                                        temp1 = str(single_tr.text).split(")")[0] + ")"
                                        data2 = temp1.split("勤務日")[1]
                                    elif "勤務時間" in single_tr.text:
                                        part = single_tr.find_all("div")
                                        for i in range(0, len(part)):
                                            if i == 0:
                                                data3 = part[i].text
                                            elif i == 1:
                                                data4 = part[i].text
                    elif tb_head.text == "勤務内容":
                        trs = single_table.find_all("tr")
                        for single_tr in trs:
                            if "勤務内容" not in single_tr.text:
                                single_tr_th = single_tr.find("th")
                                if single_tr_th is not None:
                                    if "募集科目" in single_tr.text:
                                        temp2 = str(single_tr.text).split("募集科目")
                                        data5 = temp2[1]
                    elif tb_head.text == "勤務条件":
                        trs = single_table.find_all("tr")
                        for single_tr in trs:
                            if "勤務条件" not in single_tr.text:
                                single_tr_th = single_tr.find("th")
                                if single_tr_th is not None:
                                    if "給与" in single_tr_th.text:
                                        temp3 = str(single_tr.text).split("円")[0] + "円"
                                        data6 = temp3.split("与")[1]
                    elif tb_head.text == "勤務場所":
                        trs = single_table.find_all("tr")
                        for single_tr in trs:
                            if "勤務場所" not in single_tr.text:
                                single_tr_th = single_tr.find("th")
                                if single_tr_th is not None:
                                    if "所在" in single_tr_th.text:
                                        data7 = str(single_tr.text).split("在")[1]
                                    elif "施設" in single_tr_th.text:
                                        data8 = str(single_tr.text).split("設")[1]

                data_array.append(
                    [data1, data2, data3, data4, data5, data6, data7, data8, data_url]
                )
            print("get Data web page: " + str(len(jobAll)))
            deleteAll = driver.find_elements_by_class_name("bookmark-action")
            print("deleted bookmarked: " + str(len(deleteAll)))
            for delInfo in range(0, len(deleteAll)):

                if deleteAll[0].is_displayed():
                    deleteAll[0].click()
                    alert = driver.switch_to.alert
                    time.sleep(3)
                    alert.accept()
                time.sleep(3)
                deleteAll = driver.find_elements_by_class_name("bookmark-action")

        print("Pagination completed: " + str(a + 1))
    driver.close()
    csvCreateFunction(data_array, fileName)


matchedData = []


def csvCreateFunction(data_array1, fileName):
    data_array = [
        [
            "医療法人社団 貞栄会 三田在宅診療クリニック東京都 港区（最寄：大江戸線 「赤羽橋駅」ほか）",
            "2021.02.05 (金)",
            "勤務区分：日勤(終日)",
            "08:45～17:45（休憩60分",
            "一般内科",
            "1回 80,000円",
            "東京都",
            "無床クリニック",
            "https://arbeit.doctor-navi.jp/sh/jobs/1273433",
        ],
        [
            "医療法人社団新穂会 町屋皮フ科クリニック東京都 荒川区（最寄：東京メトロ千代田線・京成線 「町屋駅」）",
            "2021.02.05 (金)",
            "勤務区分：日勤(午後のみ)",
            "15:00～18:30（休憩なし）",
            "皮膚科",
            "1回 50,000円",
            "東京都",
            "無床クリニック",
            "https://arbeit.doctor-navi.jp/sh/jobs/1274457",
        ],
        [
            "医療法人社団福寿会 赤羽岩渕病院東京都 北区（最寄：JR湘南新宿ライン、京浜東北線、埼京線、宇都宮線、高崎...",
            "2021.02.05 (金)",
            "勤務区分：当直",
            "19:00～2021.02.06 (土) 09:00",
            "科目不問、内科",
            "1回 40,000円",
            "東京都",
            "病院 総病床数：100床未満",
            "https://arbeit.doctor-navi.jp/sh/jobs/1273065",
        ],
        [
            "公益財団法人 パブリックヘルスリサーチセンター附属健康増進センター　西日本健診グループ福岡県 福岡市（最寄：福岡市営地下鉄七隈線 「福大前駅」）",
            "2021.02.04 (木)",
            "勤務区分：日勤(午前のみ)",
            "07:30～13:00",
            "健診・ドック",
            "1回 55,000円",
            "福岡県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1267429",
        ],
        [
            "医療法人 横尾病院長崎県 諫早市",
            "2021.02.01 (月)",
            "勤務区分：当直",
            "18:00～2021.02.02 (火) 08:00",
            "科目不問、内科、精神科",
            "1回 50,000円",
            "長崎県",
            "病院 総病床数：200床以上",
            "https://arbeit.doctor-navi.jp/sh/jobs/1274644",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 浦添市",
            "2021.02.19 (金)",
            "勤務区分：日勤(午前のみ)",
            "08:30～11:00",
            "健診・ドック",
            "1回 35,000円",
            "沖縄県",
            "病院 総病床数：200床以上",
            "https://arbeit.doctor-navi.jp/sh/jobs/1266672",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 沖縄市",
            "2021.02.19 (金)",
            "勤務区分：日勤(午前のみ)",
            "08:30～11:30",
            "健診・ドック",
            "1回 35,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1269301",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県",
            "2021.02.19 (金)",
            "勤務区分：日勤(午後のみ)",
            "13:15～15:00",
            "健診・ドック",
            "1回 35,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1271572",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 読谷村",
            "2021.02.18 (木)",
            "勤務区分：日勤(午前のみ)",
            "08:30～12:00",
            "健診・ドック",
            "1回 35,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1271571",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 読谷村",
            "2021.02.17 (水)",
            "勤務区分：日勤(午前のみ)",
            "08:30～12:00",
            "健診・ドック",
            "1回 35,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1269300",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 那覇市",
            "2021.02.12 (金)",
            "勤務区分：日勤(午前のみ)",
            "09:30～11:30",
            "健診・ドック",
            "1回 45,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1271569",
        ],
        [
            "一般社団法人 日本健康倶楽部　沖縄支部沖縄県 那覇市",
            "2021.02.10 (水)",
            "勤務区分：日勤(午前のみ)",
            "09:00～12:00",
            "健診・ドック",
            "1回 45,000円",
            "沖縄県",
            "その他",
            "https://arbeit.doctor-navi.jp/sh/jobs/1266623",
        ],
        [
            "医療法人社団幸訪会 高田馬場クリニック皮膚科東京都 新宿区",
            "2021.02.07 (日)",
            "勤務区分：日勤(午前のみ)",
            "10:00～15:00（休憩なし）",
            "皮膚科、美容皮膚科",
            "1回 60,000円",
            "東京都",
            "無床クリニック",
            "https://arbeit.doctor-navi.jp/sh/jobs/1274131",
        ],
        [
            "医療法人社団苑田会 花はたリハビリテーション病院東京都 足立区（最寄：東武スカイツリーライン 「竹ノ塚」駅東口ほか）",
            "2021.02.04 (木)",
            "勤務区分：日勤(午前のみ)",
            "09:00～13:00",
            "皮膚科",
            "1回 40,000円",
            "東京都",
            "足立区 花畑5-12-29",
            "病院（救急指定なし） 総病床数：168床",
            "https://arbeit.doctor-navi.jp/sh/jobs/1273936",
        ],
        [
            "医療法人社団苑田会 花はたリハビリテーション病院東京都 足立区（最寄：東武スカイツリーライン 「竹ノ塚」駅東口ほか）",
            "2021.02.04 (木)",
            "勤務区分：日勤(終日)",
            "09:00～17:00（休憩45分",
            "整形外科",
            "1回 95,000円",
            "東京都 足立区 花畑5-12-29",
            "病院（救急指定なし） 総病床数：168床",
            "https://arbeit.doctor-navi.jp/sh/jobs/1273930",
        ],
    ]

    for singleRow in data_array:
        print(len(singleRow))
        flag = 0
        for singleValue in csvArray:
            if fuzz.token_set_ratio(singleValue, singleRow[0]) > 95:
                print(
                    fuzz.token_set_ratio(singleValue, singleRow[0]),
                    "  ",
                    singleRow[0],
                    "   ",
                    singleValue,
                )
                flag = 1
                break
        if flag == 0:
            matchedData.append(singleRow[0])
    print(len(matchedData))
    # if data1 not in compareArray:
    filename = "final_data.csv"
    columnName = ["病院名", "勤務日", "勤務時間1", "勤務時間2", "募集科目", "給与", "所在", "施設", "URL"]
    with open(filename, mode="w", encoding="SHIFT-JIS") as hospital_file:
        hospital_writer = csv.writer(
            hospital_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        hospital_writer.writerow(columnName)
        hospital_writer.writerows(matchedData)
    print("Csv download completed")
    print("End get Information From AruNavi")


def acceptInformationFromUser(webName, placeName, deptName):
    if webName == "aruNavi":
        print("get Information From AruNavi")
        if deptName == "spot":
            url = "https://arbeit.doctor-navi.jp/sh"
            driver.get(url)
            like = driver.find_elements_by_css_selector('[href="#sh_area_modal"]')
            for x in range(0, len(like)):
                if like[x].is_displayed():
                    like[x].click()
                    time.sleep(1)
            time.sleep(2)
            tb = driver.find_elements_by_class_name("prefecture-select-area")
            for y in range(0, len(tb)):
                tb1 = tb[y].find_elements_by_css_selector("th")
                for z in range(0, len(tb1)):

                    if tb1[z].find_element_by_css_selector("label").text in placeName:
                        inputCheck = tb1[z].find_element_by_css_selector("input")
                        inputCheck.click()
                        time.sleep(1)
            selectButton = driver.find_elements_by_class_name("modal-button-area")
            selectButton[0].click()
            time.sleep(2)
            searchButton = driver.find_elements_by_css_selector('[alt="絞り込む"]')
            if searchButton[1].is_displayed():
                searchButton[1].click()
                time.sleep(2)
            baseUrl = driver.current_url
            # print(baseUrl)
            bookmarkedUrl = driver.find_element_by_css_selector(
                '[alt="検討中リスト"]'
            ).get_attribute("href")
            fileName = "アルなび_スポット"
            print(fileName)
            getInformationFromAruNavi(baseUrl, bookmarkedUrl, fileName)


placeArray = ["秋田県", "東京都", "九州・沖縄地方"]
acceptInformationFromUser("aruNavi", placeArray, "spot")

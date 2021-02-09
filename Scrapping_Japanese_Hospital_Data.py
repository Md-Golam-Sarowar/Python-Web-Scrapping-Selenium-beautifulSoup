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
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
# driver = webdriver.Chrome(options=options)

data_array = []
csvArrayData = []
CsvReadData = []


def processingUplodatedCsvData(CsvReadData):
    tempArray = np.array(CsvReadData)
    csvArray = tempArray[:, 1]
    csvArrayData = np.unique(csvArray)
    return csvArrayData


def getInformationFromAruNavi(baseUrl, bookmarkedUrl, fileName, driver, deptName):

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
    for a in range(0, 2):
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
                    wait = WebDriverWait(driver, 10)
                    temp = nextButtonClick[click].get_attribute("href")
                    driver.get(temp)

        print("Pagination starting: " + str(a + 1))
        like = driver.find_elements_by_class_name("bookmark-action")
        for x in range(0, len(like)):
            if like[x].is_displayed():
                like[x].click()
                counter += 1
                time.sleep(1)

        print("Bookmarked completed " + str(counter))
        data1 = ""
        data2 = ""
        data3 = ""
        data4 = ""
        data5 = ""
        data6 = ""
        data7 = ""
        data8 = ""
        driver.get(bookmarkedUrl)

        wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "utility-module-job-summary")
            )
        )
        divAll = driver.find_elements_by_class_name("utility-module-job-summary")

        for c in range(0, counter):
            print("Data getting from bookmarked no: " + str(c + 1))

            wait = WebDriverWait(driver, 10)
            name = divAll[0].find_element_by_class_name("clinic").text

            data1 = name
            job = divAll[0].find_element_by_css_selector('[alt="求人詳細を見る"]')
            data_url = job.find_element_by_xpath("..").get_attribute("href")
            page = requests.get(data_url)
            soup = BeautifulSoup(page.content, "html.parser")
            tb = soup.find_all("table", class_="detail-entry-info")
            for single_table in tb:
                tb_tr = single_table.find("tr")
                if "募集背景" not in tb_tr.text:
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

                                        if deptName == "tenshoku":
                                            temp1 = str(single_tr.text).split(")")[0]
                                            data2 = temp1.split("勤務日")[1]
                                        else:
                                            temp1 = (
                                                str(single_tr.text).split(")")[0] + ")"
                                            )
                                            data2 = temp1.split("勤務日")[1]
                                    elif "勤務時間" in single_tr.text:
                                        if deptName == "spot":
                                            part = single_tr.find_all("div")
                                            for i in range(0, len(part)):
                                                if i == 0:
                                                    data3 = part[i].text
                                                elif i == 1:
                                                    data4 = part[i].text
                                        elif deptName == "teiki":
                                            data3 = single_tr.find("div").text
                                            data4 = single_tr.find("ul").text
                                        elif deptName == "tenshoku":
                                            part = single_tr.find_all("li")
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
                                        if deptName == "spot":
                                            temp3 = (
                                                str(single_tr.text).split("円")[0] + "円"
                                            )
                                            data6 = temp3.split("与")[1]
                                        elif deptName == "teiki":
                                            temp3 = (
                                                str(single_tr.text).split("円")[0] + "円"
                                            )
                                            data6 = temp3.split("与")[1]
                                        elif deptName == "tenshoku":
                                            temp3 = (
                                                str(single_tr.text).split("円")[0] + "円"
                                            )
                                            data6_part = temp3.split("与")
                                            data6 = data6_part[1] + data6_part[2]
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

            deleteAll = divAll[0].find_element_by_class_name("bookmark-action")
            if deleteAll.is_displayed():
                deleteAll.click()
                alert = driver.switch_to.alert
                time.sleep(2)
                alert.accept()
            print("Deleted Bookmarked no: " + str(c + 1))
            # time.sleep(2)
            if len(divAll) != 1:
                wait = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "utility-module-job-summary")
                    )
                )
            divAll = driver.find_elements_by_class_name("utility-module-job-summary")

    driver.close()
    fileDownload = csvCreateFunction(data_array, fileName)
    print(fileDownload)
    return fileDownload


def csvCreateFunction(data_array, fileName):
    # data_array = final_data_array
    unMatchedData = []
    matchedData = []
    csvArrayData = processingUplodatedCsvData(CsvReadData)
    for singleRow in data_array:
        flag = 0
        for singleValue in csvArrayData:
            # print(singleValue)
            if re.sub(r"[\n\t\s]*", "", singleValue) in re.sub(
                r"[\n\t\s]*", "", singleRow[0]
            ):
                matchedData.append(singleRow)
                flag = 1
                break
        if flag == 0:
            unMatchedData.append(singleRow)
    print("Matched Data: " + str(len(matchedData)))
    print("Not Matched Data: " + str(len(unMatchedData)))
    filename = "final_data.csv"
    columnName = ["病院名", "勤務日", "勤務時間1", "勤務時間2", "募集科目", "給与", "所在", "施設", "URL"]
    with open(filename, mode="w", encoding="utf-8") as hospital_file:
        hospital_writer = csv.writer(
            hospital_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        hospital_writer.writerow(columnName)
        hospital_writer.writerows(unMatchedData)

    data_array.clear()

    print("Csv download completed")
    print("End get Information From AruNavi")

    return filename


def acceptInformationFromUser(webName, placeName, deptName, driver):
    if webName == "aruNavi":
        print("get Information From AruNavi")
        if deptName == "spot":
            print("Team: Spot")
            url = "https://arbeit.doctor-navi.jp/sh"
            fileName = "アルなび_スポット"
            area_modal_href = '[href="#sh_area_modal"]'
            searchButtonIndex = 1
            with open("他媒体求人マッチング用_new.csv", encoding="SHIFT-JIS") as csvfile:

                reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
                for row in reader:  # each row is a list
                    CsvReadData.append(row)

        elif deptName == "teiki":
            print("Team: Teiki")
            url = "https://arbeit.doctor-navi.jp/re"
            fileName = "アルなび_teiki"
            area_modal_href = '[href="#re_area_modal"]'
            searchButtonIndex = 1
            with open("他媒体求人マッチング用_new.csv", encoding="SHIFT-JIS") as csvfile:

                reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
                for row in reader:  # each row is a list
                    CsvReadData.append(row)

        elif deptName == "tenshoku":
            print("Team: Tenshoku")
            url = "https://tenshoku.doctor-navi.jp/"
            fileName = "アルなび_tenshoku"
            area_modal_href = '[href="#te_area_modal"]'
            searchButtonIndex = 0
            with open("他媒体求人マッチング用_new.csv", encoding="SHIFT-JIS") as csvfile:

                reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
                for row in reader:  # each row is a list
                    CsvReadData.append(row)

        driver.get(url)
        like = driver.find_elements_by_css_selector(area_modal_href)
        for x in range(0, len(like)):
            wait = WebDriverWait(driver, 10)
            if like[x].is_displayed():
                like[x].click()

        wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "prefecture-select-area"))
        )
        tb = driver.find_elements_by_class_name("prefecture-select-area")
        for y in range(0, len(tb)):
            tb1 = tb[y].find_elements_by_css_selector("th")
            for z in range(0, len(tb1)):
                wait = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "label"))
                )
                if tb1[z].find_element_by_css_selector("label").text in placeName:
                    inputCheck = tb1[z].find_element_by_css_selector("input")
                    inputCheck.click()
                    # time.sleep(1)
        selectButton = driver.find_elements_by_class_name("modal-button-area")
        selectButton[0].click()

        status = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[alt="絞り込む"]'))
        )
        searchButton = driver.find_elements_by_css_selector('[alt="絞り込む"]')
        if searchButton[searchButtonIndex].is_displayed():
            searchButton[searchButtonIndex].click()
            # time.sleep(2)
        baseUrl = driver.current_url
        # print(baseUrl)
        status = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[alt="検討中リスト"]'))
        )
        bookmarkedUrl = driver.find_element_by_css_selector(
            '[alt="検討中リスト"]'
        ).get_attribute("href")

        fileDownload = getInformationFromAruNavi(
            baseUrl, bookmarkedUrl, fileName, driver, deptName
        )
        print("came to last")
        print(fileDownload)
        return fileDownload


# placeArray = ["秋田県", "東京都", "九州・沖縄地方"]
# acceptInformationFromUser("aruNavi", placeArray, "spot")

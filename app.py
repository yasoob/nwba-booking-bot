import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def next_7_dates():
    today = datetime.datetime.today()
    date_list = []
    for x in range(0,7):
        new_date = today + datetime.timedelta(days=x)
        date_list.append(new_date.strftime('%Y-%m-%d'))
    return date_list

def login(browser):
    print("[+] Logging in.")
    browser.find_element("name", "username").send_keys("hi@yasoob.me")
    browser.find_element("name", "password").send_keys("4&U8asvoa@zq1q")
    browser.find_element("xpath", "//input[@type='SUBMIT']").click()

def reserve_time(browser, favorite_times):
    for fav_time in favorite_times:
        booking_link = browser.find_element("xpath", f"//div[text()='{fav_time}']")
        full = 'sessionFull' in booking_link.get_attribute('class')
        if not full:
            booking_link.click()
        else:
            continue
        browser.find_element("xpath", "//a[text()='Reserve']").click()
        reserved = "Reserved" in browser.find_element("xpath", "//div[@class='bold green']").text
        if reserved:
            return True, fav_time
    return False, None

def main():
    browser = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver')
    url = "https://northwestbadmintonacademy.sites.zenplanner.com/login.cfm"
    browser.get(url)

    login(browser)

    timeout_secs = 20
    calendar_btn = WebDriverWait(browser, timeout_secs)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@id='idNavigation']//li[2]//a")))
    # calendar_btn = browser.find_element("xpath", "//td[@id='idNavigation']//li[2]//a")
    user_id = calendar_btn.get_attribute('href').split('=')[-1].split(':')[-1]
    calendar_btn.click()

    favorite_times = ["5:00 PM", "6:00 PM"]
    booked_details = []
    for count, date in enumerate(next_7_dates()):
        if len(booked_details) == 3 and count <= 5:
            print(f"[+] Already booked 3 weekdays. Skipping {date}")
            continue
        print(f"[+] Trying to look for timeslots on {date}")
        calendar_date_link = (f"https://northwestbadmintonacademy.sites.zenplanner.com/calendar.cfm?"
            f"DATE={date}&calendarType=PERSON:{user_id}&VIEW=LIST&PERSONID={user_id}")
        browser.get(calendar_date_link)
        reserved, reservation_time = reserve_time(browser, favorite_times)
        if reserved:
            booked_details.append((date, reservation_time))

    print("[+] I was able to successfully reserve the following date/times:")
    for date, reservation_time in booked_details:
        print(f"\t{date}: {reservation_time}")

if __name__ == "__main__":
    main()
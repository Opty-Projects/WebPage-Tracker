from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def startDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    drv = webdriver.Chrome(chrome_options=chrome_options)
    drv.set_page_load_timeout(5)
    drv.set_script_timeout(5)
    return drv


def doLogin(session, lin):
    drv = startDriver()
    try:
        drv.get(lin["Link"])
        ele = None
        for nam, val in lin["Credentials"].items():
            ele = drv.find_element_by_name(nam.lower())
            ele.send_keys(val)
        ele.submit()
        for cok in drv.get_cookies():
            session.cookies.set(cok["name"], cok["value"])
    except Exception as e:
        print("Error: '{}'".format(e))
    finally:
        drv.close()

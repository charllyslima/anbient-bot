import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

global browser

browser = webdriver.Chrome(executable_path=r"./chromedriver.exe")

browser.get('https://www.anbient.com')


def procura():
    print("Digite o anime que deseja buscar: ")
    input_search = browser.find_element(By.ID, 'edit-search-api-views-fulltext')
    anime_name = input()
    input_search.send_keys(anime_name)
    input_search.send_keys(Keys.ENTER)
    return browser.find_elements(By.XPATH, "//a[@rel='bookmark']")


def selecionar(resultados):
    print("Encontramos estes resultados:")
    count = 1
    for value in resultados:
        print(str(count) + ' - ' + value.text)
        count = count + 1
    print("Qual destes deseja baixar?")
    click = input()
    resultados[int(click) - 1].click()


def captura_links():
    downloader = "zippyshare"
    zippyshare = browser.find_element(By.XPATH, '//a[contains(@href, "%s")]' % downloader)
    zippyshare.click()
    time.sleep(2)
    browser.find_element(By.CLASS_NAME, downloader).find_element(By.CLASS_NAME, 'list').click()
    time.sleep(3)
    lista = browser.find_element(By.TAG_NAME, 'textarea').get_attribute('value')
    links = lista.split("\n")
    return links


def criar_pasta():
    name = browser.find_element(By.ID, "page-title").get_attribute('innerHTML')
    newpath = "D:\TeraBoxDownload\\animes\\" + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def download_concluido(file):
    print(file)
    while not os.path.exists(file):
        print("Baixando...")
        time.sleep(5)
    print("Baixado!")


selecionar(procura())
links = captura_links()
path = criar_pasta()
browser.close()
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': path}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)

for value in links:
    if value != "":
        browser.get(value)
        time.sleep(10)  # tempo para site não identificar que é um bot
        download = browser.find_element(By.ID, 'dlbutton').get_attribute("href")
        browser.get(download)
        file = browser.find_elements(By.TAG_NAME, 'font')
        download_concluido(path + '\\' + file[3].get_attribute('innerHTML'))

browser.close()

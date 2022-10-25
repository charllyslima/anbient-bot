import os
import time
import _thread

from tkinter import *
from tkinter.ttk import Progressbar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

# Global variables
links = []
path = ''
main_path = "D:\\TeraBoxDownload\\animes\\"
name = ''
progress = ''
list_results = []


# threads
def search_th(text_search):
    clear_list()
    title["text"] = "Procurando... Por favor aguarde."
    _thread.start_new_thread(search, (text_search,))


def open_th(link):
    title["text"] = "Capturando links... Por favor aguarde."
    clear_list()
    _thread.start_new_thread(capture_links, (link,))


def clear_list():
    global list_results
    for item in list_results:
        item.destroy()
    list_results = []


def capture_links(link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(link)
    global name
    name = browser.find_element(By.ID, 'page-title').text
    create_directory()
    downloader = "zippyshare"
    WebDriverWait(browser, 20).until(
        ec.presence_of_element_located((By.XPATH, '//a[contains(@href, "%s")]' % downloader))).click()
    try:
        WebDriverWait(browser, 20).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'list'))).click()
        lista = WebDriverWait(browser, 20).until(
            ec.visibility_of_element_located((By.TAG_NAME, 'textarea'))).get_attribute('value')
        global links
        links = lista.split("\n")

    except Exception as ex:
        list_elem = browser.find_element(By.CLASS_NAME, 'zippyshare')
        links_elem = list_elem.find_elements(By.TAG_NAME, 'a')
        links = []
        for elem in links_elem:
            lk = elem.get_attribute('href')
            if lk != 'http://tasks.anbient.com/' and lk is not None:
                links.append(elem.get_attribute('href'))
    global progress
    progress = Progressbar(
        window,
        orient='horizontal',
        mode='determinate',
        length=100
    )
    progress.grid(column=0, row=4)
    progress.pack_forget()
    browser.close()
    title["text"] = "Iniciando download... Por favor aguarde."
    _thread.start_new_thread(execute, ())


def create_directory():
    global name
    global path
    name = name.replace(":", " - ").title()
    path = main_path + name

    if not os.path.exists(path):
        os.makedirs(path)


def check_download(file_name):
    while not os.path.exists(path + '\\' + file_name):
        time.sleep(5)


def execute():
    count = 0
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')
    prefs = {'download.default_directory': path}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=chrome_options)

    while count < (len(links) - 1):
        progress['value'] = 100 * count / (len(links) - 1)
        browser.get(links[count])
        try:
            download = WebDriverWait(browser, 20).until(
                ec.visibility_of_element_located((By.ID, 'dlbutton'))).get_attribute('href')
            browser.get(download)
            file = browser.find_elements(By.TAG_NAME, 'font')
            file_name = file[3].get_attribute('innerHTML')
            check_download(file_name)
            count = count + 1
        except:
            title["text"] = "O arquivo solicitado esta com link quebrado! Seguindo para o proximo arquivo"
            time.sleep(5)
            title["text"] = "Iniciando download... Por favor aguarde."
            count = count + 1

    browser.close()
    progress['value'] = 100
    title["text"] = "Download Concluido com sucesso!"
    progress.destroy()


def search(text_search):
    global list_results

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.anbient.com/search?search_api_views_fulltext=' + text_search)

    result = browser.find_elements(By.XPATH, "//a[@rel='bookmark']")
    count = 1
    window.update()
    title["text"] = "Encontramos estes animes, clique no que deseja baixar."

    for value in result:
        window.update()
        list_results.append(Label(window, text=value.text, fg="blue", cursor="hand2"))
        list_results[count - 1].grid(column=0, row=count + 3)
        href_value = value.get_attribute('href')
        list_results[count - 1].bind("<Button-1>", lambda e, url=href_value: open_th(url))
        count = count + 1

    browser.close()


window = Tk()
window.title('Anbient Bot Donwloader')

text = Label(window, text="Pesquise o anime no campo abaixo")
text.grid(column=0, row=0)

input = Entry(window, width=50)
input.grid(column=0, row=1)

button = Button(window, text="Buscar", command=lambda: search_th(input.get()))
button.grid(column=0, row=2)

title = Label(window, text="")
title.grid(column=0, row=3)

window.mainloop()

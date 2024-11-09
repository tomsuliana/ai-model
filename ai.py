import requests
from html.parser import HTMLParser
from langdetect import detect, DetectorFactory
from queue import Queue
import json
import re
from bs4 import BeautifulSoup
import subprocess
import os
import psutil
import time

model = " "


class MyHTMLParser(HTMLParser):


    def handle_data(self, data):
        if len(data.strip()) != 0:
            stringarray = data.split(". ")
            # print("Encountered some data  :", stringarray)


            # print(len(stringarray)/2)
            for i in range(int(len(stringarray)/2)):
                # print(stringarray[i*2 - 1] + stringarray[i*2])
                f = open('buffer.txt', 'w')
                f.write(stringarray[i*2 - 1] + stringarray[i*2])
                f.close()
                get_summary()
                print(str(i*2))
                print(str(len(stringarray))) 
                print("обработано строк " + str(i*2) + " из " + str(len(stringarray)))


           # try:
                # if not ("About Confluence" in data or "Available Gadgets" in data or "serverDuration" in data or "Delivrer au patient" in data or "Restrictions" in data or "function" in data):
                    # f = open('info.txt', 'a')
                    # f.write(data)
                    # f.write('\n')
                    # f.close()
            # except Exception:
              #  print("error detected")




def getFrench(stringname, cookies):

    try:
        page = requests.get(stringname, cookies=cookies)





        soup = BeautifulSoup(page.text, features="html.parser")

        title = soup.find('h1', id='title-text').get_text()

        f = open('info.txt', 'a')
        f.write(title)
        f.close()

        main_content = soup.find('div', id='main-content')

        # f = open('info.txt', 'a')
        # f.write(main_content)
        # f.close()

        # print(main_content)







        parser = MyHTMLParser()


        parser.feed(main_content.text)

    except OSError:
        print("connection lost")
    except AssertionError:
        print("assertion error detected")
    else:
        print('ok')


def get_info(word):
    url = "https://docus.everys.com"

    params = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0',
        'Content-Length': '94',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__ddg1_=qfumiqex8K2qGvVADIo0; JSESSIONID=E8A5DF8AC7E0314CCA7913B4F1166C71',
        'Origin': 'https://docus.everys.com',
        'Referer': 'https://docus.everys.com/login.action?os_destination=%2Findex.action&permissionViolation=true',
        'Sec-Ch-Ua-Mobile': '?0', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    session = requests.session()
    req = session.post(url, json=params,
                       data={'os_username': 'Ulyana.Tomskaya', 'os_password': '6SFhesD2zN', 'login': 'Log in',
                             'os_destination': '/index.action'})
    cookies = requests.utils.dict_from_cookiejar(session.cookies)

    search_url = "https://docus.everys.com/rest/api/search?cql=siteSearch%20~%20%22" + word + "%22%20AND%20type%20in%20(%22space%22%2C%22user%22%2C%22page%22%2C%22blogpost%22%2C%22attachment%22)&start=0&limit=20&excerpt=highlight&expand=space.icon&includeArchivedSpaces=false&src=next.ui.search"

    responce = requests.get(search_url, cookies=cookies)

    respjson = responce.json()



    queue = Queue()

    if "results" in respjson:
        print("results detected")
        respjson = respjson['results']
        i = 0
        for cont in respjson:
            if "url" in cont:
                currenturl = cont['url']
                docx = re.search('.docx$', currenturl)
                pdf = re.search('.pdf$', currenturl)
                pptx = re.search('.pptx$', currenturl)
                mp4 = re.search('.mp4$', currenturl)
                if docx == None and pdf == None and pptx == None and mp4 == None and i < 1:
                    i = i + 1
                    print(url + currenturl)
                    print('\n')
                    queue.put(url + currenturl)

        for i in range(1):
            if not queue.empty():
                print("queue not empty")
                new_elem = queue.get()
                getFrench(new_elem, cookies)
    else:
        print("no results")


def get_information(wordlist):

    f = open(wordlist, 'r')
    i = 0
    iter = 0
    while i < 2 and iter < 30:
        word = f.readline()
        if word != "\n" and len(word) > 2:
            print(word)
            print(len(word))
            get_info(word)
            i = i + 1
        iter = iter + 1
    f.close()

def kill(proc_pid):
	process = psutil.Process(proc_pid)
	for proc in process.children(recursive=True):
		proc.kill()
	process.kill()

words_count = 0

def get_summary():
    global words_count
    global model
    print("summary: " + model)
    executable_name = "/home/user/lama/llama.cpp/./main"
    args = ["-m", "/home/user/lama/llama.cpp/models/7B/" + model, "--threads", "12", "-c", "2048", "-ins", '--in-prefix', '" "', "--color", "--file", "/home/user/nanogpt/buffer.txt"]
    input_str = "Сделай очень краткий пересказ этого текста в 1-2 предложения\n"
    process = subprocess.Popen([executable_name] + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    print("before communication")
    input_sent = False
    count = 0
    while True:
        try:
            if not input_sent:
                input_sent = True
                process.communicate(input=input_str.encode(), timeout = 10)
            else:
                process.communicate(timeout = 4)
        except subprocess.TimeoutExpired:
            line = process.stdout.readline()
            print(line.decode('UTF-8'))
            if ">" in line.decode('UTF-8'):
                count = count + 1
                if count >= 2:
                    print("signal")
                    process.kill()
                    print("killing")
                    break
                else:
                    line  = line.decode('UTF-8')
                    line = line.replace('> " "', ' ')
                    line = line.replace('Текст', ' ')
                    words = line.split()
                    words_count = words_count + len(words)
                    print(words_count)
                    if words_count < 2000:
                        f = open('info.txt', 'a')
                        f.write(line)
                        f.close()
                    else:
                        break
        print("before trying")
    print("Сторонняя программа завершилась с кодом:", process.returncode)


def get_main_words(string):
    global model
    print("main words: " + model)
    input_str = "Identifiez les 3 mots les plus importants de ce texte: " + string + " Afficher uniquement une liste de mots importants par ordre décroissant d'importance. Écrivez-les un mot par ligne.\n"
    #input_str = "Identifiez les 3 mots les plus importans de ce texte et écrivez avec une virgule : " + string
    executable_name = "/home/user/lama/llama.cpp/./main"
    args = ["-m", "/home/user/lama/llama.cpp/models/7B/" + model, "--threads", "12", "-c", "2048", "-ins", '--in-prefix', '" "', "--color"]
    process = subprocess.Popen([executable_name] + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, text=True)
    print("before communication")
    #start_time = time.time()
    #while time.time() - start_time < 10:
    input_sent = False
    array = []
    out_text = ""
    the_end = False
    while True:
        try:
            if not input_sent:
                input_sent = True
                process.communicate(input=input_str, timeout = 10)
            else:
                process.communicate(timeout = 1)
        except subprocess.TimeoutExpired:
            line = process.stdout.readline()
            while line != None and line != "":
                out_text += line
                print(line)
                #process.stdout.flush()
                if ">" in line:
                    print("signal")
                    process.kill()
                    print("killing")
                    the_end = True
                else:
                    array = line.split(", ")
                    print(array)
                    for i in range(len(array)):
                        f = open('wordlist.txt', 'a')
                        f.write(array[i])
                        f.write('\n')
                        f.close()
                line = process.stdout.readline()
        print("before trying")
        if the_end:
            break

    print("out " + out_text)


def get_answer(question):
    global model
    print("answer: " + model)
    executable_name = "/home/user/lama/llama.cpp/./main"
    args = ["-m", "/home/user/lama/llama.cpp/models/7B/" + model , "--threads", "12", "-c", "2048", "-ins", '--in-prefix', '" "', "--color", "--file", "/home/user/nanogpt/info.txt"]
    input_str = question
    process = subprocess.Popen([executable_name] + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    print("before communication")
    input_sent = False
    count = 0
    answer = ""
    biganswer = ""
    the_end = False
    while True:
        try:
            if not input_sent:
                input_sent = True
                process.communicate(input=input_str.encode(), timeout = 15)
            else:
                process.communicate(timeout = 4)
        except subprocess.TimeoutExpired:
            line = process.stdout.readline()
            print(line.decode('UTF-8'))
            c = 0
            while line != None and line != "" and line.decode('UTF-8') != "" and c <= 20: 
                if line.decode('UTF-8').find(">") == 0:
                    count = count + 1
                    if count >= 2:
                        print("signal")
                        process.kill()
                        print("killing")
                        the_end = True
                    else:
                        line  = line.decode('UTF-8')
                        line = line.replace('> " "', ' ')
                        f = open( 'res.txt', 'a')
                        f.write(line)
                        f.close() 
                        biganswer = biganswer + line
                else:
                    biganswer = biganswer + line.decode('UTF-8')
                line = process.stdout.readline()
                print(line.decode('UTF-8'))
                print(len(line.decode('UTF-8')))
                print("line read")
                c = c + 1
        print("before trying")
        if the_end:
            break
    print("Сторонняя программа завершилась с кодом:", process.returncode)
    print(answer)
    biganswer = biganswer.replace('\n', '<br>')
    print(biganswer)
    return biganswer




def resolve_problem(newstr, selected_model):
    global model
    model = selected_model
    f = open('wordlist.txt', 'w')
    f.close()
    f = open('info.txt', 'w')
    f.write("Rappelez-vous ceci :")
    f.close()
    
    f = open('res.txt', 'w')
    f.close()
    # newstr = "J'ai un problème avec Ségur. Comment déployer un module Segure en pharmacie ?"
    
    get_main_words(newstr)

    get_information('wordlist.txt')
    
    result = get_answer(newstr)
    print("RESULT: ")
    print(result)
    first_line = result.split('<br>')[1]
    print(first_line)
    if len(first_line.strip()) != 0:
        try:
            if detect(first_line) == 'ru':
                result = result.replace(first_line, ' ')
        except Exception:
            print("error detected")
    result = result.replace('" "', ' ')
    return result
    










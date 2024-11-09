# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from html.parser import HTMLParser
from langdetect import detect, DetectorFactory
from queue import Queue




class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            print("Encountered a start tag:", tag, " ", attrs)
            for attr, value in attrs:
                if attr == "href" and value.strip() != "":
                        if value.strip()[0] == '/':
                            print (attr, value)
                            if value != "/logout.action":
                                f = open('visitedlinks.txt', 'r')
                                lines = f.readlines()
                                filehaslink = False
                                for line in lines:
                                    print(line.strip(), "    ", value.strip())
                                    if line.strip() == value.strip():
                                        filehaslink = True
                                        print("file has link")
                                f.close()

                                if not filehaslink:
                                    print (value.strip(), "     ", "putted")
                                    if not value.strip() in a:
                                        q.put(value.strip())
                                        a.add(value.strip())

                                    f = open('bufferlinks.txt', 'a')
                                    f.write(value.strip())
                                    f.write('\n')
                                    f.close

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if len(data.strip()) != 0:
            # print("Encountered some data  :", data)

            try:
                if detect(data) == 'fr':
                    f = open('frenchtext.txt', 'a')
                    f.write(data)
                    f.write('\n')
                    f.close()
            except Exception:
                print("error detected")




def getFrench(stringname):

    f = open('bufferlinks.txt', 'w')
    f.close()

    try:
        page = requests.get(url + stringname, cookies=cookies)


        # print(page.text)

        parser = MyHTMLParser()


        parser.feed(page.text)

    except OSError:
        print("connection lost")
    except AssertionError:
        print("assertion error detected")
    else:
        f = open('visitedlinks.txt', 'a')
        f.write(stringname)
        f.write('\n')
        f.close()










# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    url = "https://docus.everys.com"

    params = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Content-Length': '94',
               'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': '__ddg1_=qfumiqex8K2qGvVADIo0; JSESSIONID=E8A5DF8AC7E0314CCA7913B4F1166C71',
               'Origin': 'https://docus.everys.com', 'Referer': 'https://docus.everys.com/login.action?os_destination=%2Findex.action&permissionViolation=true',
               'Sec-Ch-Ua-Mobile': '?0', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    session = requests.session()
    req = session.post(url, json=params, data= { 'os_username': 'Ulyana.Tomskaya' , 'os_password': '6SFhesD2zN', 'login': 'Log in', 'os_destination': '/index.action' })
    cookies = requests.utils.dict_from_cookiejar(session.cookies)

    # print(req.text)
    # print(cookies)

    # responce = requests.get('https://docus.everys.com/', cookies=jar)
    # print(responce.text)

    # session = requests.session()
    # session.get("https://docus.everys.com")
    # cookies = requests.utils.dict_from_cookiejar(session.cookies)
    # print(cookies)

    # cookies = requests.utils.dict_from_cookiejar(req.cookies)

    # print(cookies)


    # session = requests.session()
    # cookies = requests.utils.cookiejar_from_dict(cookies)
    # session.cookies.update(cookies)
    # print(session.get("https://docus.everys.com").text)

    f = open('frenchtext.txt', 'w')
    f.close()
    f = open('notvisitedlinks.txt', 'w')
    f.close()
    f = open('bufferlinks.txt', 'w')
    f.close()
    # f = open('visitedlinks.txt', 'w')
    # f.close()

    q = Queue()
    a = set()

    q.put("/")
    a.add("/")
    # q.put("/pages/viewpage.action?pageId=205914890")

    while q.not_empty:
        new_elem = q.get()
        print(url + new_elem)
        getFrench(new_elem)
        a.remove(new_elem)

    # getFrench("https://docus.everys.com")
    # getFrench("https://docus.everys.com/browsepeople.action")

    # f = open('notvisitedlinks.txt', 'r')
    # while True:
    #     line = f.readline()
    #     if not line:
    #         break
    #     getFrench(url + line)
    #     print(url + line)
    # f.close()







# See PyCharm help at https://www.jetbrains.com/help/pycharm/

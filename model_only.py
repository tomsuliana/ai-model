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

def get_answer(question):
    global model 
    print(model)
    executable_name = "/home/ubuntu/ai_program/lama/llama.cpp/./main"
    args = ["-m", "/home/ubuntu/ai_program/lama/llama.cpp/models/7B/" + model , "--threads", "8", "-c", "2048", "-ins", '--in-prefix', '" "', "--color"]
    input_str = question
    process = subprocess.Popen([executable_name] + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    print("before communication")
    input_sent = False
    count = 0
    result = ''
#    while True:
 #       try:
  #          if not input_sent:
   #             input_sent = True
    #            print(input_sent)
     #           process.communicate(input=input_str.encode(), timeout = 10)
      #      else:
       #         print(input_str.encode())
        #        process.communicate(timeout = 4)
       # except subprocess.TimeoutExpired:
        #    line = process.stdout.readline()
         #   print(line.decode('UTF-8'))
          #  if ">" in line.decode('UTF-8'):
           #     count = count + 1
            #    if count >= 2:
             #       print("signal")
              #      process.kill()
               #     print("killing")
                #    break
                #else:
                 #   line  = line.decode('UTF-8')
                  #  line = line.replace('> " "', ' ')
                   # line = line.replace('Текст', ' ')
                    #result = result + line
            #else:
             #   result = result + line.decode('UTF-8')
        #print("before trying")
        #print(model)
    #print("Сторонняя программа завершилась с кодом:", process.returncode)
    #result = result.replace('\n', '<br>')
    time.sleep(5)
    result = "Привет! Очень жаль, что у тебя сломался фонарь. Можешь точнее сказать, в каком месте это произошло?"
    return result



def answer_question(newstr, selected_model):
    global model
    model = selected_model
    result = get_answer(newstr)
    print("RESULT: ")
    print(result)
    return result
    










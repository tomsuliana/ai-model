from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
from func import *
from ai import *
from model_only import *
import os

app = Flask(__name__)
sock = Sock(app)


messages = []
server_enabled = True

@app.route('/')
def index():
         files = os.listdir('/media/uliana/Data/Article/models')
         return render_template('index.html', server_enabled=server_enabled, files=files)


# @app.route('/', methods=['POST'])
# def send_message():
	# data = request.get_json()
	# message = {
		# 'text': data['text']
	# }
	# messages.append(message)
	# return render_template('index.html', messages=messages)


@app.route('/', methods=['GET'])
def get_messages():
	last_message_id = request.args.get('last_message_id')
	new_messages = messages[int(last_message_id):]
	return render_template('index.html', messages=messages)


@sock.route('/echo')
def echo(ws):
    global server_enabled
    while True:
        if server_enabled:
            dict = ws.receive()
            data = dict.partition(' ')[2]
            model = data.partition(' ')[0]
            data = data.partition(' ')[2]
            # if dict.split()[0] == "true":
            #     server_enabled = False
            #     answer = resolve_problem(data, model)
            #     server_enabled = True
            #     ws.send(answer)
            # else:
            server_enabled = False
            answer = answer_question(data, model)
            server_enabled = True
            ws.send(answer)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001)  # Теперь Flask обрабатывает запросы через порт 80


def disable_button():
    button = document.getElementById('sent-button')
    button.disabled = True


def enable_button():
    button = document.getElementById('sent-button')
    button.disabled = False


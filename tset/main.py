import webview
from model import Model
api = Model()

window = webview.create_window('Woah dude!', './main.html', js_api=api)
webview.start()
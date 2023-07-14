import webview
import sys
import urllib.request

def on_closing() -> None:
    cookies = window.get_cookies()

    url = f'{sys.argv[1]}/close?cookie={cookies}'
    urllib.request.urlopen(url)

window = webview.create_window(
    width=1280,
    height=720,
    min_size=(1280, 720),
    title= "Bard AI",
    url="https://bard.google.com"
)

window.events.closing += on_closing

webview.start(
    private_mode=False,
)
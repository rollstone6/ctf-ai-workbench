"""Exercise HTTP tooling and a real browser against a local benign fixture."""
import asyncio
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import shutil
import threading
import requests
from playwright.async_api import async_playwright

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        body='<html><meta charset="utf-8"><title>CTF Web 自检</title><button id="check">验证</button><p id="result"></p><script>document.querySelector("#check").onclick=()=>{document.querySelector("#result").textContent="页面交互通过"};</script></html>'.encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

async def check(url):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        try:
            page=await browser.new_page()
            await page.goto(url,wait_until='domcontentloaded')
            assert await page.title()=='CTF Web 自检'
            await page.locator('#check').click()
            assert await page.locator('#result').inner_text()=='页面交互通过'
        finally: await browser.close()

server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True)
thread.start()
try:
    url=f'http://127.0.0.1:{server.server_port}/'
    response=requests.get(url,timeout=5)
    assert response.status_code==200 and 'CTF Web 自检' in response.text
    asyncio.run(check(url))
    print('Web 工具自检通过：HTTP 中文正文、Chromium 渲染及按钮交互。')
finally:
    server.shutdown()
    server.server_close()
    thread.join()

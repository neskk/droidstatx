#!/usr/bin/python3

import hashlib
import urllib.request
import os
import sys
import json

def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
    total_size = response.getheader('content-length').strip()
    total_size = int(total_size)
    bytes_so_far = 0
    data = []

    while 1:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break

        data.append(chunk)
        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)

    return b"".join(data)

if __name__ == '__main__':
    print("[-]Downloading latest Apktool version...")
    response = urllib.request.urlopen("https://api.github.com/repos/iBotPeaches/Apktool/releases/latest").read()
    jsonData = json.loads(response.decode('utf-8'))
    url = jsonData["assets"][0]["browser_download_url"]
    response = urllib.request.urlopen(url)
    data = chunk_read(response, report_hook=chunk_report)
    cwd = os.getcwd()
    directories = ["/output_xmind", "/output_apktool", "/output_txt"]
    for directory in directories:
        if not os.path.exists(cwd + directory):
            os.makedirs(cwd + directory)
    with open(cwd + "/apktool.jar", 'wb') as f:
        f.write(data)
    parent = os.path.dirname(cwd)
    os.system("pip3 install -r requirements.txt --upgrade")

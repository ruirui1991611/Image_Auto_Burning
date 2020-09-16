#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 注: 公司相关的名称用xxx代替

import ssl
import sys
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

url_prefix = "https://jenkins-sh.xxx.com/job/Linux/job/"
platform = ""
firmware_index = ""
jenkins_url = ""
reg_pattern = ""

def usage():
    print("usage: %s <platform/group_name, eg:C1,C2,A1,IPC(G12B)/BR2020> <firmware_index>" % (sys.argv[0]))

if len(sys.argv) != 3:
    if len(sys.argv) == 2 and sys.argv[1] == "BR-2020":
        group_name = sys.argv[1]
        platform = input("Please input platform(eg:AE400-Fastboot_K4.19):")
        arch = input("Please input architecture(a32/a64/a6432):")
        firmware_index = input("Please input firmware index:")
        jenkins_url = url_prefix + group_name + "/" + "ARCH=" + arch + ",PLATFORM=" + platform + ",label=walle07-sh/" + firmware_index
        reg_pattern = platform + "_" + arch + "/$"
    else:
        print("wrong arguments.")
        usage()
        exit(0)
else:
    platform = sys.argv[1]
    firmware_index = sys.argv[2]
    jenkins_url = url_prefix + "Buildroot_" + platform + "/" + firmware_index
    reg_pattern = "release\W\d*/$";

print(jenkins_url)


'''
Download firmware and burn it
'''

# To solve the "certificate verify failed" error problem
context = ssl._create_unverified_context()
html = urlopen(jenkins_url, context=context)
bs = BeautifulSoup(html, "html.parser")
targets = bs.find_all("a")
for target in targets:
    href = target.get("href")
    if isinstance(href, str):
        regex = re.compile(r"" + reg_pattern)
        #if re.match("release.*?\/$", href):	# 仅从待匹配字符串或文本的开头开始匹配, 故本例无法使用
        if regex.findall(href):
            download_img_url = href + "xxx_upgrade_package.img"
            print(download_img_url)
            remote = urlopen(download_img_url)
            save_img = "%s/%s" % (os.getcwd(), "xxx_upgrade_package.img")
            with open(save_img, "wb") as fp:
                fp.write(remote.read())
            if platform == "PATCHBUILD":
                # g12b platform image burning
                print(os.popen("xxx_update_whole_package.bash %s" % (save_img)).read())
            else:
                # if platform == "C1" or platform == "C1_PatchBuild" or platform == "C2" or platform == "C2_PatchBuild":
                # c1 platform image burning
                print(os.popen("xxxx_burn_pkg -p %s" % (save_img)).read())





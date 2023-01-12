from urllib.request import urlopen

myURL = urlopen("https://www.baidu.com/")
print(myURL.read())
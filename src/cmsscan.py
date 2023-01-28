import requests
import hashlib
import threading
import time
threads = []  # 线程池
thread_max = threading.BoundedSemaphore(1000000)
'''------------------------指纹库内容------------------------'''
# 首页内容指纹库
body = {
    'content="WordPress': 'WordPress',
    'wp-includes': 'WordPress',
    'pma_password': 'phpMyAdmin',
    'hexo': 'hexo',
    'TUTUCMS': 'tutucms',
    'Powered by TUTUCMS': 'tutucms', 'Powered by 1024 CMS': '1024 CMS',
    'Discuz': 'Discuz',
    '1024 CMS (c)': '1024 CMS', 'Publish By JCms2010': '捷点 JCMS', }
# 请求头信息指纹库
head = {'X-Pingback': 'WordPress',
        'xmlrpc.php': 'WordPress', 'wordpress_test_cookie': 'WordPress', 'phpMyAdmin=': 'phpMyAdmin=',
        'adaptcms': 'adaptcms',
        'SS_MID&squarespace.net': 'squarespace建站',
        'X-Mas-Server': 'TRS MAS',
        'dr_ci_session': 'dayrui系列CMS',
        'http://www.cmseasy.cn/service_1.html': 'CmsEasy',
        'Osclass': 'Osclass',
        'clientlanguage': 'unknown cms rcms',
        'X-Powered-Cms: Twilight CMS': 'TwilightCMS',
        'IRe.CMS': 'irecms',
        'DotNetNukeAnonymous': 'DotNetNuke', }
# robots文件指纹库
robots = [
    'Tncms', '新为软件E-learning管理系统', '贷齐乐系统', '中企动力CMS', '全国烟草系统', 'Glassfish', 'phpvod', 'jieqi',
    '老Y文章管理系统',
    'DedeCMS']
# MD5指纹库
cms_rule = [
    '/images/admina/sitmap0.png|08cms|e0c4b6301b769d596d183fa9688b002a|',
    '/install/images/logo.gif|建站之星|ac85215d71732d34af35a8e69c8ba9a2|',
    '/jiaowu/hlp/Images/node.gif|qzdatasoft强智教务管理系统|70ee6179b7e3a5424b5ca22d9ea7d200|',
    '/theme/admin/images/upload.gif|sdcms|d5cd0c796cd7725beacb36ebd0596190|',
    '/themes/README.txt|drupal|5954fc62ae964539bb3586a1e4cb172a|',
    '/view/resource/skin/skin.txt|未知政府采购系统|61a9910d6156bb5b21009ba173da0919|',
    '/theme/admin/images/upload.gif|sdcms|d5cd0c796cd7725beacb36ebd0596190|',
    '/images/logout/topbg.jpg|TurboMail邮箱系统|f6d7a10b8fe70c449a77f424bc626680|', ]
# 特定网页指纹库
body_rule = [
    '/robots.txt|EmpireCMS|EmpireCMS|', '/images/css.css.lnk|KesionCMS(科讯)|kesioncms|',
    '/data/flashdata/default/cycle_image.xml|ecshop|ecshop|',
    '/admin/SouthidcEditor/Include/Editor.js|良精|southidc|', '/plugin/qqconnect/bind.html|PHP168(国徽)|php168|',
    '/SiteServer/Themes/Language/en.xml|SiteServer|siteserver|', '/system/images/fun.js|KingCMS|kingcms|',
    '/INSTALL.mysql.txt|Drupal(水滴)|drupal|', '/themes/default/style.css|ecshop|ECSHOP|',
    '/hack/gather/template/addrulesql.htm|qiboSoft(齐博)|qiboSoft|',
    '/phpcms/templates/default/wap/header.html|phpcms|phpcms']


def getweb(url):  # 尝试连接url中的网页并得到网页的请求头信息，网页的原始html，然后解码后成为中文的网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36'}
    try:
        r = requests.get(url, timeout=5, headers=headers)
        encoding = requests.utils.get_encodings_from_content(r.text)[0]
        url_content = r.content.decode(encoding, 'replace')
        return str(r.headers), r.content, url_content
    except:
        pass


def cmsScan(url):
    # 首先通过robots文件来进行判定
    url_r = url + '/robots.txt'
    res = getweb(url_r)
    if res != None:  # 如果robots文件存在，与robots进行匹配
        for robot in robots:
            if robot in res[2]:
                print('{}-->其CMS类型为:{}'.format(url, robot))
    # 如果不存在，那就根据网页内容和请求头信息判定
    res = getweb(url)
    if res != None:
        for k, v in head.items():
            if k in res[0]:
                print('{}其CMS类型为:{}'.format(url, v))
        for k, v in body.items():
            if k in res[2]:
                print('{}其CMS类型为:{}'.format(url, v))
        # 然后根据特定网址的内容判定
    for x in body_rule:
        cms_prefix = x.split('|', 3)[0]
        cms_name = x.split('|', 3)[1]
        cms_md5 = x.split('|', 3)[2]
        url_c = url + cms_prefix
        res = getweb(url_c)
        if res != None:
            if cms_md5 in res[2]:
                print('{}其CMS类型为:{}'.format(url, cms_name))

    # 最后根据MD5值判定
    for x in cms_rule:
        cms_prefix = x.split('|', 3)[0]
        cms_name = x.split('|', 3)[1]
        cms_md5 = x.split('|', 3)[2]
        url_s = url + cms_prefix
        res = getweb(url_s)
        if res != None:
            md5 = hashlib.md5()
            md5.update(res[1])
            rmd5 = md5.hexdigest()
            if cms_md5 == rmd5:
                print('{}其CMS类型为:{}'.format(url, cms_name))
            if res == None:
                print('{}暂时未搜索到其的cms地址'.format(url))


def mulit_cms(tempip):
    ipfile = tempip.readlines()
    for url in ipfile:
        url = url.split('\n')[0]  # 去掉ip后面自带的回车键
        thread_max.acquire()
        t = threading.Thread(target=cmsScan, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def begin():
    timestart=time.time()
    print("--------开始进行cms扫描,这可能会花费一些时间,请耐心等待----------")
    try:
        tempip = open('ip.txt', 'r')
        mulit_cms(tempip)
    except:
        print("请在源码文件目录下中的ip.txt目录中加入想要查找的ip地址")

    timeend=time.time()
    print("------------耗时{0:.5f}秒，主机发现功能正常------------".format(timeend - timestart))

_print = print
mutex = threading.Lock()
def print(text, *args, **kw):
    with mutex:
        _print(text, *args, **kw)


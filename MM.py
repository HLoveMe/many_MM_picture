# import representative
import urllib.request
import urllib.parse
import urllib.error
import os

DEFAULT_DIR = os.path.join(os.getcwd(),"imags")

# def _createProxy(isReload=None):
#     if isReload!=None:
#         representative.removeFile()
#     return representative.getIp()

def _openUrl(url):
    head = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"}
    req = urllib.request.Request(url,headers=head)
    # handle = urllib.request.ProxyHandler({"http":_createProxy(isRead)})
    # opener = urllib.request.build_opener(handle)
    # urllib.request.install_opener(opener)
    try:
        response = urllib.request.urlopen(req,timeout=10)
        return  response.read()
    except Exception as err:
        print("链接出错")

# 得到首页下的 子页面链接
def _getRealUrlList(html):
    result = html.split("\n")
    result = list(filter(lambda one: one.__contains__("<a target="), result))
    realtarget = []
    for i in result:
        begin = i.find("href")
        end = i.find("title")
        if end == -1:
            end = i.find(">", begin)
            i = i[begin + 6:end - 1]
        else:
            i = i[begin + 6:end - 2]
        realtarget.append(i)
    return realtarget

# 得到所有美女图片并保存
def saveImageToPath(path=None):
    if path == None:
        path = DEFAULT_DIR
    elif not os.path.isdir(path):
        path = DEFAULT_DIR
    if not os.path.exists(path):
        os.mkdir(path)
    html = _openUrl("http://www.2cto.com/meinv/").decode("GBK")
    pathList = _getRealUrlList(html)
    for i in pathList:
        name = i.rsplit("/")[-1].split(".")[0]
        if not os.path.exists(os.path.join(path,name)):
            _save(i,name)


def _save(url,dirName):
    path = os.path.join(DEFAULT_DIR,dirName)
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        html = _openUrl(url)
        try:
            html = html.decode("GBK")
        except Exception:
            html = html.decode("utf-8")
        result = html.split("\n")
        result = list(filter(lambda one: one.__contains__("点击图片进入下一页"), result))[0]
        begin = result.find("src=")
        end = result.find(">", begin)
        imgPath = result[begin + 5:end - 4]
        name = os.path.split(imgPath)[1]
        filePath = os.path.join(path, name)  # 文件路径
        if not os.path.exists(filePath):
            imgData = _openUrl(imgPath)
            with open(os.path.join(path, name), "wb") as file:
                file.write(imgData)
                file.flush()
                print(dirName, name)
        begin = result.find("<a href=", 10)
        end = result.find(">", begin);
        nextPage = result[begin + 9:end - 1]
        if "http" not in nextPage:
            nextUrl = os.path.join(os.path.split(url)[0], nextPage)
            _save(nextUrl, dirName)
    except Exception as err:
        print(html)
        print("解析出错")


saveImageToPath()

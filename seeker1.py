import requests
import bs4
import re
import traceback   #用来跟踪异常返回信息
def getHTML(url, code = "utf-8"):
    try:
        #kv = {'wd':'111'}   # param参数，html中以?wd=111形式加在url后面
        r = requests.get(url, timeout = 30)
     #   r = requests.get(url, timeout=30, headers={'cookie': coo})
        r.raise_for_status()
        r.encoding = code   #加快爬取速度
        return r
    except:
        return "爬取失败"
def fillList(ulist, url):   #用beautifulSoup爬取页面 非脚本页面
    html = getHTML(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    a = soup.find_all('a')
    for i in a:
        try:    #判断a标签属性是否为href
            href = i.attrs['href']
            ulist.append(re.findall(r"[s][hz]\d{6}", href)[0])
        except:
            continue
def getInfo(ulist, initURL, fpath):
    count = 0
    for stock in ulist:
        url = initURL + stock + ".html"
        html = getHTML(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = bs4.BeautifulSoup(html.text, "html.parser")
            stockInfo = soup.find("div",attrs = {'class':'stock-bets'})
            name = stockInfo.find_all(attrs = {'class':'bets-name'})[0]
            infoDict.update({'股票名称':name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            infoList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                info = infoList[i].text
                infoDict[key] = info
            with open(fpath,'a',encoding = 'utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(count*100/len(ulist)),end="")

        except:
            #如果根据代码搜索结果为404则跳到此处
          #  traceback.print_exc()
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(ulist)), end="")
            #\r默认将指针返回到最开始后输出（在原位置再次输出）
            continue


def main():
    uInfo = []
    stock_list_url = "http://quote.eastmoney.com/stock_list.html"
    stock_info_url = "https://gupiao.baidu.com/stock/"
    output_file = r"C:\Users\31230\PycharmProjects\Seeker\venv\BaiduStockInfo.txt"
    #在Python中\是转义符，\u表示其后是UNICODE编码，因此\User在这里会报错，在字符串前面加个r表示就可以了
    fillList(uInfo, stock_list_url)
    getInfo(uInfo,stock_info_url,output_file)
main()



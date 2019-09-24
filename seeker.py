import requests
import bs4
import re
def getHTML(url):

    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    coo = "cookie2=19588e78d2504eabb7affde8ff1be23c; v=0; _tb_token_=5e7be4e78e6e9; unb=1127368154; uc1=cookie14=UoTaHPk78xoCAA%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=Vq8l%2BKCLjA%2Bl&tag=10&cookie15=URm48syIIVrSKA%3D%3D&pas=0; csg=da1723d3; cookie17=UoCLEDGv1e3eSw%3D%3D; dnk=hyarcticfox; skt=e6682cd13de6e093; existShop=MTU2NDEzMDk4Ng%3D%3D; _l_g_=Ug%3D%3D; sg=x41; _nk_=hyarcticfox; cookie1=W8rr6rznKYsXd2RgKoki4ha9TL1uhW1IilPZq3kI%2BP0%3D; whl=-1%260%260%261564131146029; enc=uhnWUPGN2c2tOlhTyE%2B4YdzU6QAKbzN9eoBdWxgaYsr%2Bhvpv0KgIzTxy85s5jovCOO%2FHaElCs5tRhhA43KK9Xg%3D%3D; _cc_=WqG3DMC9EA%3D%3D; isg=BE9PltLITnySm0oA7wgmWxysx-NZdKOW-tlKwWFdlr7FMG8yaUS25k1pMqArU3sO; thw=cn; uc3=id2=UoCLEDGv1e3eSw%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=CzS39juFfk2XmKA%3D&vt3=F8dBy3za3x5sd28tprY%3D; t=d902880efe5b09bbaf9a3b50b195694e; miid=1131061798813509009; mt=ci=28_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; lgc=hyarcticfox; cna=7W/KEilrbgACAXL9drnDjrRh; tracknick=hyarcticfox; l=cBN7GGwVqIoB_qa_BOfa-urza77OBI9T4kPzaNbMiICPOgC658gGWZ3NNH8BCn1Vp6hyR37NjXrpBeYBq6U_YjKX2j-la; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; JSESSIONID=5D02755C223B55219E43BE2CFF72D024; alitrackid=www.taobao.com; lastalitrackid=login.taobao.com; swfstore=238861"
    try:
        #kv = {'wd':'111'}   # param参数，html中以?wd=111形式加在url后面
       # r = requests.get(url, timeout = 30)
        r = requests.get(url, timeout=30, headers={'User-Agent':UserAgent, 'cookie': coo})#浏览器伪装及利用cookies绕过反爬虫
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
        return "爬取失败"
def fillList(ulist, html):   #用beautifulSoup爬取页面 非脚本页面
    soup = bs4.BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:    #找到tbody中的子节点，但是其中会包含string节点
        if isinstance(tr,bs4.element.Tag):    #判断是否为标签
            tds = tr.find_all('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])
def parsePage(ulist, html):      #用re正则表达式爬去页面，用于脚本页面
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html.text)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html.text)   #*?为最小匹配
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ulist.append([price,title])
    except:
        print("")

def printList(ulist):
    tplt = "\t{0:^4}\t{1:>8}\t{2:{3}^16}"
    print(tplt.format("序号","价格", "商品名称",chr(12288)))
    count = 0
    for u in ulist:
        count = count + 1
        print(tplt.format(count,u[0],u[1],chr(12288)))
def main():
    uinfo = []
    goodsNum = 44
    goods = "书包"
    depth = 2
    starturl = "https://s.taobao.com/search?q=" + goods
    for i in range(depth):
        try:
            url = starturl + '&s=' +str(goodsNum * i)
            html = getHTML(url)
            parsePage(uinfo, html)
        except:
            continue
       # fillList(uinfo, html.text)

    printList(uinfo)
main()



import requests
from lxml import etree

# gold
#response = requests.get("https://rate.bot.com.tw/gold/chart/ltm/TWD")
#html = etree.HTML(response.content)
#print(etree.tostring(html, pretty_print=True))
#/html/body/div[1]/main/div[4]/table/tbody/tr
#/html/body/div[1]/main/div[3]/table/tbody/tr
#for item in html.xpath('/html/body/div[contains(@class, "page-wrapper")]/main/div[contains(@class, "container")]/table/tbody/tr'):
    # item[0][0].text->date
    # item[1].text->currency
    # item[2].text->unit
    # item[3].text->buy
    # item[4].text->sell
#    print(item[0][0].text, item[1].text, item[2].text, item[3].text, item[4].text)


# found
#response = requests.get("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=ALB04")
#html = etree.HTML(response.content)
#print(etree.tostring(html, pretty_print=True))

# date    
#for item in html.xpath('//td[contains(@class, "t3n0")]'):
#    print(item.text)

# value
#for item in html.xpath('//td[contains(@class, "t3n1")]'):
#    print(item.text)

#fund.bot
#response = requests.get("http://fund.bot.com.tw/w/wb/wb02a.djhtm?a=ALB04-0961")
#html = etree.HTML(response.content)
#print(etree.tostring(html, pretty_print=True))
#//*[@id="oMainTable"]/tbody/tr[5]/td[1]/table/tbody/tr[2]
#for item in html.xpath('//*[contains(@class, "wfb2c") or contains(@class, "wfb5c")]/parent::tr'):
    # every item have 4 column, less is not get correct item
    # item[0].text->date
    # item[1].text->price
    # item[2].text->up or down
    # item[3].text->up or down rate
#    if(len(item) == 4):
#        print(item[0].text, item[1].text)


# stock
#requests.DEFAULT_RETRIES = 5
#s = requests.session()
#s.keep_alive = False
#response = requests.get("https://www.cnyes.com/twstock/ps_historyprice.aspx?code=0050")
#html = etree.HTML(response.content)
#print(etree.tostring(html, pretty_print=True))

#print(html.xpath('//*[@id="main3"]/div[5]/div[3]/table/tbody/tr[2]'))

#response = requests.get("http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20180520&stockNo=0050")
#html = etree.HTML(response.content)
#print(etree.tostring(html, pretty_print=True))

#print(html.xpath('/html/body/div/table/tbody/tr'))
#for item in html.xpath('/html/body/div/table/tbody/tr'):
    #item[0].text->日期
    #item[1].text->成交股數
    #item[2].text->成交金額
    #item[3].text->開盤價
    #item[4].text->最高價
    #item[5].text->最低價
    #item[6].text->收盤價
    #item[7].text->漲跌價差
    #item[8].text->成交筆數
#    print(item[0].text, item[1].text, item[2].text, item[3].text, item[4].text, item[5].text, item[6].text, item[7].text, item[8].text)



# exchange
exchangeParam = {
    "datestart":"2018/05/01",
    "syear":"2018",
    "smonth":"05",
    "sday":"01",
    "dateend":"2018/07/20",
    "eyear":"2018",
    "emonth":"07",
    "eday":"20",
}
response = requests.post('http://www.taifex.com.tw/chinese/3/3_5.asp', exchangeParam)
html = etree.HTML(response.content)


#print(html.xpath('//*[@id="printhere"]/div[3]/table/tbody/tr/td'))
for item in html.xpath('//*[contains(@class, "table_c")]/tbody/tr'):
    # item[0].text->日期
    # item[1].text->美元／新台幣
    # item[3].text->美元／新台幣
    # item[5].text->英鎊／美元
    # item[6].text->澳幣／美元
    # item[10].text->紐幣／美元
    print(item[0].text, item[1].text, item[3].text, item[5].text, item[6].text, item[10].text)
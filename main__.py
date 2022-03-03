# 搜索爬虫。
# 1，输入关键字，返回列表;2，输入group和页码 返回列表
# 列表内容：1,时间，作者，title,内容，github链接
from search import search
from monitor import monitor

headers = {
    'authority': 'api.zsxq.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'x-version': '2.18.0',
    'x-signature': 'c302d5753dafe8a84aac2df2fb7c6944f5c36248',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'x-timestamp': '1646207273',
    'x-request-id': '2ce1058a0-05cd-0e9d-0b9d-c6f11cfce9d',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://wx.zsxq.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://wx.zsxq.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'zsxq_access_token=0DE35B07-A866-8401-8A25-94CBAF1FB4A0_D3EA69AE3F149971',
}

if __name__ == '__main__':
    print('[***]选择功能：1、搜索  2、监控七天最新\n')
    choose = int(input('输入数字即可：'))
    storage = input('输入存储文件名：')
    while True:
        if choose == 1:
            search(headers,storage)
            break
        elif choose == 2:
            monitor(headers,storage)
            break
        else:
            print('[***]输入错误，重新输入！！')
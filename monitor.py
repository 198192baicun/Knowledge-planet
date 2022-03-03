# 监控 kol爬虫
# 1，输入关键字，返回列表;2，输入group和页码 返回列表
# 列表内容：1,时间，作者，title,内容，github链接


import re
import time
import urllib.parse
import jsonpath
from loguru import logger
import requests
import pickledb

dict_groups = {}


def get_group(headers):
    response = requests.get('https://api.zsxq.com/v2/groups', headers=headers).json()
    groups = jsonpath.jsonpath(response, '$..groups')[0]
    for i in groups:
        group_id = i['group_id']
        name = i['name']
        dict_groups[name] = group_id
    if response['succeeded'] == False:
        return -1
    else:
        return list(dict_groups.keys())


def monitor_planet(planet,headers,storage):
    db = pickledb.load(f'{storage}.db', auto_dump=False)
    group_id = dict_groups[planet]
    params = (
        ('scope', 'all'),
        ('count', '20'),
    )
    response = requests.get(f'https://api.zsxq.com/v2/groups/{group_id}/topics', headers=headers, params=params).json()
    topics = response['resp_data']['topics']
    num = 1
    for topic in topics:
        date = str(topic['create_time']).split('.')[0].replace('T', ' ')
        timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timeArray))
        if int(time.time()) - timestamp < 3600 * 24 * 7:
            author = jsonpath.jsonpath(topic, '$..talk..owner..name')
            text = ' '.join(jsonpath.jsonpath(topic, '$..text')).replace('\n', '')
            img_url = jsonpath.jsonpath(topic, '$..images..url')

            # 复制链接
            topic_id = jsonpath.jsonpath(topic, '$..topic_id')[0]
            time.sleep(0.5)
            copy_Link_resp = requests.get(f'https://api.zsxq.com/v2/topics/{topic_id}/share_url',headers=headers).json()
            copy_Link = jsonpath.jsonpath(copy_Link_resp, '$..share_url')

            if 'type="web"' in text:

                em_ = re.findall('<e type="web".*', text)[0]
                hrefs = re.findall('href="(.*?)" title', em_)
                href = [urllib.parse.unquote(i) for i in hrefs]

                titles = re.findall('title="(.*?)" />', em_)
                title = [urllib.parse.unquote(i) for i in titles][0].replace('cache="', '')

                # 取出完整的content
                replace_em = re.findall('<e type="web".*?>', em_)
                content = text
                for i in range(len(replace_em)):
                    content = content.replace(replace_em[i], title[i] + ' ')
                if re.findall('<e.*/>', content):
                    em = re.findall('<e.*/>', text)[0]
                    content = text.replace(em, '')
                db_dict = {'创作日期': date, '作者': author, '标题': title, '内容': content, '跳转链接': href, '图片链接': img_url,
                           '复制链接': copy_Link}
                db.set(f'第{num}篇', db_dict)
                db.dump()
                logger.info(
                    f'\n第{num}篇---->\n创作日期：{date}\n作者：{author}\n标题：{title}\n内容：{content}\n跳转链接：{href}\n图片链接：{img_url}\n复制链接：{copy_Link}\n')
            else:
                if re.findall('<e.*/>', text):
                    em = re.findall('<e.*/>', text)[0]
                    text = text.replace(em, '')
                db_dict = {'创作日期': date, '作者': author, '内容': text, '图片链接': img_url, '复制链接': copy_Link}
                db.set(f'第{num}篇', db_dict)
                db.dump()
                logger.info(f'-----\n第{num}篇---->\n创作日期：{date}\n作者：{author}\n内容：{text}\n图片链接：{img_url}\n复制链接：{copy_Link}\n')

        num += 1

def monitor(headers,storage):
    groups = get_group(headers)
    if groups == -1:
        logger.error('可能网络抖动请重试；重试无效，可能cookie失效，请重新填入zsxq_access_token ----> ^_^!')
    else:
        print('现有的星球：\n', groups)
        planet = input('Enter the query：')
        monitor_planet(planet,headers,storage)
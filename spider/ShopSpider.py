import requests
import re
import csv
import os
import time
import json
import hashlib
import random
from lxml import etree
from utils.getCorrRel import CSSEncrypt
from utils.verify import Verify


class PublicCrawler(object):

    fieldnames = [
        'id',
        'tit',
        'star',
        'comments',
        'avg_price',
        'cate',
        'tag',
        'region',
        'address',
        'tasty_score',
        'env_score',
        'ser_score',
    ]

    # 初始化方法
    def __init__(self):
        if os.path.exists('font/css.json'):
            with open('font/css.json', 'r', encoding='utf-8') as f:
                self.data_dict = json.loads(f.read())
        else:
            self.data_dict = CSSEncrypt().get_corr_data()
        print(self.data_dict)
        if not os.path.exists('data.csv'):
            with open('data.csv', 'w', encoding='utf-8', newline='') as f:
                wf = csv.DictWriter(f, fieldnames=self.fieldnames)
                wf.writeheader()
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'navCtgScroll=0; showNav=#nav-tab|0|1; showNav=javascript:; navCtgScroll=111.11111450195312; _lxsdk_cuid=171e938a355c8-0e394b7c9537b8-c373667-144000-171e938a355c8; _lxsdk=171e938a355c8-0e394b7c9537b8-c373667-144000-171e938a355c8; _hc.v=c78c4015-91f6-18f8-b589-7920f2879520.1588755736; t_lxid=171e938a41ac8-0dfbe617032b58-c373667-144000-171e938a41ac8-tid; ua=%E9%9D%9E%E9%93%9C%E9%9D%9E%E9%93%81%E4%BA%A6%E9%9D%9E%E9%92%A2; ctu=d64e13e7bf3523b909058a0b837297aaa719a02be5ffa5d528c64ab9bf0c2e25; s_ViewType=10; cityid=17; switchcityflashtoast=1; m_flash2=1; seouser_ab=shop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; cy=76; cye=songyuan; default_ab=shop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5; _dp.ac.v=22bf8065-8cc2-4b77-9d0d-659c76e7b2c9; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597832856,1597833073,1597842503,1597893731; lgtoken=0f14b356a-69f0-4393-8c3c-979816032b64; thirdtoken=6691167f-0bb9-4ef8-92da-acd9e4462171; dper=9409171fef76c6f505138b7a5d265b4c6e6ea34ef1e7287926588be3d064922d850c3f5bcd36372329c85965cac8663af67395193e58254ae7079e25074201bb156cbab312010799171c69a4c97bc3f744752c5b62f5a79a26186b8f6ec1dd3b; ll=7fd06e815b796be3df069dec7836c3df; ctu=f0e755da4b57aab5565174c4a0505c9f0f68525f19eaa98fc479d7579cdd5d1d8d54ee0c161452f038946a1512cc8fb3; dplet=bc5222165d2866516ee23805ccde757a; _lxsdk_s=1740a14a131-4d6-c36-3d4%7C%7C231; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1597899939',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        }

    # 解析列表页数据
    def get_home_page_html(self, url):
        print(url)
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding
        if resp.status_code == 200:
            # print(resp.text)
            content = resp.text
            for k, v in self.data_dict['number'].items():
                content = re.sub('<svgmtsi class="shopNum">{}</svgmtsi>'.format(k),
                                 '<svgmtsi class="shopNum">{}</svgmtsi>'.format(v), content)
            for k, v in self.data_dict['tagName'].items():
                content = re.sub('<svgmtsi class="tagName">{}</svgmtsi>'.format(k),
                                 '<svgmtsi class="tagName">{}</svgmtsi>'.format(v), content)
            for k, v in self.data_dict['address'].items():
                content = re.sub('<svgmtsi class="address">{}</svgmtsi>'.format(k),
                                 '<svgmtsi class="address">{}</svgmtsi>'.format(v), content)
            return content
        else:
            print('状态码错误：', resp.status_code)
            with open('flag/flag.txt', 'w', encoding='utf-8') as f:
                f.write(url)

    # 解析详情页数据
    def parse(self, content, cate):
        doc = etree.HTML(content)
        lis = doc.xpath('//div[@id="shop-all-list"]/ul/li')
        print(lis)
        for li in lis:
            sid = self.get_md5(li.xpath('div[@class="txt"]/div/a/@href')[0])
            tit = li.xpath('div[@class="txt"]/div/a/h4/text()')[0]
            star = self.get_first(li.xpath('div[@class="txt"]//div[@class="nebula_star"]/div[2]/text()'))
            comments = li.xpath('string(div/div[@class="comment"]/a[1]/b)')
            avg_price = li.xpath('string(div/div[@class="comment"]/a[2]/b)')
            tag = li.xpath('string(div/div[@class="tag-addr"]/a[1]/span)')
            region = li.xpath('string(div/div[@class="tag-addr"]/a[2]/span)')
            address = li.xpath('string(div/div[@class="tag-addr"]/span)')
            tasty_score = li.xpath('string(div/span[@class="comment-list"]/span[1]/b)')
            env_score = li.xpath('string(div/span[@class="comment-list"]/span[2]/b)')
            ser_score = li.xpath('string(div/span[@class="comment-list"]/span[3]/b)')
            data = {
                'id': sid,
                'tit': tit,
                'star': star,
                'comments': comments,
                'avg_price': avg_price,
                'cate': cate,
                'tag': tag,
                'region': region,
                'address': address,
                'tasty_score': tasty_score,
                'env_score': env_score,
                'ser_score': ser_score,
            }
            print(data)
            self.save(data)
        next_url = doc.xpath('//a[@title="下一页"]/@href')
        return next_url[0] if next_url else None

    @staticmethod
    def get_first(lst):
        return lst[0] if lst else ''

    @staticmethod
    def get_md5(string):
        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        return m.hexdigest()

    def get_food_type(self, url):
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding
        doc = etree.HTML(resp.text)
        urls = doc.xpath('//div[@id="classfy"]/a/@href')
        texts = doc.xpath('//div[@id="classfy"]/a/span/text()')
        print(urls, texts)
        return urls, texts

    def save(self, data):
        with open('data.csv', 'a', encoding='utf-8', newline='') as f:
            wf = csv.DictWriter(f, fieldnames=self.fieldnames)
            wf.writerow(data)

    def work(self, url):
        region_code = [
            # 'r4791'
            # 'r4793',
            # 'r4795',
            # 'r4792',
            # 'c4438',
            # 'c4439',
            'c1492'
        ]
        urls, texts = self.get_food_type(url)
        num = 0
        if os.path.exists('flag/flag.txt'):
            with open('flag/flag.txt', 'r', encoding='utf-8') as f:
                url1 = f.read()
            for index, url in enumerate(urls):
                if url in url1:
                    num = index
                    break
        print(num)
        for region in region_code:
            for href, cate in zip(urls[num:], texts[num:]):
                tmp = href
                href += region
                while True:
                    content = self.get_home_page_html(href)
                    href = self.parse(content, cate)
                    if not href:
                        href = tmp
                        break
                    time.sleep(2)


import requests
import re
import json
import os
import time
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont
# from utils.verify import Verify
FONT_SOUR = (' x1234567890店'
             '中美家馆小车大市公酒行国品'
             '发电金心业商司超生装园场食'
             '有新限天面工服海华水房饰城'
             '乐汽香部利子老艺花专东肉菜'
             '学福饭人百餐茶务通味所山区'
             '门药银农龙停尚安广鑫一容动'
             '南具源兴鲜记时机烤'
             '文康信果阳理锅宝达地儿衣特'
             '产西批坊州牛佳化五米修爱北'
             '养卖建材三会鸡室红站德王光'
             '名丽油院堂烧江社合星货型村'
             '自科快便日民营和活童明器烟'
             '育宾精屋经居庄石顺林尔县手'
             '厅销用好客火雅盛体旅之鞋辣'
             '作粉包楼校鱼平彩上'
             '吧保永万物教吃设医正造丰健'
             '点汤网庆技斯洗料配汇木缘加'
             '麻联卫川泰色世方寓风幼羊烫'
             '来高厂兰阿贝皮全女拉成云维'
             '贸道术运都口博河瑞宏京际路'
             '祥青镇厨培力惠连马鸿钢训影'
             '甲助窗布富牌头四多妆吉苑沙'
             '恒隆春干饼氏里二管'
             '诚制售嘉长轩杂副清计黄讯太'
             '鸭号街交与叉附近层旁对巷栋'
             '环省桥湖段乡厦府铺内侧元购'
             '前幢滨处向座下県凤港开关景'
             '泉塘放昌线湾政步宁解白田町'
             '溪十八古双胜本单同九迎第台'
             '玉锦底后七斜期武岭松角纪朝'
             '峰六振珠局岗洲横边'
             '济井办汉代临弄团外塔杨铁浦'
             '字年岛陵原梅进荣友虹央桂沿'
             '事津凯莲丁秀柳集紫旗张谷的'
             '是不了很还个也这我就在以可'
             '到错没去过感次要比觉看得说'
             '常真们但最喜哈么别位能较境'
             '非为欢然他挺看价那意种想出'
             '员两推做排实分间甜'
             '度起满给热完格荐喝等其再几'
             '只现朋候样直而买于般豆量选'
             '奶打每评少算又因情找些份置'
             '适什蛋师气你姐棒试总定啊足'
             '级整带虾如态且尝主话强当更'
             '板知己无酸让入啦式笑赞片酱'
             '差像提队走嫩才刚午接重串回'
             '晚微周值费性桌拍跟'
             '块调糕点'
             )


# 转化映射关系
class CSSEncrypt(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'showNav=#nav-tab|0|1; navCtgScroll=139.1999969482422; navCtgScroll=200; _lxsdk_cuid=171e938a355c8-0e394b7c9537b8-c373667-144000-171e938a355c8; _lxsdk=171e938a355c8-0e394b7c9537b8-c373667-144000-171e938a355c8; _hc.v=c78c4015-91f6-18f8-b589-7920f2879520.1588755736; t_lxid=171e938a41ac8-0dfbe617032b58-c373667-144000-171e938a41ac8-tid; ua=%E9%9D%9E%E9%93%9C%E9%9D%9E%E9%93%81%E4%BA%A6%E9%9D%9E%E9%92%A2; ctu=d64e13e7bf3523b909058a0b837297aaa719a02be5ffa5d528c64ab9bf0c2e25; s_ViewType=10; fspop=test; cityid=17; switchcityflashtoast=1; m_flash2=1; seouser_ab=shop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; cy=76; cye=songyuan; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597831304,1597832075,1597832856,1597833073; pvhistory="6L+U5ZuePjo8L3N1Z2dlc3QvZ2V0SnNvbkRhdGE/Y2FsbGJhY2s9anNvbnBfMTU5NzgzNDAzMTQ4MV83MDU1MD46PDE1OTc4MzQwMzE3MjddX1s="; default_ab=shop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5; _lxsdk_s=174062ad111-a0-846-2ee%7C%7C2690; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1597836114',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        }
        self.detail_css_link = self.get_css_url('http://www.dianping.com/songyuan/ch10/g110r3688')
        print(self.detail_css_link)
        if not os.path.exists('font'):
            os.mkdir('font')

    def get_css_url(self, url):
        print(f'Get css file links from {url}')
        resp = self.session.get(url).content.decode('utf-8')
        print(resp)
        try:
            css_link = re.search('<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/\w+.css)">', resp).group(1)
        except AttributeError as e:
            print(e.args)
            time.sleep(5)
            self.get_css_url(url)
        else:
            return 'https:' + css_link

    def get_css_links(self):
        resp = self.session.get(
            self.detail_css_link,
        ).content.decode('utf-8')
        with open('font/detail-css.css', 'w', encoding='utf-8') as f:
            f.write(resp)
        css_links = {
            'number': 'https:' + re.findall(
                '"PingFangSC-Regular-shopNum";src:url.*?;src:url.*?format.*?,url\("(.*?)"\);} .shopNum{',
                resp)[0],
            'address': 'https:' + re.findall(
                '"PingFangSC-Regular-address";src:url.*?;src:url.*?format.*?,url\("(.*?)"\);} .address{',
                resp)[0],
            'tagName': 'https:' + re.findall(
                '"PingFangSC-Regular-tagName";src:url.*?;src:url.*?format.*?,url\("(.*?)"\);} .tagName{',
                resp)[0],
        }
        print(css_links)
        return css_links

    def download_font_file(self, css_link):
        file_name = 'font/' + css_link[0] + '.woff'
        url = css_link[1]
        print('Download font files from {}'.format(url))
        resp = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(resp.content)
        return css_link[0]

    @staticmethod
    def handler_data(css_link):
        file_name = 'font/' + css_link + '.woff'
        print(f'Parsing {file_name} to xml format...')
        data = {}
        xml_file = file_name.rsplit('.', 1)[0] + '.xml'
        font = TTFont(file_name)
        font.saveXML(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for index, gid in enumerate(root.iter('GlyphID')):
            data[gid.attrib['name'].replace('uni', '&#x') + ';'] = FONT_SOUR[index]
        return {
            css_link: data
        }

    def get_corr_data(self):
        corr_dict = {}
        css_links = self.get_css_links()
        for css_link in css_links.items():
            file_name = self.download_font_file(css_link)
            data = self.handler_data(file_name)
            corr_dict.update(data)
        with open('font/css.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(corr_dict, ensure_ascii=False, indent=4))
        return corr_dict


if __name__ == '__main__':
    spider = CSSEncrypt()
    data_dict = spider.get_corr_data()
    print('CSS字典', data_dict)
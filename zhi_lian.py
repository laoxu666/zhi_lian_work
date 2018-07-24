import time
import json
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup


class ZhiLianZhaoPin(object):
    '''class'''

    def __init__(self, city, kw, start_page, end_page):
        # 保存到成员属性
        self.city = city
        self.kw = kw
        self.start_page = start_page
        self.end_page = end_page
        self.url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'
        # 声明一个空列表，保存字典信息
        self.items = []

    def parse_content(self, page, content):
        '''一级解析函数'''
        # 创建soup对象
        soup = BeautifulSoup(content, 'lxml')
        table_list = soup.find_all('table', class_="newlist")[1:]
        # print (table_list[0])
        for table_content in table_list:
            # 获取信息
            href_list = table_content.select(" tr > td > div > a")
            # print(href_list)
            href = href_list[0]['href']
            print(href)
            # # 反馈率
            # fklv = str(table_content.select('.new_list > tr > .fk_lv')[0].text) + "反馈率"
            # print(fklv)
            # 第二级查找
            self.parse_content2(page, href)

    def parse_content2(self, page, href):
        '''二级解析函数'''
        # 创建请求对象
        request = self.handle_request(page, href)
        # 获取内容
        content = urllib.request.urlopen(request).read().decode('utf8')
        # 解析
        # pattern = re.compile(r'')
        soup = BeautifulSoup(content, 'lxml')
        # 职位名称
        job_name = soup.h1.text
        # print(job_name)
        # 公司名称
        company_name = soup.h2.text
        # print(company_name)
        # 福利待遇
        fldy = soup.find('div', class_="welfare-tab-box").text
        # print(fldy)
        # 招聘信息
        information = soup.select('.terminalpage-left > ul')[0].text.replace('\n',' ')
        # print(information)
        # 任职要求 工作地址
        job_requirements = soup.select('.tab-inner-cont')[0].text.replace('\n', ' ')
        # print(job_requirements)

        # 保存为字典格式
        item = {
            '职位名称': job_name,
            '公司名称': company_name,
            '福利待遇': fldy,
            '招聘信息': [information],
            '任职要求与工作地点': job_requirements
        }
        # 添加进列表
        self.items.append(item)
        time.sleep(1)

    def run(self):
        '''运行函数'''
        for page in range(self.start_page, self.end_page + 1):
            request = self.handle_request(page)
            content = urllib.request.urlopen(request).read().decode('utf8')
            print('开始保存第%s页。。。' % page)
            # 解析函数
            self.parse_content(page, content)
            string = json.dumps(self.items, ensure_ascii=False)
            json_path = self.kw + '.json'
            with open(json_path, 'w', encoding='utf8') as fp:
                fp.write(string)
            print('第%s页保存完毕' % page)

    def handle_request(self, page=0, href=None):
        '''请求函数'''
        data = {
            'jl': self.city,
            'kw': self.kw,
            'p': page,
        }
        # 处理data，拼接url
        data = urllib.parse.urlencode(data)
        url = self.url + data
        print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        }

        if href:
            return urllib.request.Request(url=href, headers=headers)
        else:
            return urllib.request.Request(url, headers=headers)


def main():
    '''主函数'''
    # 提示用户输入城市名称
    city = input('请输入要爬取的城市名称:')
    # 提示用户输入岗位关键字
    kw = input('请输入要爬取的岗位名称:')
    # 提示用户输入爬取的页码
    start_page = int(input('请输入起始页码:'))
    end_page = int(input('请输入结束页码:'))

    zhilian = ZhiLianZhaoPin(city, kw, start_page, end_page)
    zhilian.run()


if __name__ == '__main__':
    main()
import urllib.request
import re

class Qiubai():
    """爬取糗事百科内容"""
    
    def __init__(self):
        """初始化相关数据"""
        #初始url地址
        self.__init_url = "http://www.qiushibaike.com"
        self.__full_url = self.__init_url #记录下一次需要爬取得url，开始为初始地址
        self.__page_number = 1 #用来记录这是第几条数据
        self.__content_count = 20 #记录每页显示的糗事数
        self.__html = None #保存提取到的html内容
        self.__contents = [] #保存爬取到的页面糗事
        
        #设置http头,用来伪装python程序，让糗百服务器以为我们是浏览器人为行为
        #否则糗百检测到是程序自动访问会拒绝请求，防止过多请求
        self.__send_headers = {}
        self.__send_headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"


    def __str__(self):
        return str(self.__contents)

    
    def __get_html(self):
        """爬取指定html页面的内容"""
        self.__contents.clear()#每次开始爬取前，清空上一次的内容
        req = urllib.request.Request(self.__full_url,headers = self.__send_headers)
        self.__html = urllib.request.urlopen(req).read().decode("utf-8")
        self.__page_number += 1 #每调用一次这个函数，就说明又爬取了一页


    def __extract_content(self):
        """提取我们需要的糗事内容"""
        #u'[\u0010-\uffe5]*表示所有的unicode编码的字符，因为有两个换行，所以
        #用..来匹配
        data = re.findall('"content">..[\u0010-\uffe5]*',self.__html,re.DOTALL)
        self.__content_count = len(data)
        for content in data:
            self.__contents.append(re.findall("\n\n.*",content)[0])


    def __find_next_Page(self):
        """找出下一页的地址，更新full_url"""
        data = re.findall('/8hr/page/\d+.*下一页',self.__html,re.DOTALL)
        data = re.findall('/8hr/page/\d.s=\d+',str(data))
        self.__full_url = self.__init_url + data[-1]        


    def get_contents(self):
        """获取爬取到的内容列表"""
        self.__get_html()
        self.__extract_content()
        self.__find_next_Page()
        return self.__contents


    def get_page_number(self):
        """获取当前爬取的是第几个页面"""
        return self.__page_number


    def get_content_count(self):
        """获取当前爬取的页面有多少条糗事内容"""
        return self.__content_count

        
if __name__ == "__main__":
    qiubai = Qiubai()
    while True:
        print("第%d页 本页共%d条糗事" % (qiubai.get_page_number(),qiubai.get_content_count()))
        contents = qiubai.get_contents()
        for content in contents:
            print(content)
        flag = input("\nDo you want to continue(y/n):")
        print("\n\n\n\n")
        if flag == "n" or flag == "N":
            break
        else:
            continue    



        

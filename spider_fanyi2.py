# encoding: utf-8
"""
@author:王耗
@file: spider_fanyi2.py
@time：2018/6/16 19:06
"""
from retrying import retry
import requests
import json
class BaiDu_spider():
    def __init__(self,search1):
        self.search1 = search1
        self.language_url = "http://fanyi.baidu.com/langdetect"
        self.result_url = "http://fanyi.baidu.com/basetrans"
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
    @retry(stop_max_attempt_number=3)
    def parse_language_url(self):
        re = requests.post(self.language_url,data={"query":self.search1},headers=self.headers,timeout=10,verify=False)
        return json.loads(re.content.decode())

    @retry(stop_max_attempt_number=3)
    def parse_result_url(self,language):
        data = {"query":self.search1,"from":"zh","to":"en"} if language=="zh" else {"query":self.search1,"from":"en","to":"zh"}
        result = requests.post(self.result_url,data=data,headers=self.headers,timeout=10,verify=False)
        return json.loads(result.content.decode())
    def run(self):
        language = self.parse_language_url()["lan"]
        result = self.parse_result_url(language)
        print("result is:",result["trans"][0]["dst"])

if __name__ == "__main__":
    search1 = input("请输入:")
    my_spider = BaiDu_spider(search1)
    my_spider.run()
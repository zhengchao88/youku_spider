# -*- coding: utf-8 -*-  
   
import urllib2  
import urllib  
import re  
import time  
import random

  
#----------- 加载处理优酷视频 -----------  
class Youku_Spider:  
      
    def __init__(self,style):  
        self.total_page = 1   
        self.style = style

    def GetTypeUrl(self):
        url_list = {"电视剧":"http://www.youku.com/v_olist/c_97.html",
                    "电影":"http://www.youku.com/v_olist/c_96.html",
                    "综艺":"http://www.youku.com/v_olist/c_85.html",
                    "音乐":"http://www.youku.com/v_olist/c_95.html",
                    "动漫":"http://www.youku.com/v_olist/c_100.html",
                    "全部":"http://www.youku.com/v_showlist/c0.html"}
        
        return url_list[self.style]
        

    def GetTotalPage(self,website):
        website = re.sub('\t|\n','',website)
        page_part = re.findall('<.*?"yk-pages">(.*?)</ul>',website)[0]
        self.total_page = int(re.findall('<li.*?><.*?>(.*?)</.*?></li>',page_part)[-2])
        print '共%s页：' % self.total_page

  
    # 将所有视频名称添加到列表中并且返回列表  
    def GetVideo(self,url,page):  
        NewUrl = re.findall('(.*?).html',url)[0]+"_p_"+str(page)+".html"
        print '正在加载第%d页...%s' % (page,NewUrl) 
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        req = urllib2.Request(NewUrl, headers = headers) 
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()  
  
        # 找出所有class="p-meta-title"的div标记  
        pattern_list = {"电视剧":'<div.*?class="p-meta-title".*?title="(.*?)">.*?</div>',
                    "电影":'<div.*?class="p-meta-title".*?title="(.*?)">.*?</div>',
                    "综艺":'<div.*?class="p-meta-title".*?title="(.*?)">.*?</div>',
                    "音乐":'<div.*?class="v-meta-title".*?title="(.*?)">.*?</div>',
                    "动漫":'<div.*?class="p-meta-title".*?title="(.*?)">.*?</div>',
                    "全部":'<div.*?class="v-meta-title".*?title="(.*?)">.*?</div>'}
        myItems = re.findall(pattern_list[self.style],myPage,re.S)
        items = []
        for i in myItems:
            items.append(i+"\n")
        return items  
   
          
    def Start(self):  

        #获取对应的url
        url = self.GetTypeUrl()  
  
        print '正在加载%s中请稍候......' % url

        #获取总页数
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        req = urllib2.Request(url, headers = headers) 
        website = urllib2.urlopen(req)
        index = website.read()  
        self.GetTotalPage(index)

        #逐页获取视频信息
        file_name = self.style+".txt"
        f=open(file_name,'a')
        for i in range(1,self.total_page+1):
            videos = self.GetVideo(url,i)
            f.writelines(videos)
            time.sleep(random.randint(1,5))
        f.close()
        print '已经抓完喽...'
        
  
  
#----------- 程序的入口处 -----------  
print """ 
--------------------------------------- 
   程序：优酷爬虫 
   作者：chao zheng
   日期：2015-04-17
   操作：输入“电视剧”"电影"“综艺”“音乐”“动漫”或“全部” 
   功能：按下回车将对应类型的视频名存储到txt文件中，按下quit退出
--------------------------------------- 
"""
  
while 1:  
    print '请输入您想要抓取的视频类型：(“电视剧”"电影"“综艺”“音乐”“动漫”或“全部”)'  
    style = raw_input(' ')  
    while style not in ["电视剧","电影","综艺","音乐","动漫","全部","quit"]:
        print '您输入的类型错误，请重新输入：'
        style = raw_input(' ')
    if style == "quit":
        exit()    
    myModel = Youku_Spider(style)  
    myModel.Start()

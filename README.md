# Mzitu
操作系统：Ubuntu 16.04
<br>
IDE： pycharm
<br>
抓取www.meizu.com/all的所有图片。
<br>
看到网上有个项目是抓取妹子图网站的图片，而且网站结构很简单。站长很大方的做了一个/all页面，这简直就是爬虫们的福音啊！！！
<br>
采用简单的requests + lxml 进行爬虫，简单的爬去了/all页面的图片。
<br>
最开始不知道网站有防盗链接，后来把referer加上去了才能正常的下载图片。
<br>
<hr> 差不多完善之后，开始爬取，结果出现了访问次数过多的错误，但是没有被封IP，所以加上了time模块的sleep，最后也算是可以进行爬去了。</hr>
<br>
加上了带了IP，就不用等待了，而且很稳定。
<br>
代理IP池借鉴了Germe的ProxyPool项目。
ProxyPool地址 https://github.com/Germey/ProxyPool

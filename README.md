原本这个项目只是一个http服务器<br>
当我实现CGI功能之后发现了新天地<br>
于是乎通过CGI+Python,可以实现一个在线的漏洞扫描平台<br>
因为好奇，所以努力....加油!<br>

<h1>服务器</h1>
单线程的epoll处理http请求完毕<br>
多线程的epoll处理http请求时发现一个非常奇怪的问题:两个不同的线程处理了一个sock.<br>
百思不得其解.......Why???<br>

<h1>Python漏洞扫描</h1>
2017-07-27 CDN检测模块完成!
2017-07-28 端口扫描模块完成!
2017-07-30 动态页面抓取爬虫完成!
2017-08-03 sql注入漏洞检测模块完成!
2017-08-11 cms指纹检测模块完成!
2017-08-12 webshell爆破模块完成!
2017-08-13 XSS跨站脚本漏洞扫描模块完成!
2017-08-16 网站备份检测模块完成!
等待整合...

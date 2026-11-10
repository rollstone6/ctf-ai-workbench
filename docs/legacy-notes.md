# 历史学习笔记

以下保留原 README 的学习资料，属于历史归档；SQL 注入不在本次架构方案的题型范围。

# CTF_WP
cosulting in the ctf


敏感目录、敏感备份文件、Banner 识别
https://github.com/denny0223/scrabble——获取网站源码或者工具


?id=0' union select 1,2,group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='notes'--+

thinkPHP的时候，可以结合banner信息解决
https://blog.csdn.net/weixin_48135624/article/details/122700556——dedecms网站系统介绍

数字型注入和Union注入

字符注入和布尔注入

时间盲注：sqlmap -u "http://example.com/page.php?id=1" \
  --technique=T \
  --time-sec=2 \
  --level=3 \
  --risk=2 \
  --batch

报错注入

逃逸引号（编码解码、PHP可控点、二次注入、字符串截断


二、文件漏洞
web语言（Node、Ruby、java、python、php）
--------------------------------------------------
2025第三界 ‘陇剑杯’ 初赛


https://zh.wikipedia.org/wiki/%E6%B1%89%E6%98%8E%E8%B7%9D%E7%A6%BB——汉明距离定义
汉明重量是字符串相对于同样长度的零字符串的汉明距离


------------------------------------------------
pwn.college

1、sh 和 .\ 执行上内核区分的权限

由于安全考虑，内核默认会忽略脚本文件（如 Bash、Python 脚本）的 setuid 位。这是一个重要的安全特性，因为脚本比二进制文件更容易被篡改和注入恶意代码。

2、chmod 644 修改文件变普通用户可读

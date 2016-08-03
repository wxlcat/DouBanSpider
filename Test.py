
import requests

cookies = {
'bid':'tDtl1xwpa_o',
'_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1470197991%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D4em9oT6QEwWzZvCuwv_1Ujh9I8gj8AsUNeXqo_YOGFkR_IpetG_GDmXqRA9CAHzMByUEFe7RnzJYcO2zWXxgh_%26wd%3D%26eqid%3D973b3c38001e403e0000000657a17085%22%5D',
'__utmt':'1', 
'_pk_id.100001.8cb4':'88391a451737bd5c.1468899588.13.1470198152.1470194414.',
'_pk_ses.100001.8cb4':'*', 
'__utma':'30149280.632302979.1468899589.1470194201.1470197991.13',
'__utmb':'30149280.16.5.1470198152273',
'__utmc':'30149280',
'__utmz':'30149280.1470197991.13.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
}

cookies2={'name':'wxl'}

ret = requests.get('https://www.douban.com/group/GuangZhoulove/discussion?start=0', cookies=cookies2)
print ret.text

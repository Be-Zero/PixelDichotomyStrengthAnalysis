from data_downloader import downloader
from xml.dom.minidom import parse

netrc = downloader.Netrc()
netrc.add('scihub.copernicus.eu', 'bezero', 'MKB123456', overwrite=True)

# 文件输出目录，需确保此文件夹存在
folder_out = './data/yearsDatas'
# 第一步下载的包含url的 products.meta4 文件
url_file = './products.meta4'

data = parse(url_file).documentElement
urls = [i.childNodes[0].nodeValue for i in data.getElementsByTagName('url')]

downloader.download_datas(urls, folder_out)

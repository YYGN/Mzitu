from mzitu import *
from multiprocessing import Pool

def run():
    print('正在向网站发起请求......')
    html = get_html()
    if html:
        gallery = parse_html(html)
        pool = Pool(4)
        pool.map(parse_detail, gallery)
        pool.close()
        pool.join()

if __name__ == '__main__':
    run()

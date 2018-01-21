from mzitu import *
from multiprocessing import Pool
import time

def run():
    print('正在向网站发起请求......')
    gallery = parse_html(get_html())
    pool = Pool(4)
    pool.map(parse_detail, gallery)
    pool.close()
    time.sleep(3)
    pool.join()

if __name__ == '__main__':
    run()
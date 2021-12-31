import os, sys
from multiprocessing import Pool
from typing import List, Any
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.append(BASE_DIR)

from collection.scraper import *
from base.conn import *
from base.dbhelper import *
from base.argument import args

data_date = str(args.data_date)

def create_dbhelper():
    conn = create_connect("database")
    helper = DBHelper(conn)
    return helper

def get_total_pages():
    # @TODO
    return range(1,30)

def scrape(page: int) -> List[Any]:
    return Scraper(page).scrape_info()

if __name__ == '__main__':
    start_time = time.time()

    pages = get_total_pages()
    # pool = ThreadPool(5)
    # results = pool.map(scrape, pages)
    with Pool() as pool:
        results = pool.map(scrape, pages)

    # pool.close()
    # pool.join()

    duration = time.time() - start_time
    print(f"Finish in {duration} seconds")

    conn = create_dbhelper()
    books = []
    for l in results:
        books.extend(l)

    try:
        conn.executemany(
            f"""REPLACE INTO book_info (ds,book_id,book_name,book_author,book_intro,book_length,
                        book_view_num,book_comment_num,book_fav_num,book_tags,create_time,update_time)
                        VALUES ('{data_date}', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            books
        )
    except Exception as e:
        print(e)
        print('data load failed')
        conn.close()
        sys.exit(1)

    conn.close()

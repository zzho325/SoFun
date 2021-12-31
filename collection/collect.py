import os, sys
from concurrent import futures
import threading
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
    return range(1,3000)

def scrape_page(page):
    return Scraper(page).scrape_info()

def scrape_range(conn, pages):
    books = []
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(scrape_page, pages)
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
    print(f"Save pages {list(pages)[0]} to {list(pages)[1]} successfully.")

if __name__ == '__main__':

    start_time = time.time()
    ranges = [range(1, 500), range(500, 1000), range(1000, 1500), range(1500, 2000),
    range(2000, 2500), range(2500, 3000)]

    duration = time.time() - start_time

    conn = create_dbhelper()
    for r in ranges:
        scrape_range(conn, r)
    conn.close()
    print(f"Finish in {duration} seconds")

import datetime
import time

import pika
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

DELAY_SECS = 10
SERVER_NEWS = "https://rozetked.me/news"

RABBIT_HOST = 'localhost'
RABBIT_QUEUE = 'newstr'

AUTHOR_TAG = './div/div/span/a'
ELEMENTS_TAG = '//div[@class="r_content"]//div[@class="post_new"]'
TITLE_TAG = './div/a'
VIEWS_TAG = './div[@class=post_new-meta]/div[@class=post_new-meta-views]/span'


def get_data() -> None:
    """
    Get articles from SERVER_NEWS and put them into Rebbit MQ.

    Returns: None

    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(SERVER_NEWS)
    assert "No results found." not in driver.page_source

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE)

    last_news = None
    while True:
        elem_table = driver.find_elements_by_xpath(ELEMENTS_TAG)
        article_count = 1
        first_article = None
        print(f'last_news={last_news}')
        for i in elem_table:
            elem_table_title = i.find_element_by_xpath(TITLE_TAG)
            elem_table_author = i.find_element_by_xpath(AUTHOR_TAG)
            elem_table_href = i.find_element_by_link_text(f"{elem_table_title.text}").get_attribute("href")
            elem_table_date = datetime.datetime.now().strftime("%x")
            if article_count == 1 and not last_news:
                last_news = elem_table_title.text
            elif last_news == elem_table_title.text:
                break
            if article_count == 1:
                first_article = elem_table_title.text
            channel.basic_publish(exchange='',
                                  routing_key=RABBIT_QUEUE,
                                  body='|'.join([str(article_count), elem_table_title.text, elem_table_author.text,
                                                 elem_table_href, elem_table_date]))
            print(f'\t{article_count} {elem_table_title.text}')
            print(f'\tlast_news={last_news}')
            print(f'\tfirst_article={first_article}')
            print(f'\t{elem_table_author.text}')
            print(f'\t{elem_table_href}')
            print(f'\t{elem_table_date}')
            article_count += 1
        print(f'first_article={first_article}')
        if first_article:
            last_news = first_article
        time.sleep(DELAY_SECS)
    driver.close()
    driver.quit()
    connection.close()


if __name__ == "__main__":
    get_data()

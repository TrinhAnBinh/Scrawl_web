import requests
import argparse
import html
import sys

PAGE_SIZE = 100


def fetch(url, params):
    '''
    Lấy question từ `url` với `params`, trả về tiêu đề `question` và `question_id` # NOQA
    :param url: link API
    :param params: dict param để truy vấn API
    :rtype: Generator
    '''
    try:
        session = requests.Session()
        response = session.get(url, params=params)
        for item in response.json().get('items'):
            yield html.unescape(item.get('title')), item.get('question_id')
    except Exception:
        print("Request limited! We can make only 300 requests per day :(")
        sys.exit()


def questions(num_of_questions, tag):
    '''
    Trả về generator của tất cả các question đã fetch được
    :param `num_of_questions`: số lượng question cần lấy
    :param `tag`: tag của question
    :rtype: Generator
    '''
    url = 'https://api.stackexchange.com/2.2/questions'
    params = {'page': 0,
              'pagesize': PAGE_SIZE,
              'order': 'desc',
              'sort': 'votes',
              'tagged': tag,
              'site': 'stackoverflow'
              }
    # Chia lượng question cần lấy thành nhiều trang
    # num_of_questions = num_of_pages * PAGE_SIZE + remainder_of_page
    num_of_pages = num_of_questions // PAGE_SIZE + 1
    remainder_of_page = num_of_questions % PAGE_SIZE
    # Lấy các trang có pagesize là 100
    for page in range(1, num_of_pages):
        params.update(page=page)
        for question in fetch(url, params):
            yield question
    # Lấy nốt phần trang còn lại
    params.update(page=num_of_pages)
    params.update(pagesize=remainder_of_page)
    for question in fetch(url, params):
        yield question


def top1_answer(question):
    '''
    Trả về link của answer có vote cao nhất trong question đầu vào
    :param question: tuple chứa title và question id
    :rtype: str
    '''
    _, question_id = question
    url = f'https://api.stackexchange.com/2.2/questions/{question_id}/answers'
    params = {'page': 1,
              'pagesize': 1,
              'order': 'desc',
              'sort': 'votes',
              'site': 'stackoverflow'
              }
    try:
        session = requests.Session()
        response = session.get(url, params=params)
        answer_id = response.json().get('items')[0].get('answer_id')
        link_to_top1_answer = f'https://stackoverflow.com/a/{answer_id}'
        return link_to_top1_answer
    except Exception:
        print("Request limited! We can make only 300 requests per day :(")
        sys.exit()


def main():
    '''
    script lấy top **N** câu hỏi được vote cao nhất của tag **LABEL**
    trên stackoverflow.com.
    In ra màn hình: Title câu hỏi, link đến câu trả lời được vote cao nhất,
    Dạng của câu lệnh::
    `so.py N LABLE`
    '''
    # Parse args
    paser = argparse.ArgumentParser(description="Get top N question with LABLE on stackoverflow") # NOQA
    paser.add_argument("N", help="Get top N question",type=int) # NOQA
    paser.add_argument("LABLE", help="Get question with tag is given lable",type=str) # NOQA
    args = paser.parse_args()

    number_of_question = args.N
    lable = args.LABLE

    # Hiển thị kết quả
    for question in questions(number_of_question, lable):
        question_title, _ = question
        print(question_title, end=" | ")
        print(top1_answer(question))


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
from collections import Counter
import jieba

# 請求頭
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36'
}

# 獲取網頁內容
def get_webpage_content(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"無法獲取網頁內容: {e}")
        return None

# 提取文本並進行分詞
def extract_and_tokenize_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    # 找到具有"nr_title"類的<div>元素並提取文本
    title_div = soup.find('div', class_='content_detail')
    if title_div:
        title_text = title_div.get_text().strip()
    else:
        title_text = ""

    # 提取纯文本内容
    text = soup.get_text()
    # 使用jieba分詞對文本進行中文分詞
    words = list(jieba.cut(text))
    words = [word.lower() for word in words if word.isalnum()]
    return title_text, words


#統計並獲取出出現頻率最高的詞
def most_common_words(words, top_n=10):
    word_counter = Counter(words)
    return word_counter.most_common(top_n)

if __name__ == "__main__":
    # 第一頁網址
    base_url = "https://m.42zw.la/book/31955/20053753.html"
    current_url = base_url
    all_words = []

    while current_url:
        webpage_content = get_webpage_content(current_url)
        if webpage_content:
            title, words = extract_and_tokenize_text(webpage_content)
            all_words.extend(words)

            # 查找下一頁，如果有的话
            soup = BeautifulSoup(webpage_content, 'html.parser')
            next_page_link = soup.find('a', id='lastchapter')

            if next_page_link and next_page_link.get('href'):
                next_page_url = next_page_link.get('href')
                current_url = f"https://m.bqg9527.net{next_page_url}"
            else:
                current_url = None
        else:
            current_url = None

    print("章節標题：", title)
    print("出現最多的兩個中文字词：")
    word_counter = Counter(all_words)
    two_character_words = [word for word in word_counter.keys() if len(word) == 2]
    sorted_two_character_words = sorted(two_character_words, key=lambda word: word_counter[word], reverse=True)
    for word in sorted_two_character_words[:10]:
        print(f"{word}: {word_counter[word]}次")

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2

# url definition
url = "https://www.theguardian.com/uk"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html.parser')

# News identification
coverpage_news = soup1.find_all('h3', class_='fc-item__title')
# print(len(coverpage_news))
# print(coverpage_news[0])

number_of_articles = 5

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):

    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n].find('a')['href']:
        # print(coverpage_news[n].find('a')['href'])
        continue

    print(n)

    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    list_links.append(link)

    # Getting the title
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    body = soup_article.find_all('div', class_='content__article-body from-content-api js-article__body')
    x = body[0].find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    news_contents.append(final_article)

df_features = pd.DataFrame({'Content': news_contents })

df = df_features

print(list_titles)

    # df_show_info
df_show_info = pd.DataFrame({'Article Title': list_titles,'Article Link': list_links,'Newspaper': 'The Guardian'})

df['Content'] = df['Content'].str.replace("\r", " ")
df['Content'] = df['Content'].str.replace("\n", " ")
df['Content'] = df['Content'].str.replace("    ", " ")
df['Content'] = df['Content'].str.replace('"', '')
df['Content'] = df['Content'].str.lower()
punctuation_signs = list("?:!.,;")
df['Content'] = df['Content']

for punct_sign in punctuation_signs:
    df['Content'] = df['Content'].str.replace(punct_sign, '')

df['Content'] = df['Content'].str.replace("'s", "")

print(df)

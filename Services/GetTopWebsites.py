from googlesearch import search
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import spacy
import re
import pytextrank

# Step 1. Getting top n urls from Google's search results


def get_links_from_google(term, num_results=10, lang="en"):
    url_list = [
        x for x in search(term=term, lang=lang, num_results=num_results)
    ]
    return pd.DataFrame(url_list, columns=["url"])


# Testing step 1
# df = get_links_from_google("How to learn English", 5)

# Step 2. Getting the content of the top n pages


def get_page_content(url):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    with HTMLSession() as session:
        try:
            res = session.get(url, headers=headers, timeout=200)
            return BeautifulSoup(res.content, "html.parser").text
        except:
            return BeautifulSoup("", "html.parser").text
        finally:
            print(f"Done Scrapping")


# Testing step 2
# Step 3. Cleaning the text content from pages


def text_cleaning(text):
    try:
        # removing more than one newline or spaces
        text = re.sub(r"[\n\r]+", "\n", text)
    except:
        print(f"Failed to clean")
    return text


# Testing step 3
# Step 4. Extracting Keyphrases from content
def get_top_n_keyphrases(text, top_n=25):

    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    if top_n > len(doc._.phrases):
        top_n = len(doc._.phrases)

    rank_dict = {phrase.text: phrase.rank for phrase in doc._.phrases[:top_n]}
    return pd.DataFrame.from_dict(rank_dict, orient="index")


# Testing step 4

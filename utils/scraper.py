import requests

from urllib.parse import urlparse

from utils.config import (
    APYHUB_API_KEY,
    gemini
)
from utils.json_utils import safe_json_loads

def is_valid_url(url):

    try:

        parsed = urlparse(url)

        return all([
            parsed.scheme,
            parsed.netloc
        ])

    except:

        return False

def extract_webpage(url):

    headers = {

        "apy-token": APYHUB_API_KEY

    }

    params = {

        "url": url

    }

    response = requests.get(

        "https://api.apyhub.com/extract/text/webpage",

        headers=headers,

        params=params,

        timeout=60

    )

    response.raise_for_status()

    result = response.json()

    webpage = (

        result.get("data")

        or result.get("text")

        or result.get("content")

        or ""

    )

    if not webpage:

        raise Exception(

            "No webpage content extracted."

        )

    return webpage

def clean_article(raw_text):

    prompt = f"""
            You are a professional news extractor.

            Extract ONLY the actual news article.

            Remove:

            - navigation
            - advertisements
            - comments
            - author widgets
            - recommended posts
            - footer
            - cookie notices
            - repeated paragraphs

            Return ONLY JSON.

            {{
            "title":"",

            "article":""

            }}

            Raw webpage:

            {raw_text}
    """

    response = gemini.generate_content(prompt)

    output = response.text.strip()

    article = safe_json_loads(
        output,
        default={"title": "", "article": ""}
    )

    return (

        article["title"],

        article["article"]

    )



def scrape_news(url):

    if not is_valid_url(url):

        raise Exception(

            "Invalid URL."

        )

    webpage = extract_webpage(url)

    title, article = clean_article(webpage)

    return {

        "title": title,

        "article": article

    }
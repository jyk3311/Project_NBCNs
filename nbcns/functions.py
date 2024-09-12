import requests
from bs4 import BeautifulSoup  # HTML 파싱을 위해 BeautifulSoup 사용
from django.conf import settings  # Django 설정에서 API 키 가져오기 위해 사용
from openai import OpenAI  # OpenAI API 사용을 위해 임포트

# 주어진 URL에서 제목과 정리된 텍스트를 모두 가져오는 함수
def fetch_title_and_clean_content(url):

    #url 파싱
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # HTML 문서의 제목을 가져오거나, 제목이 없으면 "제목없음" 반환
    title = soup.title.text if soup.title else "제목없음"

    # HTML 문서에서 script와 style 태그를 제거
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # 남은 텍스트를 정리하여 줄 단위로 나누고, 중복된 공백을 제거
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)

    return title, clean_text  # 제목과 정리된 텍스트를 함께 반환

# 주어진 텍스트를 GPT 모델을 이용해 요약하는 함수
def NBCNGpts(text):

    CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)

    system_instruction = """
    뉴스 기사를 크롤링한 텍스트를 받아서 기사 내용을 정리 하여 개발자가 이해 하기 쉽도록 작성 하며 뉴스 기사가 한국어가 아니라면 한국어로 번역해서 요약해줘.
    """

    completion = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": text},
        ]
    )

    return completion.choices[0].message.content

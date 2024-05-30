import requests
import json
from bs4 import BeautifulSoup


def crawling(crawl_type) :
    #경향신문 O, 국민일보 X, 내일신문 O , 동아일보 O, 문화일보 O, 서울신문 O, 서울일보 O, 세계일보 X, 아시아투데이 O, 조선일보, 중앙일보 O , 한겨레 (크롤링 허용 X), 한국일보 (크롤링 허용 X)
    data_bundle = crawl_khan(crawl_type) # 경향신문 크롤링
    data_bundle.extend(crawl_naeil(crawl_type)) #내일신문 크롤링
    data_bundle.extend(crawl_donga(crawl_type)) #동아일보 크롤링

    data_bundle.extend(crawl_munhwa(crawl_type)) # 문화일보 크롤링
    data_bundle.extend(crawl_seoulNews(crawl_type)) # 서울신문 크롤링
    data_bundle.extend(crawl_seoulIlbo(crawl_type)) # 서울일보 크롤링
    #data_bundle.extend(crawl_segye(crawl_type)) # 세계일보 크롤링(미구현)
    data_bundle.extend(crawl_asia(crawl_type)) # 아시아투데이 크롤링

    data_bundle.extend(crawl_joongang(crawl_type)) #중앙일보 크롤링
    

    
    #JSON 형식으로 데이터 변환 및 타입 태그 추가
    data = {
        'crawl_type' : crawl_type,
        'data' : data_bundle
    }
    
    print(data)
        
    return data

def selectCrawlType(crawl_type) :
    CRAWL_TYPES = ['economy', 'politics', 'society', 'culture', 'science', 'world', 'sport', 'enter', 'people', 'education'] # 크롤링 타입 리스트
    #경제, 정치, 사회, 문화, 과학(IT), 세계, 스포츠, 연예

    #crawl_type 에 따라 조건문 수행
    if(crawl_type in CRAWL_TYPES ) : # 리스트에 포함된 타입인 경우에만 수행
        return crawling(crawl_type)
    else : # 잘못된 타입인 경우
        return {
            'crawl_type' : crawl_type,
            'title' : "no data",
            'content' : "no data"
        }
        

    

def crawl_khan(crawl_type) : # 경향신문 크롤링, 경향 신문에는 사진과 제목만 존재하고 본문이 없는 경우도 있음. 현제 1페이지만 크롤링 가능. 기능 추가 필요함
    TYPETAG = {'politics' : 'politics', 
               'economy' : 'economy', 'society' : 'national', 'culture' : 'culture', 'science' : 'science', 'world' : 'world', 'sport' : 'sports'} # 타입에 따른 주소 태그의 딕셔너리
    
    if not (crawl_type in TYPETAG) :
        return {}
    
    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.khan.co.kr/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='main-list-wrap')
    news = newsBox.select('.line_clamp2')

    for link in news: # 뉴스마다 제목과 내용을 따옴

        subRes = requests.get(link.attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')

        article_text = subSoup.select('#articleBody')
        
        title = link.attrs['title']

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거
    
        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_naeil(crawl_type) : # 내일신문 크롤링
    TYPETAG = {'politics' : 'politics',
               'economy' : 'economy', 'society' : 'policy', 'science' : 'industry', 'world' : 'diplomacy'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.naeil.com/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='story-list')
    news = newsBox.find_all(class_ = 'headline')

    for link in news: # 뉴스마다 제목과 내용을 따옴

        subRes = requests.get("https://www.naeil.com" + link.find('a').attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('.article-view')

        title = link.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거

        #print(content)
        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_donga(crawl_type) : # 동아일보 크롤링
    TYPETAG = {'politics' : 'Politics',
               'economy' : 'Economy', 'society' : 'Society', 'culture' : 'Culture', 'world' : 'Inter', 'sport' : 'Sports',
               'enter' : 'Entertainment'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.donga.com/news/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='row_list')
    news = newsBox.select('.tit')
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get(link.find('a').attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('.news_view')

        title = link.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_joongang(crawl_type) : # 중앙일보 크롤링
    TYPETAG = {'politics' : 'politics', 
               'economy' : 'money', 'society' : 'society', 'culture' : 'culture', 'world' : 'world', 'sport' : 'sports'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}  
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.joongang.co.kr/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='story_list')
    news = newsBox.select('.headline')
    #print(news)
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get(link.find('a').attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('#article_body')
        #print(article_text)
        title = link.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    #print(data_bundle)

    return data_bundle

def crawl_munhwa(crawl_type) : # 문화일보 크롤링
    TYPETAG = {'politics' : 'politics',
               'economy' : 'economy', 'society' : 'society', 'culture' : 'culture', 'world' : 'international',
               'sport' : 'sports', 'enter' : 'ent', 'people':'people'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.munhwa.com/news/section_main.html?sec="+str(TYPETAG[crawl_type])+"&class=30", headers=header)
    html = res.content.decode('euc-kr','replace') # 인코딩을 euc-kr로 바꿈
    soup = BeautifulSoup(html, 'html.parser')
    
    newsBox = soup.find(class_='news_list')
    news = newsBox.select('a.title')
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get("https:" + link.attrs['href'], headers=header)
        html = subRes.content.decode('euc-kr','replace') # 인코딩을 euc-kr로 바꿈

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('#News_content')

        title = link.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_seoulNews(crawl_type) : # 서울신문 크롤링
    TYPETAG = {'politics' : 'politics',
                'economy' : 'economy', 'society' : 'society', 'culture' : 'life', 'world' : 'international', 'sport' : 'sport',
                'people' : 'peoples'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.seoul.co.kr/newsList/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.content.decode('utf-8','replace') # 인코딩을 utf-8로 바꿈
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='pageListWrap')
    news = newsBox.select('.articleTitle')
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get("https://www.seoul.co.kr/" + link.find('a').attrs['href'], headers=header)
        html = subRes.content.decode('utf-8','replace') # 인코딩을 utf-8로 바꿈

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('.viewContent')

        title = link.find('h2')
        title = title.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip()
            content = content.replace('\n', ' ') # 개행 제거
            content = content.replace('\t', '')
            content = content.replace('\r', '')

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_seoulIlbo(crawl_type) : # 서울일보 크롤링
    TYPETAG = {'politics' : '8',
                'economy' : '9', 'society' : '10', 'culture' : '11', 'enter' : '12', 'world' : '14',
                'education' : '20'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.seoulilbo.com/news/articleList.html?sc_section_code=S1N"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='section-body')
    news = newsBox.select('h4', attrs={"class": "titles"})
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get("https://www.seoulilbo.com/"+link.find('a').attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('#article-view-content-div')

        title = link.text.strip()

        for letter in article_text: # 내용 따오기
            letter = letter.text.strip()
            letter = letter.replace('\xa0', ' ')
            letter = letter.replace('\n', ' ')
            content = letter # 개행 제거

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

'''
# newsBox.select() 에서 오류
def crawl_segye(crawl_type) : # 세계일보 크롤링
    TYPETAG = {'politics' : 'news/politics',
                'society' : 'news/society', 'culture' : 'news/culture', 'sport' : 'sports',
                'enter' : 'entertainment'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.segye.com/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    
    newsBox = soup.find(id='wps_layout2_box2')
    news = newsBox.select('ul>li>a')
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get(link.attrs['href'], headers=header)
        html = subRes.text

        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('.viewBox2')

        title = link.find(class_='tit')
        title = title.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip()
            content = content.replace('\n', ' ') # 개행 제거
            content = content.replace('\t', '')
            content = content.replace('\r', '')

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle
'''

def crawl_asia(crawl_type) : # 아시아투데이 크롤링
    TYPETAG = {'politics' : '2',
                'society' : '3', 'economy' : '4', 'world' : '6', 'culture' : '7&d2=5', 'sport' : '7&d2=7',
                'enter' : '7&d2=2'} # 타입에 따른 주소 태그의 딕셔너리

    if not (crawl_type in TYPETAG) :
        return {}

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://www.asiatoday.co.kr/kn_section.php?d1="+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='sub_section_news_box')
    news = newsBox.select('dl>dd>a')
    
    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get("https://www.asiatoday.co.kr" + link.attrs['href'], headers=header)
        html = subRes.text
        
        subSoup = BeautifulSoup(html, 'html.parser')
        article_text = subSoup.select('.news_bm')

        title = link.find('h4')
        title = title.text.strip()

        for letter in article_text: # 내용 따오기
            content = letter.text.strip()
            content = content.replace("\xa0", ' ')

        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

#Not in use

def crawl_naver(crawl_type) : # 네이버 뉴스 크롤링
    TYPETAG = {'politics' : 100, 
               'economy' : 101, 'society' : 102, 'culture' : 103, 'science' : 105, 'world' : 104} # 타입에 따른 주소 태그의 딕셔너리

    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열
    
    res = requests.get("https://news.naver.com/section/"+str(TYPETAG[crawl_type]), headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find('div', attrs={"class": "section_latest"})
    news = newsBox.select('.sa_text_title')

    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get(link.attrs['href'], headers=header)
        html = subRes.text
        subSoup = BeautifulSoup(html, 'html.parser')

        article_text = subSoup.select('#dic_area')

        title = link.text.strip() # 제목 따오기

        for letter in article_text: # 내용 따오기
            content = letter.text.strip()
    
        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

def crawl_daum(crawl_type) : # 다음 뉴스 크롤링
    TYPETAG = {'politics' : 'politics', 
               'economy' : 'economic', 'society' : 'society', 'culture' : 'culture', 'science' : 'digital', 'world' : 'foreign'} # 타입에 따른 주소 태그의 딕셔너리
    
    if TYPETAG.get(crawl_type) == None :
        return {}
    
    header = {'User-agent' : 'Mozila/2.0'}
    data_bundle=[] # 뉴스 정보를 담고 있는 JSON들의 배열

    res = requests.get("https://news.daum.net/"+str(TYPETAG[crawl_type]) + '#1', headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    newsBox = soup.find(class_='list_newsmajor')
    news = newsBox.select('.link_txt')

    for link in news: # 뉴스마다 제목과 내용을 따옴
        subRes = requests.get(link.attrs['href'], headers=header)
        html = subRes.text
        subSoup = BeautifulSoup(html, 'html.parser')

        article_text = subSoup.select('.article_view')

        title = link.get_text() # 제목 따오기

        for letter in article_text: # 내용 따오기
            content = letter.text.strip().replace('\n', '') # 개행 제거
    
        # 제목과 내용 배열에 삽입
        data_bundle.append({"title": title, "content": content})

    return data_bundle

crawling('politics')
import praw
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

reddit = praw.Reddit(
    client_id="fRgIGad0O43Lydb5e4-b5A",
    client_secret="LU7k6xjvHSmKQm68FLESNfCDBpPw5Q",
    user_agent="sexOffenderDTx by zox2m",
)

print("Reddit instance initialized successfully!")

# 필요한 NLTK 데이터 다운로드
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

# 불용어 다운로드
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# 서브레딧명
# SexOffenderSupport
# sexualassault
# CriminalProfiling
# worldnews
# psychology
# all
subredditName = 'SexOffenderSupport'

# 키워드명 
# sexual offender 
# sex
# sa
keyword = 'sex offender'

# 데이터명
dataName = subredditName + "_"+ keyword

# 데이터 수집
subreddit = reddit.subreddit(subredditName) 
text_data = []

# 서브레딧으로 특정 키워드 검색하는 것 
'''
for submission in subreddit.search(keyword, limit=100):  # limit은 필요에 맞게 조정
    text_data.append(submission.title)
    text_data.append(submission.selftext)
'''

# 아래는 검색 키워드 없이 게시판 hot 게시글 불러오는 방법 
for submission in subreddit.hot(limit=1000):
    text_data.append(submission.title)
    text_data.append(submission.selftext)


# 텍스트 데이터 전처리 및 불용어 제거
all_text = ' '.join(text_data)
all_text = re.sub(r"'", ' ', all_text)  # '를 공백으로 대체
all_text = re.sub(r'[^a-zA-Z\s]', '', all_text)  # 특수문자 제거
all_text = all_text.lower().split()  # 소문자로 변환 후 split

# POS 태깅
words_with_pos = nltk.pos_tag(all_text)

# 명사(NN, NNS, NNP, NNPS)만 필터링
nouns = [word for word, pos in words_with_pos if pos.startswith('NN')]

# 불용어 제거
stop_words = set(stopwords.words('english'))

filtered_text = [word for word in nouns if word not in stop_words]

# 키워드 카운트
word_count = Counter(filtered_text)

# 빈도가 10이하 단어 제거
filtered_word_count = {word: count for word, count in word_count.items() if count > 10}

# 자주 등장하는 단어 CSV로 저장
df = pd.DataFrame(filtered_word_count.items(), columns=['Word', 'Count'])
df = df.sort_values(by='Count', ascending=False)
df.to_csv(dataName+'.csv', index=False)

# 워드 클라우드 생성
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(filtered_word_count)

# 워드 클라우드를 PNG 파일로 저장
wordcloud.to_file(dataName+'.png')

# 워드 클라우드 표시 
'''
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
'''
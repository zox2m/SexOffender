import praw
import pandas as pd
import time

# Reddit API 초기화
reddit = praw.Reddit(
    client_id="fRgIGad0O43Lydb5e4-b5A",
    client_secret="LU7k6xjvHSmKQm68FLESNfCDBpPw5Q",
    user_agent="sexOffenderDTx by zox2m",
)

print("Reddit instance initialized successfully!")

# 서브레딧 및 데이터 초기화
subreddit_name = 'SexOffenderSupport'
data_name = f"{subreddit_name}_extended_posts"
subreddit = reddit.subreddit(subreddit_name)

posts_data = []

# 페이징 수집
limit_per_request = 100  # 한 번에 가져올 게시글 수 (최대 100)
total_limit = 2000  # 총 가져올 게시글 수 (예: 5000)
after = 1000  # 초기값 None

while len(posts_data) < total_limit:
    # 게시글 수집
    submissions = subreddit.hot(limit=limit_per_request, params={"after": after})
    count = 0
    
    for submission in submissions:
        post_content = {
            "Title": submission.title,
            "Content": submission.selftext,
            "Comments": submission.num_comments,
        }
        posts_data.append(post_content)
        count += 1
    
    # 페이징 정보 업데이트
    after = submissions._listing.after
    if not after:
        print("No more posts to fetch.")
        break  # 더 이상 가져올 데이터가 없으면 종료
    
    print(f"Fetched {count} more posts. Total collected: {len(posts_data)}")
    time.sleep(1)  # Reddit API rate limit 준수

# DataFrame 생성
df = pd.DataFrame(posts_data)

# DataFrame 저장
df.to_csv(data_name + ".csv", index=False)

print(f"Data saved to {data_name}.csv with {len(posts_data)} posts.")

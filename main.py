import requests
import time

# Hugging Face API URL 및 헤더 정보 설정
API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-emotion-analysis"
headers = {
    "Authorization": "Bearer hf_apiKey"  # hugging face API key
}

# 분석할 텍스트 입력
data = {
    "inputs": "I was a spectator to my own self destruction while I fought myself over the guilt and shame versus feeding my addiction. ",
}


# 모델 로드 완료 시까지 반복 시도 - 로딩하는 시간이 꽤 걸리기 때문. 
while True:
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(result)  # 예: [{'label': 'fear', 'score': 0.95}]

        # 제일 높은 감정 출력
        # result는 이중 리스트로 반환되므로 첫 번째 요소로 접근
        emotions = result[0]  
        top_emotion = max(emotions, key=lambda x: x['score'])
        print(f"가장 강한 감정은: {top_emotion['label']} (확률: {top_emotion['score']})")

        break
    elif response.status_code == 503:
        print("Model is still loading, waiting for a while...")
        time.sleep(5)  # 5초 대기 후 다시 시도
    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

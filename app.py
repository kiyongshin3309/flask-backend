from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS 추가
import hgtk
import time
import random

app = Flask(__name__)
CORS(app)

# 연습 문장 리스트 (첨부파일 기반)
word_list = [
    "한글은 아름다운 언어입니다.",
    "타자 연습을 통해 속도를 향상시킵니다.",
    "빠르게 타이핑하는 것은 중요합니다.",
    "연습을 하면 실력이 향상됩니다.",
]

# 사용자의 타이핑 시작 시간을 저장할 딕셔너리
user_start_times = {}

@app.route("/")
def home():
    return "Flask 서버가 정상적으로 실행 중입니다!"

# 랜덤 연습 문구 제공 API
@app.route("/api/get_word", methods=["GET"])
def get_word():
    sentence = random.choice(word_list)  # 랜덤 문구 선택
    return jsonify({"word": sentence})

# 타이핑 시작 시간 기록 API
@app.route("/api/start", methods=["POST"])
def start_typing():
    user_id = request.json.get("user_id")
    user_start_times[user_id] = time.time()  # 현재 시간 저장
    return jsonify({"message": "타이핑 시작 시간이 기록되었습니다."})

# hgtk 모듈을 활용한 타이핑 속도 및 정확도 측정 API
@app.route("/api/typing", methods=["POST"])
def check_typing():
    data = request.get_json()
    user_id = data.get("user_id")
    user_input = data.get("text", "")
    correct_text = data.get("correct_text", "")  # 정답 문장
    start_time = user_start_times.get(user_id)

    if not start_time:
        return jsonify({"error": "타이핑 시작 시간이 기록되지 않았습니다."}), 400

    end_time = time.time()
    typing_time = end_time - start_time  # 총 소요 시간 (초)

    # 한글 자모 분석을 위한 hgtk 활용
    decomposed_input = hgtk.text.decompose(user_input)  # 사용자가 입력한 문장 분해
    decomposed_correct = hgtk.text.decompose(correct_text)  # 정답 문장 분해

    # 정확도 계산 (자모 기준)
    correct_count = sum(1 for i in range(min(len(decomposed_input), len(decomposed_correct))) 
                        if decomposed_input[i] == decomposed_correct[i])
    accuracy = (correct_count / len(decomposed_correct)) * 100 if decomposed_correct else 0

    # 한글 입력의 경우 자모 단위로 구분하여 분석
    words_per_minute = (len(correct_text) / typing_time) * 60  # 분당 입력 속도 (WPM)

    result = {
        "message": "타이핑 완료",
        "accuracy": round(accuracy, 2),  # 정확도 (%)
        "speed": round(words_per_minute, 2),  # WPM
        "time_taken": round(typing_time, 2),  # 걸린 시간 (초)
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

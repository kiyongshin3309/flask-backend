from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask 서버가 정상적으로 실행 중입니다!"

@app.route("/api/typing", methods=["POST"])
def check_typing():
    data = request.get_json()
    user_input = data.get("text", "")
    return jsonify({"message": "타이핑 결과", "user_input": user_input})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

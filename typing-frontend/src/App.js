import React, { useState, useEffect } from "react";
import API_BASE_URL from "./config";

function App() {
    const [word, setWord] = useState(""); // 연습 문구
    const [text, setText] = useState(""); // 사용자가 입력한 텍스트
    const [result, setResult] = useState(null); // 결과 데이터
    const [userId, setUserId] = useState(`user-${Math.random()}`); // 사용자 ID

    // 서버에서 연습 문구 가져오기
    const fetchWord = async () => {
        const response = await fetch(`${API_BASE_URL}/api/get_word`);
        const data = await response.json();
        setWord(data.word);
    };

    // 타이핑 시작 기록 (서버에 시작 시간 저장)
    const startTyping = async () => {
        await fetch(`${API_BASE_URL}/api/start`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId }),
        });
    };

    // 타이핑 결과 전송
    const checkTyping = async () => {
        const response = await fetch(`${API_BASE_URL}/api/typing`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: userId,
                text,
                correct_text: word,
            }),
        });
        const data = await response.json();
        setResult(data);
    };

    // 페이지 로드 시 연습 문구 가져오기
    useEffect(() => {
        fetchWord();
    }, []);

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>한글 타자 연습</h1>
            <p><strong>연습 문장:</strong> {word}</p>
            <input 
                type="text" 
                value={text} 
                onChange={(e) => setText(e.target.value)}
                onFocus={startTyping} // 입력창 클릭 시 타이핑 시작
                placeholder="문장을 입력하세요"
            />
            <button onClick={checkTyping}>확인</button>
            {result && (
                <div>
                    <p><strong>정확도:</strong> {result.accuracy}%</p>
                    <p><strong>속도:</strong> {result.speed} WPM</p>
                    <p><strong>소요 시간:</strong> {result.time_taken} 초</p>
                </div>
            )}
        </div>
    );
}

export default App;

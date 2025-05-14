from gpt_functions import (
    get_current_time,
    get_yf_stock_info,
    get_yf_stock_history,
    tools
)
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

# ✅ 환경 변수 로드 및 OpenAI 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ✅ GPT 응답 생성 함수
def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )
    return response

# ✅ Streamlit 앱 시작
st.title("💬 Chatbot")

# ✅ 세션 상태에 메시지 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},
    ]

# ✅ 이전 메시지 출력
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        st.chat_message(msg["role"]).write(msg["content"])

# ✅ 사용자 입력 처리
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = ai_response.choices[0].message

    tool_calls = ai_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            arguments = json.loads(tool_call.function.arguments)

            try:
                if tool_name == "get_current_time":
                    func_result = get_current_time(timezone=arguments['timezone'])

                elif tool_name == "get_yf_stock_info":
                    func_result = get_yf_stock_info(ticker=arguments['ticker'])

                elif tool_name == "get_yf_stock_history":
                    func_result = get_yf_stock_history(
                        ticker=arguments['ticker'],
                        period=arguments['period']
                    )

                else:
                    func_result = "❗️지원되지 않는 함수입니다."

            except Exception as e:
                func_result = f"❗️ 데이터를 가져오는 중 오류 발생: {str(e)}"

            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": func_result,
            })

        # 툴 실행 결과 기반 재요청
        st.session_state.messages.append({
            "role": "system",
            "content": "이제 주어진 결과를 바탕으로 답변할 차례다."
        })

        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

    # ✅ GPT 응답 최종 출력
    final_text = ai_message.content or "(❗️ GPT 응답이 없습니다)"
    st.session_state.messages.append({"role": "assistant", "content": final_text})
    st.chat_message("assistant").write(final_text)

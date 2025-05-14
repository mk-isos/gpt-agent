from gpt_functions import (
    get_current_time,
    get_yf_stock_info,
    tools
)
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

# 🔹 환경 변수에서 OPENAI API 키 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 🔹 GPT 응답 생성 함수
def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )
    return response

# 🔹 Streamlit UI 시작
st.title("💬 Chatbot")

# 🔹 메시지 세션 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},
    ]

# 🔹 이전 메시지 출력
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        st.chat_message(msg["role"]).write(msg["content"])

# 🔹 사용자 입력 받기
if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 🔸 GPT에게 메시지 전달
    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    ai_message = ai_response.choices[0].message
    print("🔍 AI tool call 응답:", ai_message)

    # 🔹 tool_call 수행
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            arguments = json.loads(tool_call.function.arguments)

            # 🔸 함수 실행
            if tool_name == "get_current_time":
                func_result = get_current_time(timezone=arguments["timezone"])
            elif tool_name == "get_yf_stock_info":
                func_result = get_yf_stock_info(ticker=arguments["ticker"])
            else:
                func_result = f"{tool_name}은 아직 구현되지 않았습니다."

            # 🔸 함수 실행 결과를 function 역할로 기록
            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": func_result,
            })

        # 🔸 다시 GPT에게 결과 기반 응답 요청
        st.session_state.messages.append({
            "role": "system",
            "content": "이제 주어진 결과를 바탕으로 답변할 차례다.",
        })

        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

    # 🔹 최종 assistant 메시지 출력
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message.content
    })
    print("🤖 AI:", ai_message.content)
    st.chat_message("assistant").write(ai_message.content)

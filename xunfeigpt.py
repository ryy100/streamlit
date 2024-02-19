import streamlit as st
from streamlit_chat import message

import SparkApi
# 设置 API 信息
appid = st.secrets["appid"]
api_secret = st.secrets["api_secret"]
api_key = st.secrets["api_key"]
domain = "generalv3"
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"

# 初始化 Streamlit 状态
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

def add_to_conversation(role, content):
    st.session_state['conversation'].append({"role": role, "content": content})

def call_spark_api(conversation):
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, conversation)
    return SparkApi.answer

# 自定义 CSS 函数来添加背景图

def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://www.zjczxy.cn/images/banner3.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )


def app():
    # 调用函数应用背景图
    add_bg_from_url()
    st.title("智能问答助手")

    # 创建两栏布局
    col1, col2 = st.columns([1, 1.5])  # 比例为1:1.5，可根据需要调整

    # 第一栏：应用介绍和说明
    with col1:
        with st.container():
            st.markdown("<h4>智能机器人</h4>", unsafe_allow_html=True)
            st.markdown("<p>我可以回答您的任何问题！</p>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #f5232f;'>使用说明</h4>", unsafe_allow_html=True)
            st.markdown("<p style='color: #ff7f50;'>在右侧输入框中输入您的问题。</p>", unsafe_allow_html=True)

    # 第二栏：用户输入和对话历史
    with col2:
        user_input = st.text_input("请输入您的问题:", key='input')
        send_button = st.button("发送")
        new_chat_button = st.button("新聊天")

        if send_button and user_input:
            add_to_conversation("user", user_input)
            answer = call_spark_api(st.session_state['conversation'])
            add_to_conversation("assistant", answer)
            # st.session_state['input'] = ''  # 清空输入框

        if new_chat_button:
            st.session_state['conversation'] = []  # 清空对话历史

        # 渲染对话
        for chat in reversed(st.session_state['conversation']):
            if chat["role"] == "assistant":
                message(chat["content"])
            else:
                message(chat["content"], is_user=True)



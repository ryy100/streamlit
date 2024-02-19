import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    # 加载并显示 Lottie 动画
    lottie_url1 = 'https://lottie.host/a7de7503-9369-4f17-8557-759b2f0a8f0a/sEa71OXtng.json'
    lottie_url2 = 'https://lottie.host/f6ac6fcc-dfec-460e-9de5-e549adecef21/NIhTvMtdMY.json'
    lottie_animation1 = load_lottie(lottie_url1)
    lottie_animation2 = load_lottie(lottie_url2)
    # 主页的内容
    with st.container():
        image_column, text_column = st.columns((1, 3))
        with image_column:
            st_lottie(lottie_animation1, height=100, key='coding')
        with text_column:
            st.title("欢迎来到数据分析与可视化工具")

    with st.container():
        l_column, r_column = st.columns(2)
        with l_column:
            st.write("""
                这是一个简单的应用，用于展示数据分析和数据可视化的能力。\n
                - 在 **频率分布图** 页面，您可以上传数据文件，进行绘制频率分布图。
                - 在 **饼状图和直方图** 页面，您可以查看数据的图形表示，如饼图和条形图。
                - 在 **决策树** 页面，您可以利用决策树算法对数据进行预测分析。
            """)
        with r_column:
            st_lottie(lottie_animation2, height=300, key="cod")



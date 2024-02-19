import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

def app():
    # 饼状图和直方图页面的内容
    st.title("饼状图和直方图")

    # 文件上传
    uploaded_file = st.file_uploader("选择文件（ldeaths.csv）", type=["csv"], key="visualization")

    if uploaded_file is not None:
        # 读取数据
        data = pd.read_csv(uploaded_file, encoding='GBK')

        # 绘制饼图
        fig1, ax1 = plt.subplots()
        ax1.pie(data['死亡人数'], labels=data['月份'], autopct='%1.2f%%')
        plt.title('1974年英国每个月死于支气管炎、肺气肿和哮喘病的人数分布（饼图）')
        st.pyplot(fig1)

        # 绘制条形图
        fig2, ax2 = plt.subplots()
        ax2.bar(data['月份'], data['死亡人数'])
        plt.title('1974年英国每个月死于支气管炎、肺气肿和哮喘病的人数分布（条形图）')
        plt.xlabel('月份')
        plt.ylabel('死亡人数/人')
        st.pyplot(fig2)
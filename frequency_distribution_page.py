import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

def app():
    # 频率分布图页面的内容
    st.title("频率分布图")
    with st.container():
        st.write("""
        定量数据的分布分析，一般按照以下步骤进行。\n
        - 求极差
        - 决定组距与组数
        - 决定分点
        - 列出频率分布表
        - 绘制频率分布直方图
        """)

    uploaded_file = st.file_uploader("选择文件（lh .csv）", type=["csv"])
    if uploaded_file is not None:
        # 读取数据
        sale = pd.read_csv(uploaded_file, encoding='GBK')
        sale = np.array(sale)

        # 求极差
        sale_jicha = max(sale) - min(sale)

        # 分组，这里取初始组距为1000
        group = round(sale_jicha[0] / 0.25)  # 确定组数

        # 根据group对数据进行切片，即决定分点
        bins = np.linspace(min(sale), max(sale), group)

        # 根据分点确定最终组距
        zuju = bins[1] - bins[0]

        # 显示极差、分组组数、分点、最终组距
        st.write(f'极差为: {sale_jicha}')
        st.write(f'分组组数为: {group}')
        st.write(f'分点为：\n {bins}')
        st.write(f'最终组距为: {zuju}')

        # 绘制频率分布表
        table_fre = pd.DataFrame(np.zeros([6, 5]), columns=['组段', '组中值x', '频数', '频率f', '累计频率'])
        f_sum = 0  # 累计频率初始值
        for i in range(len(bins) - 1):
            table_fre.at[i, '组段'] = f'[{round(bins[i][0], 2)},{round(bins[i + 1][0], 2)})'
            table_fre.at[i, '组中值x'] = round(np.array([bins[i], bins[i + 1]]).mean(), 2)
            table_fre.at[i, '频数'] = sum([1 for j in sale if bins[i] <= j < bins[i + 1]])
            table_fre.at[i, '频率f'] = table_fre.at[i, '频数'] / len(sale)
            f_sum += table_fre.at[i, '频率f']
            table_fre.at[i, '累计频率'] = f_sum

        # 显示频率分布表
        st.write('频率分布表为：', table_fre)

        # 计算频率与组距的比值，作为频率分布直方图的纵坐标
        y = table_fre['频率f'] / zuju

        # 绘制频率分布直方图
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.bar(table_fre['组段'], y, width=0.8)
        ax.set_xlabel('分布区间')
        ax.set_ylabel('频率/组距')
        ax.set_title('频率分布直方图')
        st.pyplot(fig)
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from streamlit_lottie import st_lottie

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    st.title("决策树模型")
    lottie_url = 'https://lottie.host/72c56b42-152e-47d9-9502-a631e7ff7afe/v6bJrr0uS7.json'
    lottie_animation1 = load_lottie(lottie_url)
    with st.container():
        text_column,image_column = st.columns((2, 1))
        with text_column:
            st.write("""
                决策树：从训练数据中学习得出一个树状结构的模型。\n
                    决策树属于判别模型。
                    - 决策树是一种树状结构，通过做出一系列决策（选择）来对数据进行划分，这类似于针对一系列问题进行选择。
                    - 决策过程就是从根节点开始，测试待分类项中对应的特征属性，并按照其值选择输出分支，
                    - 直到叶子节点，将叶子节点的存放的类别作为决策结果。
                        """)
        with image_column:
            st_lottie(lottie_animation1, height=150, key='coding')


    # 文件上传
    uploaded_file = st.file_uploader("上传 EEG Eye State 数据文件", type=["txt"])

    if uploaded_file is not None:
        # 读取数据
        data = pd.read_table(uploaded_file, sep=',')
        X = data.iloc[:, :14]
        y = data.iloc[:, 14]

        # 数据标准化
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        # 划分训练集、测试集
        traindata, testdata, traintarget, testtarget = train_test_split(X, y, test_size=0.2)
        model_dtc = DecisionTreeClassifier() # 确定决策树参数
        model_dtc.fit(traindata, traintarget) # 拟合数据

        # 预测测试集结果
        testtarget_pre = model_dtc.predict(testdata)

        # 结果展示
        st.write("预测结果准确率为：", accuracy_score(testtarget, testtarget_pre))

        # 绘制混淆矩阵
        cm = confusion_matrix(testtarget, testtarget_pre)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", ax=ax)
        plt.ylabel('实际值')
        plt.xlabel('预测值')
        st.pyplot(fig)

        # 绘制预测数值和真实值的折线图
        fig2, ax2 = plt.subplots()
        ax2.plot(testtarget.values[:20], label='实际值', marker='o')
        ax2.plot(testtarget_pre[:20], label='预测值', marker='x')
        plt.title('预测值与实际值对比')
        plt.ylabel('值')
        plt.xlabel('样本')
        plt.legend()
        st.pyplot(fig2)

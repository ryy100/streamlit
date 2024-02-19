import streamlit as st
import leancloud
import hashlib
import script_name
import io
import home_page
import frequency_distribution_page
import pie_bar_chart_page
import decision_tree_page
import Classroom_system
# import face_page
# LeanCloud 初始化
# LeanCloud 初始化
leancloud.init(st.secrets["ID"], st.secrets["key"])

# 自定义样式
def custom_css():
    st.markdown("""
        <style>
            .main { background-color: #adfadf; }
            .stButton>button { width: 100%; }
            .stTextInput>div>div>input { padding: 10px; }
            .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; text-align: center; padding: 10px; }
        </style>
        """, unsafe_allow_html=True)

# 学生用户类
class Student(leancloud.Object):
    pass

# 文件存储类
class Course1Files(leancloud.Object):
    pass

class Course2Files(leancloud.Object):
    pass

class Course3Files(leancloud.Object):
    pass

class Course4Files(leancloud.Object):
    pass

# 注册学生
def register_student(username, password):
    new_student = Student()
    new_student.set('username', username)
    new_student.set('password', password)  # 存储明文密码（注意：实际应用中应使用哈希密码）
    try:
        new_student.save()
        return True
    except leancloud.LeanCloudError as e:
        st.error(f"注册失败: {e}")
        return False

# 验证学生
def verify_student(username, password):
    query = Student.query
    query.equal_to('username', username)
    try:
        student = query.first()
        return student.get('password') == password  # 直接比较明文密码
    except leancloud.LeanCloudError:
        return False

# 显示登录或注册页面
def login_or_register_page():
    st.title('🌍 学生文件上传系统')
    choice = st.radio("选择操作", ['登录', '注册'])

    username = st.text_input("用户名", key='username')
    password = st.text_input("密码", type='password', key='password')

    if choice == '登录':
        if st.button("登录"):
            if verify_student(username, password):
                st.session_state['logged_in'] = True
                st.session_state['student_name'] = username
                st.experimental_rerun()
            else:
                st.error("用户名或密码错误")
    elif choice == '注册':
        if st.button("注册"):
            if register_student(username, password):
                st.success("注册成功，请登录")
                st.session_state['logged_in'] = False

# 初始化页面配置
st.set_page_config(page_title="数据分析", page_icon=":tiger:", layout="wide")

# 定义页面
PAGES = {
    "主页": home_page,
    "文件上传": script_name,
    "频率分布图": frequency_distribution_page,
    "饼状图和直方图": pie_bar_chart_page,
    "决策树": decision_tree_page,
    "在线选座":Classroom_system,
    # "人脸识别打卡":face_page,
}

# 初始登录状态
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 根据登录状态决定显示内容
if not st.session_state['logged_in']:
    login_or_register_page()
else:
    st.sidebar.title('导航')
    selection = st.sidebar.selectbox("去往", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

import streamlit as st
import leancloud
import io

# 假设这里是 LeanCloud 的初始化代码
# leancloud.init("your_app_id", "your_app_key")

# 文件上传和显示文件的页面函数
def app():
    st.title('文件上传')

    # 获取当前登录学生的用户名，这里用一个固定的示例值代替
    username = st.session_state.get('student_name', '默认学生名')

    # 选择课程
    st.subheader("选择课程")
    courses = ["Python语言程序设计及医学应用", "临床大数据挖掘与分析", "实时数据分析", "数据仓库与数据挖掘实务"]
    course_columns = st.columns(len(courses))  # 为每个课程创建一个列

    # 初始化选择的课程
    if 'selected_course' not in st.session_state:
        st.session_state['selected_course'] = "Python语言程序设计及医学应用"  # 默认选择课程1

    # 为每个课程创建一个按钮
    for i, course in enumerate(courses):
        with course_columns[i]:
            if st.button(course):
                st.session_state['selected_course'] = course

    # 显示当前选择的课程
    selected_course = st.session_state['selected_course']
    st.write(f"您选择了: {selected_course}")

    # 根据选定的课程选择对应的数据库
    database_map = {
        "Python语言程序设计及医学应用": "Course1Files",
        "临床大数据挖掘与分析": "Course2Files",
        "实时数据分析": "Course3Files",
        "数据仓库与数据挖掘实务": "Course4Files"
    }
    database_name = database_map.get(selected_course, "Course1Files")  # 默认为 Course1Files

    # 文件上传逻辑
    uploader_key = f"file_uploader_{selected_course}"
    uploaded_files = st.file_uploader("上传文件", accept_multiple_files=True, type=["pdf", "docx", "doc"],
                                          key=uploader_key)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                file_data = uploaded_file.getvalue()
                lc_file = leancloud.File(uploaded_file.name, io.BytesIO(file_data))
                lc_file.save()

                user_file = leancloud.Object.extend(database_name)()
                user_file.set('username', username)
                user_file.set('file', lc_file)
                user_file.set('state', True)
                user_file.save()
                st.success(f"文件 '{uploaded_file.name}' 上传成功！")
            except Exception as e:
                st.error(f"文件上传失败：{e}")

    # 显示当前用户上传的文件
    with st.container():
        st.subheader("已上传的文件")
        try:
            query = leancloud.Query(database_name)
            query.equal_to('username', username)
            files = query.find()
            if files:
                for file in files:
                    with st.container():
                        lc_file = file.get('file')
                        file_name = lc_file.name
                        file_url = lc_file.url
                        # 文件信息和下载按钮
                        st.markdown(f"""
                                <div style="margin: 10px 0; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                                    <h4>{file_name}</h4>
                                    <a href="{file_url}" target="_blank">下载</a>
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.write("无文件")
        except Exception as e:
            st.error("加载文件失败：{e}")
    # 文件修改提醒
    with st.container():
        try:
            modified_files = []  # 存储已被修改的文件名称
            if files:
                for file in files:
                    # 检查文件是否被修改
                    if not file.get('state'):
                        modified_files.append(file.get('file').name)

                    if modified_files:
                        st.warning("以下文件已被修改：")
                        for file_name in modified_files:
                            st.markdown(f'<div class="file-box" style="color: red;">⚠️ {file_name}</div>',
                                            unsafe_allow_html=True)
                            # st.write(f"⚠️ {file_name}")
                    else:
                        st.write("没有文件被修改。")
        except Exception as e:
                st.error("检查文件修改状态时出错")



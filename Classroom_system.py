import streamlit as st
import leancloud
from datetime import datetime, timedelta
from leancloud import Object, Query,LeanCloudError
import pandas as pd

# 定义“教室”模型
class Classroom(Object):
    pass

# 定义“预约”模型
class Booking(Object):
    pass

# 初始化LeanCloud（请替换为您的应用ID和Key）
def init_leancloud():
    leancloud.init("q62BpC06IhG9jDS6ujh12Swb-gzGzoHsz", "c9Y3b6v3A2nFrPkJNtAIcTd2")


# 生成未来三天的日期列表
def get_next_three_days():
    today = datetime.now()
    return [today + timedelta(days=i) for i in range(3)]

# 获取预约数据
def get_bookings():
    bookings_query = Query(Booking)
    bookings = bookings_query.find()
    booked_slots = {(b.get("date"), b.get("time"), b.get("classroom_name")): True for b in bookings}
    return booked_slots

# 构建并填充预约状态表
def build_booking_table(booked_slots):
    dates = [date.strftime("%Y-%m-%d") for date in get_next_three_days()]
    time_slots = ["8:00-10:00", "12:00-14:00", "18:00-21:00"]
    classrooms = ["西301", "西202"]

    all_rows = []
    for time_slot in time_slots:
        for classroom in classrooms:
            row = {'时间段': time_slot, '教室': classroom}
            for date in dates:
                key = (date, time_slot, classroom)
                is_booked = booked_slots.get(key, False)
                color = "red" if is_booked else "gray"
                row[date] = f"<span style='color: {color};'>{'已预约' if is_booked else '未预约'}</span>"
            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    return df.to_html(escape=False, index=False)

# 检查教室是否已被预订
def is_booked(classroom_name, selected_date, selected_time):
    query = Query(Booking)
    query.equal_to("classroom_name", classroom_name)
    query.equal_to("date", selected_date.strftime("%Y-%m-%d"))
    query.equal_to("time", selected_time)
    try:
        return query.first() is not None
    except LeanCloudError as e:
        if e.code == 101:  # 对象未找到错误
            return False  # 未找到预约记录，故未被预订
        else:
            raise  # 其他错误重新抛出

# 提交预约
def submit_booking(classroom_name, selected_date, selected_time, name, student_id):
    if is_booked(classroom_name, selected_date, selected_time):
        return False
    else:
        booking = Booking()
        booking.set("classroom_name", classroom_name)
        booking.set("date", selected_date.strftime("%Y-%m-%d"))
        booking.set("time", selected_time)
        booking.set("name", name)
        booking.set("student_id", student_id)
        booking.save()
        return True

# Streamlit界面
def app():
    init_leancloud()

    st.title("教室预约系统")
    # 展示预约情况
    st.subheader("预约情况")
    booked_slots = get_bookings()
    booking_table_html = build_booking_table(booked_slots)
    st.markdown(booking_table_html, unsafe_allow_html=True)

    # 固定的教室和时间选项
    classrooms = ["西301", "西202"]
    time_slots = ["8:00-10:00", "12:00-14:00", "18:00-21:00"]
    dates = get_next_three_days()

    selected_classroom = st.selectbox("选择教室", classrooms)
    selected_date = st.selectbox("选择日期", dates, format_func=lambda d: d.strftime("%Y-%m-%d"))
    selected_time = st.selectbox("选择时间段", time_slots)
    name = st.text_input("输入姓名")
    student_id = st.text_input("输入学号")

    if st.button("预约"):
        if submit_booking(selected_classroom, selected_date, selected_time, name, student_id):
            st.success("预约成功！")
        else:
            st.error("该时间已被预订，请选择其他时间。")



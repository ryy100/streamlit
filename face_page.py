#
# 人脸比对 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret以及图片路径
# 运行方法：直接运行 main 即可
# 结果： 控制台输出结果信息
#
# 接口文档（必看）：https://www.xfyun.cn/doc/face/xffaceComparisonRecg/API.html
import leancloud
import streamlit as st
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import os
import traceback
import json
import requests
import cv2

# leancloud.init(st.secrets["ID"], st.secrets["key"])
class PunchCard(leancloud.Object):
    pass

class StudentProfile(leancloud.Object):
    pass


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass

# 进行sha256加密和base64编码
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)

def gen_body(appid, img1_data, img2_url, server_id):
    # with open(img1_path, 'rb') as f:
    #     img1_data = f.read()
    # with open(img2_path, 'rb') as f:
    response = requests.get(img2_url)
    if response.status_code != 200:
        raise Exception("无法下载图像")
    img2_data = response.content
    body = {
        "header": {
            "app_id": appid,
            "status": 3
        },
        "parameter": {
            server_id: {
                "service_kind": "face_compare",
                "face_compare_result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "input1": {
                "encoding": "jpg",
                "status": 3,
                "image": str(base64.b64encode(img1_data), 'utf-8')
            },
            "input2": {
                "encoding": "jpg",
                "status": 3,
                "image": str(base64.b64encode(img2_data), 'utf-8')
            }
        }
    }
    return json.dumps(body)

def capture_image_from_camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        # 将图像转换为JPEG格式并返回字节数据
        retval, buffer = cv2.imencode('.jpg', frame)
        st.image(frame, channels="BGR", caption="捕获的图像")
        return buffer.tobytes()
    return None



def store_image_in_database(username, image_data):
    """
    将图像存储到 LeanCloud 数据库中。
    """
    try:
        current_time = datetime.now()
        image_file = leancloud.File(username + "_punch_card.jpg", image_data)
        punch_card_image = PunchCard()
        punch_card_image.set("username", username)
        punch_card_image.set("image", image_file)
        punch_card_image.set('time', current_time)
        punch_card_image.save()
    except Exception as e:
        st.error("图像存储失败：" + str(e))


def get_student_image_path(username):
    """
    根据用户名从 LeanCloud 获取学生的图像路径。
    """
    query = StudentProfile.query.equal_to("username", username)
    try:
        student_profile = query.first()
        if student_profile:
            image_file = student_profile.get("image_file")
            return image_file.url if image_file else None
    except leancloud.LeanCloudError as e:
        print("获取学生图像路径失败：", str(e))
    return None



def run(appid, apikey, apisecret, img1_path, img2_path, server_id='s67c9c78c'):
    url = 'http://api.xf-yun.com/v1/private/{}'.format(server_id)
    request_url = assemble_ws_auth_url(url, "POST", apikey, apisecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': appid}
    response = requests.post(request_url, data=gen_body(appid, img1_path, img2_path, server_id), headers=headers)
    resp_data = json.loads(response.content.decode('utf-8'))
    return (base64.b64decode(resp_data['payload']['face_compare_result']['text']).decode())



appid = st.secrets["appid"]
apisecret = st.secrets["api_secret"]
apikey = st.secrets["api_key"]

def app():
    # Streamlit 应用界面
    st.title('在线打卡系统')

    with st.form("my_form"):
        username = st.text_input("用户名")
        submitted = st.form_submit_button("打卡")

        if submitted:
            img1_bytes = capture_image_from_camera()
            if img1_bytes:
                # 从 LeanCloud 获取比对图像路径

                student_image_path = get_student_image_path(username)
                if student_image_path:
                    # 执行人脸比对
                    response = run(appid, apikey, apisecret, img1_bytes, student_image_path)
                    # print(response)
                    response_dict = json.loads(response)
                    score = response_dict.get("score", 0)
                    if score > 0.7:
                        # 记录打卡时间
                        try:
                            store_image_in_database(username, img1_bytes)
                            st.success("打卡成功！")
                        except Exception as e:
                            st.error("打卡失败：" + str(e))
                    else:
                        st.error("人脸不匹配，打卡失败。")
                else:
                    st.error("找不到学生的图片。")

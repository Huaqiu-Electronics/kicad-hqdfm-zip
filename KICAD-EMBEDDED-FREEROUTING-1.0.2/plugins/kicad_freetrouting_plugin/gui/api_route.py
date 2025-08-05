import requests
import json
import wx
import time
from requests.exceptions import Timeout, RequestException

TIMEOUT = 20

class Response:
    status_code: int = 400

class ApiRoute:
    def __init__(self, m_gauge, base_url = "http://192.168.50.103:37864" ):
        self.m_gauge = m_gauge
        
        self.base_url = base_url
        self.headers = {
            "Freerouting-Profile-ID": "d0071163-7ba3-46b3-b3af-bc2ebfd4d1a0",
            "Freerouting-Profile-Email": "1023861154@qq.com",
            "Freerouting-Environment-Host": "PostmanRuntime/7.44.0",
            "Content-Type": "application/json"
        }

    def create_session(self):
        url = f"{self.base_url}/v1/sessions/create"
        # # response = self.get_request(url)
        # response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
        # self.m_gauge.SetValue(10)
        # # if response.status_code == 200:
        # #     return response.json().get('sessionId')
        # # else:
        # #     self.report_error("Failed to create session")
        # #     return "False"
        try:
            # 发送 GET 请求
            self.m_gauge.SetValue(10)
            response = requests.post(url, headers=self.headers, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            # wx.MessageBox(f"{response.status_code}")
            if response.status_code == 200:
                content = json.loads(response.text)
                job_id = content["id"]
                return job_id
            else:
                self.report_error(_("Failed to create session"))
                return "False"
        except RequestException as e:
            self.report_error(_(f"Failed to create session：{e}"))
            return "False"
        except Exception as e:
            self.report_error(_(f"Failed to create session：{e}"))
            return "False"


    def enqueue_job(self, session_id, filename):
        url = f"{self.base_url}/v1/jobs/enqueue"
        data = {
            "session_id": session_id,
            "name": filename,
            "priority": "NORMAL"
        }
        try:
            # 发送 GET 请求
            response = requests.post(url, headers=self.headers, json=data, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            self.m_gauge.SetValue(15)
            # wx.MessageBox(f"{response.status_code}")
            if response.status_code == 200:
                content = json.loads(response.text)
                job_id = content["id"]
                return job_id
            else:
                self.report_error(_("Failed to enqueue job"))
                return "False"
        except RequestException as e:
            self.report_error(_(f"Failed to enqueue job：{e}"))
            return "False"
        except Exception as e:
            self.report_error(_(f"Failed to enqueue job：{e}"))
            return "False"
        
        # response = self.post_request(url, data)
        # self.m_gauge.SetValue(15)
        # if response.status_code == 200:
        #     content = json.loads(response.text)
        #     job_id = content["id"]
        #     return job_id
        # else:
        #     self.report_error("Failed to enqueue job")
        #     return "False"



    def settings_job( self, job_id ):
        url = f"{self.base_url}/v1/jobs/{job_id}/settings"
        input_data = {
            "max_passes": 5,
            "via_costs": 1000
            }
        response = self.post_request(url, input_data)
        self.m_gauge.SetValue(16)
        if response.status_code != 200:
            self.report_error(_("Failed to upload input"))
            return "False"



    def upload_input(self, job_id, filename, data):
        url = f"{self.base_url}/v1/jobs/{job_id}/input"
        input_data = {
            "filename": filename,
            "data": data
        }
        response = self.post_request(url, input_data)
        self.m_gauge.SetValue(16)
        if response.status_code != 200:
            self.report_error(_("Failed to upload input"))
            return "False"

    def start_job(self, job_id):
        url = f"{self.base_url}/v1/jobs/{job_id}/start"
        response = self.put_request( url )
        self.m_gauge.SetValue(17)
        if response.status_code != 200:
            self.report_error("Failed to start job")
            return "False"

    def cancel_job(self, job_id):
        url = f"{self.base_url}/v1/jobs/{job_id}/cancel"
        response = self.put_request( url )
        self.m_gauge.SetValue(0)
        if response.status_code != 200:
            self.report_error(_( "Failed to start job"))
            return "False"

    # def get_job_status(self, job_id):
    #     url = f"{self.base_url}/v1/jobs/{job_id}"
    #     start_time = time.time()
    #     count = 3
    #     while True:
    #         response = self.get_request(url)
    #         if count < 10:
    #             self.m_gauge.SetValue(20 + count)
    #         if response.status_code == 200:
    #             content = json.loads(response.text)
    #             process_state = content["state"]
    #             print(f"Job {job_id} status: {process_state}")  # 打印当前状态
    #             if process_state == "COMPLETED":
    #                 return "True"
    #             count += 1
    #             time.sleep( count )
    #         else:
    #             self.report_error("Failed to get job status")
    #             return "False"



    def get_job_status(self, job_id):
        url = f"{self.base_url}/v1/jobs/{job_id}"
        response = self.get_request(url)
        if response.status_code == 200:
            content = json.loads(response.text)
            # process_state = content["state"]
            # print(f"Job {job_id} status: {process_state}")  # 打印当前状态
            
            return content
        else:
            self.report_error(_("Failed to get job status"))
            return "False"
    


    def get_job_output(self, job_id):
        url = f"{self.base_url}/v1/jobs/{job_id}/output"
        # response = self.get_request(url)
        # #self.m_gauge.SetValue(90)
        # if response.status_code == 200:
        #     content = json.loads(response.text)
        #     ses_data = content["data"]
        #     return ses_data
        # else:
        #     self.report_error("Failed to get job output")
        #     return "False"

        try:
            # 发送 GET 请求
            response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            # wx.MessageBox(f"{response.status_code}")
            if response.status_code == 200:
                content = json.loads(response.text)
                job_id = content["data"]
                # wx.MessageBox(f"{job_id}")
                return job_id
                
            else:
                self.report_error( _("Failed to get job output") )
                return "False"
        except RequestException as e:
            self.report_error(_(f"Failed to get job output：{e}"))
            return "False"
        except Exception as e:
            self.report_error(_(f"Failed to get job output：{e}"))
            return "False"



    def get_request(self, url ):
        try:
            # 发送 GET 请求
            response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            response.raise_for_status()
            return response
        except Timeout:
            print(f"请求超时：在 {self.timeout} 秒内未收到响应。")
            response = Response()
            return response
        except Exception as e:
            print(f"发生未知错误：{e}")
            response = Response()
            return response
        

    def post_request(self, url, data ):
        try:
            # 发送 GET 请求
            response = requests.post(url, headers=self.headers, json=data, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            response.raise_for_status()
            return response
        except Timeout:
            print(f"请求超时：在 {self.timeout} 秒内未收到响应。")
            response = Response()
            return response
        except Exception as e:
            print(f"发生未知错误：{e}")
            response = Response()
            return response
        
    def put_request(self, url ):
        try:
            # 发送 GET 请求
            response = requests.put(url, headers=self.headers, timeout=TIMEOUT)
            # 检查响应状态码是否为 200-299
            response.raise_for_status()
            return response
        except Timeout:
            print(f"请求超时：在 {self.timeout} 秒内未收到响应。")
            response = Response()
            return response
        except Exception as e:
            print(f"发生未知错误：{e}")
            response = Response()
            return response

    def report_error(self, reason):
        wx.MessageBox(
            _("Routing process failure:\r\n{reasons}\r\n").format(reasons=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        self.m_gauge.SetValue(0)


import base64

def file_to_base64(file_path):
    """
    将文件内容读取并转换为Base64格式
    :param file_path: 文件路径
    :return: Base64编码的字符串
    """
    try:
        with open(file_path, 'rb') as file:  # 以二进制模式打开文件
            file_content = file.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')  # 转换为Base64并解码为字符串
            return base64_content
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None

# 示例用法
if __name__ == "__main__":
    api = ApiRoute("http://192.168.50.103:37864")

    # 创建会话
    # session_id = api.create_session()
    # print(f"Session ID: {session_id}")

    session_id = "680b279a-b92f-4007-b07d-ab32e5131ec9"
    # 排队任务
    job_id = api.enqueue_job(session_id)
    if job_id is False:
        print(f"Job ID: {job_id}")

    # 上传输入数据
    filename = f"freerouting.dsn"
    base64_data = file_to_base64(filename)
    if base64_data:
        print("文件内容的Base64编码如下：")
    else:
        print("文件内容为空或无法读取。")
    api.upload_input(job_id, filename, base64_data)

    # 启动任务
    api.start_job(job_id)

    # 获取任务状态
    status = api.get_job_status(job_id)
    print(f"Job Status: {status}")

    # 获取任务输出
    output = api.get_job_output(job_id)
    print(f"Job Output: {output}")
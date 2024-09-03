import os

import requests
from requests_toolbelt import MultipartEncoder


def test_pip():
    print('Test Success')


def upload(token, file_lir_path, task_name=''):
    file_fail_name = []
    for file_path in os.listdir(file_lir_path):
        file_read_path = os.path.join(file_lir_path, file_path)
        with open(file_read_path, 'rb') as file:

            fields = {
                'user_id': token,
                'task_name': task_name,
                'file': (file.name, file, 'application/octet-stream')
            }
            m = MultipartEncoder(fields=fields)

            # 发送 POST 请求
            headers = {'Content-Type': m.content_type}
            response = requests.post('http://192.168.8.21:8087/api/api/upload', data=m, headers=headers)
            if response.status_code != 200:
                file_fail_name.append(file_path)
    return file_fail_name


def parser(token: str, file_name: str, task_name='') -> dict:
    API_ENDPOINT = "http://192.168.8.21:8087/api/api/task_return_list"
    data = {
        'user_id': token,
        'task_name': task_name,
        'fileName': file_name  # 根据你的接口定义，文件名参数应该是 fileName
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}












import requests

def add_todo_list(headers, list_name):
    """
    添加新的 To Do 列表。
    
    :param headers: 包含认证信息的请求头
    :param list_name: 新列表的名称
    :return: 新创建的 To Do 列表信息或错误信息
    """
    url = "https://graph.microsoft.com/v1.0/me/todo/lists"
    payload = {
        "displayName": list_name
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return response.json()  # 返回新创建的列表信息
    else:
        raise RuntimeError(f"添加 To Do 列表失败: {response.status_code} - {response.text}")
import requests

def get_todo_list(headers) -> list:
    """
    获取用户的 To Do 列表。
    
    :param headers: 包含认证信息的请求头
    :return: To Do 列表或错误信息
    """
    url = "https://graph.microsoft.com/v1.0/me/todo/lists"
    response = requests.get(url, headers=headers)

    try:
        if response.status_code == 200:
            todo_lists = response.json().get('value', [])
            return [ {'displayName' : todo_list['displayName'], 'id' : todo_list['id']} for todo_list in todo_lists ]
    except Exception as e:
        raise RuntimeError(f"获取 To Do 列表时发生错误: {e}")
    
    return []
import requests

def get_todo_task(headers, todo_list_id) -> list:
    """
    获取指定 To Do 列表中的任务。
    
    :param headers: 包含认证信息的请求头
    :param todo_list_id: To Do 列表的 ID
    :return: 任务列表或错误信息
    """
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{todo_list_id}/tasks"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tasks = response.json().get('value', [])
        return tasks
    else:
        return []



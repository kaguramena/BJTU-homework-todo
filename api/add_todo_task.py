import requests
from typing import Literal

def add_todo_task(headers, todo_list_id, task_title,status = Literal[ "notStarted","inProgress","completed","waitingOnOthers","deferred"],created_datetime = None,linked_resources = None, due_date = None, importance = None):
    """
    添加新的 To Do 任务到指定列表。
    
    :param headers: 包含认证信息的请求头
    :param todo_list_id: To Do 列表的 ID
    :param task_title: 任务的标题
    :param due_date: 任务的截止日期（可选）
    :param importance: 任务的重要性（可选，值为 "low", "normal", "high"）
    :return: 新创建的任务信息或错误信息
    """

    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{todo_list_id}/tasks"
    payload = {
        "title": task_title,
        "status": status
    }
    
    if due_date:
        payload["dueDateTime"] = {
            "dateTime": due_date,
            "timeZone": "UTC + 8"  # 可以根据需要调整时区
        }
    
    if importance:
        payload["importance"] = importance

    if created_datetime:
        payload["createdDateTime"] = created_datetime

    if linked_resources:
        payload["linkedResources"] = linked_resources

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return response.json()  # 返回新创建的任务信息
    else:
        raise RuntimeError(f"添加 To Do 任务失败: {response.status_code} - {response.text}")

import msal
import requests
import os
import configparser
from api.get_todo_task import get_todo_task
from api.get_todo_list import get_todo_list
from api.add_todo_list import add_todo_list
from api.add_todo_task import add_todo_task
from GetHW.gethw import get_homework
import argparse
import json


def process(add_homework = False):
    # --- 配置 ---
    config = configparser.ConfigParser()
    config.read('config.cfg')

    # 使用 'common' 终结点来支持个人账户和多租户
    TENANT_ID = 'consumers'
    CLIENT_ID = config['azure']['clientId']
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPE = ["User.Read", "Tasks.ReadWrite"]
    TOKEN_CACHE_FILE = "msal_token_cache.json"
    save_path = config['gethw']['savePath']
    hw_json_file = config['gethw']['jsonFile']
    hw_json = json.load(open(os.path.join(save_path, hw_json_file), "r", encoding="utf-8"))

    # --- MSAL 令牌缓存处理 ---
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        cache.deserialize(open(TOKEN_CACHE_FILE, "r").read())

    # --- 初始化 MSAL 应用并绑定缓存 ---
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

    # --- 获取令牌 ---
    result = None
    accounts = app.get_accounts()

    if accounts:
        print("找到了已缓存的账户，尝试静默获取令牌...")
        result = app.acquire_token_silent(SCOPE, account=accounts[0])

    if not result:
        print("缓存中无有效令牌，启动设备代码流进行认证...")
        flow = app.initiate_device_flow(scopes=SCOPE)
        if "user_code" not in flow:
            raise ValueError("获取设备代码失败。请检查应用注册和权限配置。")
        
        print(flow["message"]) # 显示 URL 和用户代码
        result = app.acquire_token_by_device_flow(flow)

    # --- 处理结果并调用 API ---
    if "access_token" in result:
        # 令牌获取成功后，立即保存缓存状态
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())
        
        access_token = result['access_token']
        print("\n令牌获取成功!")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # 调用 /me API 获取用户信息
        me_url = "https://graph.microsoft.com/v1.0/me"
        me_response = requests.get(me_url, headers=headers)
        print(me_response.status_code)
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"成功以 {user_data.get('userPrincipalName')} 的身份登录。")

            # 调用 To Do API
            todo_lists : list = get_todo_list(headers)
            for todo_list in todo_lists:
                display_name = todo_list.get('displayName')
                todo_list_id = todo_list.get('id')
                print(f" - 列表名称: {display_name}, ID: {todo_list_id}")
                for task in get_todo_task(headers, todo_list_id):
                    print(f"   - 任务: {task.get('title')}, 状态: {task.get('status')}")
                if add_homework:
                    if display_name == "homework":
                        xq_code = config['gethw']['xqCode']
                        student_id = config['gethw']['studentId']
                        homework_lists = get_homework(xq_code,student_id)
                        for course, homeworks in homework_lists.items():
                            for homework in homeworks:
                                if str(homework['id']) in hw_json:
                                    continue
                                hw_json[homework['id']] = True
                                add_todo_task(headers,todo_list_id,f"{course} - {homework['title']}","inProgress",created_datetime=homework['openDate'],due_date=homework['endTime'],importance="high")
                    with open(os.path.join(save_path, hw_json_file), "w", encoding="utf-8") as f:
                        json.dump(hw_json, f, ensure_ascii=False, indent=4)
                        print(f"已将作业信息保存到 {os.path.join(save_path, hw_json_file)}")
        else:
            print(f"获取 '/me' 信息失败: {me_response.status_code} - {me_response.text}")

    else:
        print("\n认证失败:")
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Microsoft To Do CLI")
    parser.add_argument('-a','--add-homework', action = "store_true", help='Update Homework List')
    args = parser.parse_args()
    add_homework = False
    if args.add_homework:
        add_homework = True
    process(add_homework)




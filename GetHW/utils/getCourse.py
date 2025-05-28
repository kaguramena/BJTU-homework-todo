import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_course_url(course):
    """
    构造访问特定课程的URL
    :param course: 课程字典
    :return: 完整的课程URL
    """
    base_url = "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml"
    params = {
        "method": "toCoursePlatform",
        "courseToPage": "10460",  # 课程作业为 10460 ， 课程 实验为 10461
        "courseId": course["course_num"],
        "dataSource": "1",
        "cId": course["id"],
        "xkhId": course["fz_id"],
        "xqCode": course["xq_code"],
        "teacherId": course["teacher_id"]
    }
    return f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

def access_course(course_url, jsessionid):
    """
    访问特定课程页面
    :param course_url: 课程URL
    :param jsessionid: JSESSIONID
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    cookies = {
        "JSESSIONID": jsessionid
    }
    response = requests.get(course_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        print(f"成功访问课程页面")
        return response.text
        # 可以进一步解析HTML内容
    else:
        print(f"访问课程页面失败，状态码：{response.status_code}")
        return None

def get_homework_list(course_id, xq_code, jsessionid):
    """
    获取作业列表
    :param course_id: 课程编号
    :param xq_code: 学期代码
    :param jsessionid: JSESSIONID
    :return: 作业列表
    """
    api_url = "http://123.121.147.7:88/ve/back/coursePlatform/homeWork.shtml"
    params = {
        "method": "getHomeWorkList",
        "cId": course_id,
        "xqCode": xq_code,
        "subType":0,
        "page": 1,
        "pagesize": 10
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    cookies = {
        "JSESSIONID": jsessionid
    }

    response = requests.get(api_url, params=params, headers=headers, cookies=cookies)
    homework_list = []
    if response.status_code == 200:
        data = response.json()
        if data.get("STATUS") == "0" and data.get("courseNoteList"):
            for homework in data["courseNoteList"]:
                if homework.get("subStatus") == '已提交':
                    continue
                open_date = datetime.strptime(homework.get("open_date"), "%Y-%m-%d %H:%M")
                open_data = open_date.strftime("%Y-%m-%dT%H:%M:%SZ")

                end_data = datetime.strptime(homework.get("end_time"), "%Y-%m-%d %H:%M")
                end_data = end_data.strftime("%Y-%m-%dT%H:%M:%SZ")
                homework_info = {
                    "id":homework.get("id"),
                    "title": homework.get("title"),
                    #"content": homework.get("content"),
                    "openDate": open_data,
                    "endTime": end_data,
                }
                homework_list.append(homework_info)
            return homework_list
        else:
            return []
    else:
        print(f"Failed to retrieve homework list. Status code: {response.status_code}")
        return []
    
def get_lab_list(course_id, xq_code, jsessionid):
    """
    获取作业列表
    :param course_id: 课程编号
    :param xq_code: 学期代码
    :param jsessionid: JSESSIONID
    :return: 作业列表
    """
    api_url = "http://123.121.147.7:88/ve/back/coursePlatform/homeWork.shtml"
    params = {
        "method": "getHomeWorkList",
        "cId": course_id,
        "xqCode": xq_code,
        "subType":2,
        "page": 1,
        "pagesize": 10
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    cookies = {
        "JSESSIONID": jsessionid
    }

    response = requests.get(api_url, params=params, headers=headers, cookies=cookies)
    homework_list = []
    if response.status_code == 200:
        data = response.json()
        if data.get("STATUS") == "0" and data.get("courseNoteList"):
            for homework in data["courseNoteList"]:
                if homework.get("subStatus") == '已提交':
                    continue
                open_date = datetime.strptime(homework.get("open_date"), "%Y-%m-%d %H:%M")
                open_data = open_date.strftime("%Y-%m-%dT%H:%M:%SZ")

                end_data = datetime.strptime(homework.get("end_time"), "%Y-%m-%d %H:%M")
                end_data = end_data.strftime("%Y-%m-%dT%H:%M:%SZ")
                homework_info = {
                    "id":homework.get("id"),
                    "title": homework.get("title"),
                    #"content": homework.get("content"),
                    "openDate": open_data,
                    "endTime": end_data,
                }
                homework_list.append(homework_info)
            return homework_list
        else:
            return []
    else:
        print(f"Failed to retrieve homework list. Status code: {response.status_code}")
        return []
import requests
def get_course_list(xq_code, jsessionid):
    """
    获取课程列表
    :param xq_code: 学期代码，例如 "2024202502"
    :param jsessionid: JSESSIONID，用于维持登录状态
    :return: 课程列表
    """
    # API接口URL
    api_url = "http://123.121.147.7:88/ve/back/coursePlatform/course.shtml"

    # 请求参数
    params = {
        "method": "getCourseList",
        "pagesize": 100,
        "page": 1,
        "xqCode": xq_code
    }

    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    # 设置Cookie，携带JSESSIONID
    cookies = {
        "JSESSIONID": jsessionid
    }

    # 发起请求
    response = requests.get(api_url, params=params, headers=headers, cookies=cookies)

    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        if data.get("STATUS") == "0" and data.get("courseList"):
            courses = data["courseList"]
            return courses
        else:
            print("No courses found.")
            return []
    else:
        print(f"Failed to retrieve the course list. Status code: {response.status_code}")
        return []
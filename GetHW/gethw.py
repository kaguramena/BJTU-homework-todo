from GetHW.utils.getCourseList import get_course_list
from GetHW.utils.getCourse import get_homework_list, get_lab_list
from GetHW.utils.update_cookie import get_cookie
import json
import configparser


def get_homework(xq_code,student_id):
    jsessionid = get_cookie(student_id)

    courses = get_course_list(xq_code, jsessionid)
    homework_json = {}
    for course in courses:
        homework_list = get_homework_list(course['id'],xq_code,jsessionid)
        lab_list = get_lab_list(course['id'],xq_code,jsessionid)
        homework_list =  homework_list + lab_list
        if not homework_list:
            continue
        homework_json[course['name']] = homework_list
    return homework_json

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")
    xq_code = config['gethw']['xqCode']
    student_id = config['gethw']['studentId']
    homework_data = get_homework(xq_code,student_id)
    print(homework_data)
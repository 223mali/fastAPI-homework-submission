from os import getcwd
import datetime

project_root_dir = getcwd()

teacher_data = {

    "first_name": "Test",
    "last_name": "User",
    "password": "123456",
    "email": "test2@mail.com",
    "role": "Teacher"

}


def convert_date(date_text, format: str = '%d-%m-%Y'):
    try:
        return datetime.datetime.strptime(date_text, format)
    except ValueError:
        return False

# coding:utf8
# import django.core.files
# import django.core.files.uploadedfile
from django.core.files.storage import *
import os

def handle_uploaded_case(f, project_id, case_id):
    # print(f.name)
    suffix = '.'+f.name.split('.')[1]
    project_id = str(project_id)
    case_id = str(case_id)
    file = FileSystemStorage()
    base = os.path.join(file.location, 'cases')
    # print(file.location)
    project_base = os.path.join(base, project_id)
    if not os.path.exists(project_base):
        os.mkdir(os.path.join(base, project_id))
    file = FileSystemStorage(location=project_base)
    if file.exists(case_id+suffix):
        file.delete(case_id + suffix)
    with file.open(case_id+suffix, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    file_path = os.path.join(project_id, case_id+suffix)
    # print(file_path)
    return file_path



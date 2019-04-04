# coding:utf8
import os, time
from django.conf import settings
from .models import *
from TestCore.Main import *
from datasource.models import *
from testcase.models import *

def runcase(testplan_id, case, case_path, case_sheet, ds_path=None, ds_sheet=None, ds_range=None):
    testplan = TestPlan.objects.get(id=testplan_id)
    log_base = os.path.join(settings.MEDIA_ROOT, 'log')
    if not os.path.isdir(log_base):
        os.mkdir(log_base)
    project_log_base = os.path.join(log_base, str(testplan.project_id))
    if not os.path.isdir(project_log_base):
        os.mkdir(project_log_base)
    log_time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    log_name = str(testplan.project_id)+ '_' + str(testplan.id) + '_' + log_time_stamp + '.txt'
    log_path = os.path.join(project_log_base, log_name)
    thd = MainThread(log_path,
                     case_path,
                     case_sheet,
                     ds_path=ds_path,
                     ds_sheet=ds_sheet,
                     rg=ds_range)
    beg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    thd.start()
    thd.join()
    res = thd.get_res()
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lg_path = os.path.join(str(testplan.project_id), log_name)
    his = TP_Run_His(
        testplan=testplan,
        case=case,
        beg_time=beg_time,
        end_time=end_time,
        log_path= lg_path
    )
    his.save()
    result = 'PASS'
    for r in res:
        if r[3].find('FAIL') != -1:
            result = r[3]
        detail = TP_Run_Detail(
            his=his,
            ds_order=r[0],
            beg_time=r[1],
            end_time=r[2],
            result=r[3]
        )
        detail.save()
    his.result = result
    his.save()
    testplan.status = '已结束'
    testplan.save()

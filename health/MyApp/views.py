import datetime
import hashlib

from django.core.mail import message
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render
from MyApp.models import*
from django.contrib import messages
final_n= None
final_d=None
request_time=""
#登录
def hash_code(s,salt='MyApp'):
    h=hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def manager_login(request):
    global  manager_tel
    user_telephone = request.GET.get("user_telephone")
    user_password = request.GET.get("user_password")
    user_result = user.objects.filter(user_telephone=user_telephone)
    context = {}
    if len(user_result) == 1:
        password = user_result[0].user_password
        identity = user_result[0].user_identity
        if user_password == password:
            if identity == "管理员":
                manager_tel=user_telephone
                return render(request, 'manager/manager_homepage.html')
            else:
                context["info"] = "身份错误，请检查您的身份后选择相应按钮！"
                context["status"] = 3
                return render(request, 'login.html', context=context)
        else:
            context["info"] = "密码错误，请确认密码后填写！"
            context["status"] = 2
            return render(request, 'login.html', context=context)
    else:
        context["info"] = "用户不存在，请确认用户名后填写！"
        context["status"] = 1
        return render(request, 'login.html', context=context)
def doctor_login(request):
    global doctor_tel,doctor_condition
    user_telephone = request.GET.get("user_telephone")
    user_password = request.GET.get("user_password")
    user_result = user.objects.filter(user_telephone=user_telephone)
    context = {}
    if len(user_result) == 1:
        password = user_result[0].user_password
        identity = user_result[0].user_identity
        if user_password == password:
            if identity == "医生":
                doctor_tel=user_telephone
                signal = doctor.objects.filter(doctor_telephone=user_telephone).first().doctor_condition
                if signal == "空闲":
                    a = message.objects.filter(message_receive=user_telephone, doctor_IsRead="未读")
                    b=appoint.objects.filter(doctor_telephone=user_telephone,doctor_IsRead="未读")
                    count = len(a)+len(b)
                    print(count)
                    if count != 0:
                        attention = 1
                    else:
                        attention = 0
                    return render(request, 'doctor/doctor_homepage.html', context={"signal1": 1, "signal2": 0, "attention":attention,"count":count})
                else:
                    a = message.objects.filter(message_receive=user_telephone, doctor_IsRead="未读")
                    b = appoint.objects.filter(doctor_telephone=user_telephone, doctor_IsRead="未读")
                    count = len(a) + len(b)
                    print(count)
                    if count != 0:
                        attention = 1
                    else:
                        attention = 0
                    doctor.objects.filter(doctor_telephone=doctor_tel).update(doctor_condition="忙碌")
                    return render(request, 'doctor/doctor_homepage.html', context={"signal1": 0, "signal2": 1,"attention":attention,"count":count })
            else:
                context["info"] = "身份错误，请检查您的身份后选择相应按钮！"
                context["status"] = 3
                return render(request, 'login.html', context=context)
        else:
            context["info"] = "密码错误，请确认密码后填写！"
            context["status"] = 2
            return render(request, 'login.html', context=context)
    else:
        context["info"] = "用户不存在，请确认用户名后填写！"
        context["status"] = 1
        return render(request, 'login.html', context=context)
def resident_login(request):
    global resident_tel
    user_telephone = request.GET.get("user_telephone")
    user_password = request.GET.get("user_password")
    user_result = user.objects.filter(user_telephone=user_telephone)
    context = {}
    if len(user_result) == 1:
        password = user_result[0].user_password
        identity = user_result[0].user_identity
        if user_password == password:
            if identity == "居民":
                resident_tel=user_telephone
                a=message.objects.filter(message_receive=user_telephone,resident_IsRead="未读")
                b=appoint.objects.filter(resident_telephone=user_telephone,resident_IsRead="未读")
                count = len(a)+len(b)
                if count !=0:
                    attention=1
                else:
                    attention=0
                return render(request, 'resident/resident_homepage.html',context={"count":count,"attention":attention,})
            else:
                context["info"] = "身份错误，请检查您的身份后选择相应按钮！"
                context["status"] = 3
                return render(request, 'login.html', context=context)
        else:
            context["info"] = "密码错误，请确认密码后填写！"
            context["status"] = 2
            return render(request, 'login.html', context=context)
    else:
        context["info"] = "用户不存在，请确认用户名后填写！"
        context["status"] = 1
        return render(request, 'login.html', context=context)
def doctor_register(request):
    user_telephone = request.GET.get("user_telephone")
    user_password = request.GET.get("user_password")
    user_result = user.objects.filter(user_telephone=user_telephone)
    if len(user_result) == 1:
        context = {
            "status": 1,
            "info": "用户已经存在，请重新选择用户名！"
        }
        return render(request, 'register.html', context=context)
    else:
        context={
            "status":4,
            "info":"注册成功！"
        }
        user.objects.create(user_telephone=user_telephone, user_password=user_password,
                            user_identity="医生")
        doctor.objects.create(doctor_telephone=user_telephone,doctor_condition="空闲")
        return render(request, 'login.html',context = context)
def resident_register(request):
    print(1)
    user_telephone = request.GET.get("user_telephone")
    print(user_telephone)
    user_password = request.GET.get("user_password")
    print(user_password)
    user_result = user.objects.filter(user_telephone=user_telephone)
    if len(user_result) == 1:
        context = {
            "status": 1,
            "info": "用户已经存在，请重新选择用户名！"
        }
        return render(request, 'register.html', context=context)
    else:
        context = {
            "status": 4,
            "info": "注册成功！"
        }
        user.objects.create(user_telephone=user_telephone, user_password=user_password,user_identity="居民")
        resident.objects.create(resident_name=user_telephone,resident_sex="",resident_age="",
                                resident_telephone=user_telephone,resident_address=" ",resident_condition="")
        return render(request, 'login.html', context=context)
#居民
def personal_info(request):
    global resident_tel
    if request.method == "GET":
        result=resident.objects.filter(resident_telephone=resident_tel).first()
        if result is None:
            return render(request, 'resident/personal_info.html')
        else:
            context = {
                "resident_name": result.resident_name,
                "resident_sex": result.resident_sex,
                "resident_age": result.resident_age,
                "resident_address": result.resident_address
            }
            return render(request,'resident/personal_info.html',context=context)
    else:
        resident_name = request.POST.get("resident_name")
        resident_sex = request.POST.get("resident_sex")
        resident_age = request.POST.get("resident_age")
        resident_address = request.POST.get("resident_address")
        result=resident.objects.filter(resident_telephone=resident_tel).first()
        if result is None:
            resident.objects.create(resident_name=resident_name,resident_sex=resident_sex,resident_age=resident_age,
                                resident_telephone=resident_tel,resident_address=resident_address,resident_condition="未签约")
        else:
            resident.objects.filter(resident_telephone=resident_tel).update(resident_name=resident_name, resident_sex=resident_sex, resident_age=resident_age,
                                    resident_telephone=resident_tel, resident_address=resident_address)
        context={
            "resident_name":resident_name,
            "resident_sex":resident_sex,
            "resident_age":resident_age,
            "resident_address":resident_address
        }
        return render(request,'resident/personal_info.html',context=context)
def calculate_BMI(request):
    global resident_tel
    if request.method == "GET":
        return render(request,'resident/calculate_BMI.html')
    else:
        weight=request.POST.get("weight")
        h=request.POST.get("height")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        height=float(h)/100
        r=resident.objects.filter(resident_telephone=resident_tel).first()
        if r is None:
            name=""
        else:
            name=r.resident_name
        num=float(weight)/(float(height)*float(height))
        result_num=round(num,1)
        if result_num<=18.4:
            result_condition="偏瘦"
        elif result_num<=23.9:
            result_condition="正常"
        elif result_num<=27.9:
            result_condition="过重"
        else:
            result_condition = "肥胖"
        Health_Report.objects.create(report_telephone=resident_tel,report_name=name,report_height=h,report_weight=weight,
        result_num=result_num,result_condition=result_condition,report_time=t)
        context={
            "result_num":result_num,
            "result_condition":result_condition,
            "weight":weight,
            "height":h,
            "status":1
        }
        return render(request,'resident/calculate_BMI.html',context=context)
def delete_report(request):
    global resident_tel,final_name
    if request.method == "GET":
        id = request.GET.get("report_id")
        Health_Report.objects.filter(id=id).delete()
        results = Health_Report.objects.filter(report_telephone=resident_tel, report_name=final_name)
        context = {
            "results": results,
            "name":final_name
        }
        return render(request,'resident/health_report.html',context=context)

def delete_family_report(request):
    global resident_tel, final_name
    if request.method == "GET":
        id = request.GET.get("report_id")
        Health_Report.objects.filter(id = id).delete( )
        results = Health_Report.objects.filter(report_telephone = resident_tel, report_name = final_name)
        context = {
            "results": results,
            "name": final_name
        }
        return render(request, 'resident/family_reports.html', context = context)
def health_reports(request):
    global resident_tel,f_name,final_name
    if request.method == "GET":
        result=resident.objects.filter(resident_telephone=resident_tel).first()
        if result is None:
            # return HttpResponse("请先完善居民信息！")
            return render(request,'resident/personal_info.html',context={"status":1})
        else:
            name=result.resident_name
            final_name=name
            results=Health_Report.objects.filter(report_telephone=resident_tel,report_name=name)
            context={
                "results":results,
                "name":name,
            }
            return render(request,'resident/health_report.html',context=context)
    else:
        results=Health_Report.objects.filter(report_telephone=resident_tel,report_name=f_name)
        final_name=f_name
        context = {
            "results": results,
            "name": f_name,
        }
        return render(request,'resident/family_reports.html',context=context)


def add_family(request):
    global resident_tel
    if request.method == "GET":
        return render(request,'resident/add_family.html')
    else:
        family_name = request.POST.get("family_name")
        family_age = request.POST.get("family_age")
        family_sex = request.POST.get("family_sex")
        family_relationship = request.POST.get("family_relationship")
        family_telephone=resident_tel
        family.objects.create(family_name=family_name,family_age=family_age,family_sex=family_sex,
        family_relationship=family_relationship, family_telephone=family_telephone)
        return render(request,'resident/add_family.html')
def search_family(request):
    global resident_tel
    if request.method == "GET":
        results=family.objects.filter(family_telephone=resident_tel)
        context = {
            "results": results
        }
        return render(request,'resident/search_family.html',context=context)
def delete_family(request):
    global resident_tel
    id=request.GET.get("family_id")
    family.objects.filter(id=id).delete()
    results = family.objects.filter(family_telephone=resident_tel)
    context = {
        "results": results
    }
    return render(request, 'resident/search_family.html', context=context)
def alter_family(request):
    global resident_tel
    if request.method == "GET":
        id = request.GET.get("f_id")
        result=family.objects.filter(id=id).first()
        context={
            "family_name":result.family_name,
            "family_sex":result.family_sex,
            "family_age":result.family_age,
            "family_relationship":result.family_relationship
        }
        return render(request, 'resident/family_info.html',context=context)
    else:
        family_name = request.POST.get("family_name")
        family_sex = request.POST.get("family_sex")
        family_age = request.POST.get("family_age")
        family_relationship = request.POST.get("family_relationship")
        family.objects.filter(family_telephone=resident_tel,family_name=family_name).update(family_name=family_name,
         family_sex=family_sex,family_age=family_age,family_relationship=family_relationship)
        context = {
            "family_name": family_name,
            "family_sex": family_sex,
            "family_age": family_age,
            "family_relationship": family_relationship
        }
        return render(request, 'resident/family_info.html',context=context)
def family_calculate(request):
    global resident_tel,f_name
    if request.method == "GET":
        id=request.GET.get("report_id")
        f=family.objects.filter(id=id).first()
        f_name=f.family_name
        return render(request,'resident/family_calculate.html')
    else:
        weight=request.POST.get("weight")
        h=request.POST.get("height")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        height=float(h)/100
        num=float(weight)/(float(height)*float(height))
        result_num=round(num,1)
        if result_num<=18.4:
            result_condition="偏瘦"
        elif result_num<=23.9:
            result_condition="正常"
        elif result_num<=27.9:
            result_condition="过重"
        else:
            result_condition = "肥胖"
        Health_Report.objects.create(report_telephone=resident_tel,report_name=f_name,report_height=h,report_weight=weight,
        result_num=result_num,result_condition=result_condition,report_time=t)
        context={
            "result_num":result_num,
            "result_condition":result_condition,
            "weight":weight,
            "height":h,
            "status":1
        }
        return render(request,'resident/family_calculate.html',context=context)
def search_doctor(request):
    global resident_tel, request_time
    if request.method == "GET":
        doctor_id = request.GET.get("doctor_id")
        d = doctor.objects.filter(id = doctor_id).first()
        d_tel=doctor.objects.filter(id=doctor_id).first().doctor_telephone
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        r = appoint.objects.filter(resident_telephone = resident_tel).first()
        c=resident.objects.filter(resident_telephone=resident_tel).first().resident_condition
        print(doctor_id)
        print(c)
        if r is None:
            appoint.objects.create(resident_telephone = resident_tel, doctor_telephone = d.doctor_telephone,
                                   resident_request_time = t, resident_appoint_time = request_time, doctor_IsRead = "未读",appoint_result="签约处理中",doctor_deal_time="无",)
            # doctor.objects.filter(doctor_telephone=d.doctor_telephone).update(doctor_condition="已签约")
            results = doctor.objects.all()
            context = {
                "results": results,
                "status":1,
                "doctor_telephone":d_tel,
                "resident_condition":c
            }
            return render(request, 'resident/search_doctor.html', context = context)
        else:
            appoint.objects.filter(resident_telephone=resident_tel).update(resident_appoint_time=request_time)
            doctor_tel=appoint.objects.filter(resident_telephone=resident_tel).first().doctor_telephone
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            results = doctor.objects.filter(doctor_condition = "空闲")
            context = {
                "results": results,
                "status":0,
                "doctor_telephone": doctor_tel,
                "resident_condition": c
            }
            return render(request, 'resident/search_doctor.html', context = context)
    else:
        try:
            doctor_tel = appoint.objects.filter(resident_telephone = resident_tel).first( ).doctor_telephone
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            results=doctor.objects.filter(doctor_condition="空闲")
            context={
                "results":results,
                "resident_condition": c,
                "doctor_telephone": doctor_tel,
            }
            return render(request,'resident/search_doctor.html',context = context)
        except AttributeError:
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            results = doctor.objects.filter(doctor_condition = "空闲")
            context = {
                "results": results,
                "resident_condition": c,
                "doctor_telephone": None,
            }
            return render(request, 'resident/search_doctor.html', context = context)


def search_d(request):
    global final_n, final_d,resident_tel
    if request.method == "GET":
        try:
            doctor_name = request.GET.get("doctor_name")
            doctors = doctor.objects.filter(doctor_name__icontains = doctor_name)
            doctor_tel = appoint.objects.filter(resident_telephone = resident_tel).first( ).doctor_telephone
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            print(doctor_tel)
            print(c)
            context = {
                "results": doctors,
                "resident_condition": c,
                "doctor_telephone": doctor_tel,
            }
            final_n = doctor_name
            return render(request, 'resident/search_doctor.html', context = context)
        except AttributeError:
            doctor_name = request.GET.get("doctor_name")
            doctors = doctor.objects.filter(doctor_name__icontains = doctor_name)
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            print(c)
            context = {
                "results": doctors,
                "resident_condition": c,
                "doctor_telephone": None,
            }
            final_n = doctor_name
            return render(request, 'resident/search_doctor.html', context = context)
    else:
        try:
            doctor_dept = request.POST.get("doctor_dept")
            doctors = doctor.objects.filter(doctor_dept__icontains = doctor_dept)
            doctor_tel = appoint.objects.filter(resident_telephone = resident_tel).first( ).doctor_telephone
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            context = {
                "results": doctors,
                "resident_condition": c,
                "doctor_telephone": doctor_tel,
            }
            final_d = doctor_dept
            return render(request, 'resident/search_doctor.html', context = context)
        except AttributeError:
            doctor_dept = request.POST.get("doctor_dept")
            doctors = doctor.objects.filter(doctor_dept__icontains = doctor_dept)
            c = resident.objects.filter(resident_telephone = resident_tel).first( ).resident_condition
            context = {
                "results": doctors,
                "resident_condition": c,
                "doctor_telephone": None,
            }
            final_d = doctor_dept
            return render(request, 'resident/search_doctor.html', context = context)
def appoint_doctor(request):
    global resident_tel,request_time,final_n,final_d
    if request.method == "GET":
        results=appoint.objects.filter(resident_telephone=resident_tel,appoint_result="签约成功")
        context = {
            "results": results
        }
        return render(request,'resident/appoint_doctor.html',context=context)
    else:
        request_time=request.POST.get("resident_appoint_time")
        appoint.objects.filter(resident_telephone=resident_tel).update(resident_appoint_time=request_time)
        results = doctor.objects.filter(doctor_condition="空闲")
        if final_n is None and final_d is None:
            context = {
                "results": results,
                "status":0
            }
            return render(request, 'resident/search_doctor.html', context=context)
        elif final_n is None:
            doctors = doctor.objects.filter(doctor_dept=final_d)
            context = {
                "doctors": doctors,
                "results": results,
                "status": 1
            }
            final_d=None
            return render(request, 'resident/search_doctor.html', context=context)
        else:
            doctors = doctor.objects.filter(doctor_name=final_n)
            context = {
                "doctors": doctors,
                "results": results,
                "status": 1
            }
            final_n=None
            return render(request, 'resident/search_doctor.html', context=context)
def doctor_info(request):
    global resident_tel
    if request.method == "GET":
        id=request.GET.get("appoint_id")
        result=appoint.objects.filter(id=id).first()
        r=doctor.objects.filter(doctor_telephone=result.doctor_telephone).first()
        context = {
            "doctor_name": r.doctor_name,
            "doctor_sex": r.doctor_sex,
            "doctor_age": r.doctor_age,
            "doctor_work_time": r.doctor_work_time,
            "doctor_dept": r.doctor_dept,
            "doctor_level": r.doctor_level,
            "doctor_hospital": r.doctor_hospital,
        }
        return render(request,'resident/doctor_info.html',context=context)
    else:
        results = appoint.objects.filter(resident_telephone=resident_tel, appoint_result="签约成功")
        context = {
            "results": results
        }
        return render(request,'resident/appoint_doctor.html',context=context)
def new_message(request):
    global resident_tel
    if request.method == "GET":
        results=appoint.objects.filter(Q(resident_telephone=resident_tel) & ~Q(appoint_result=''))
        appoint.objects.filter(resident_telephone=resident_tel,resident_IsRead="未读").update(resident_IsRead="已读")
        context={
            "results":results
        }
        return render(request, 'resident/appoint_message.html',context=context)
    else:
        results = message.objects.filter(message_receive=resident_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request,'resident/consult_message.html',context=context)
def resident_receive_message(request):
    global resident_tel,response_tels
    if request.method == "GET":
        message_id=request.GET.get("message_id")
        message.objects.filter(id=message_id).update(resident_IsRead="已读")
        result=message.objects.filter(id=message_id).first()
        send=doctor.objects.filter(doctor_telephone=result.message_send).first()
        consult_t=appoint.objects.filter(doctor_telephone=result.message_send,resident_telephone=resident_tel).first()
        response_tels=result.message_send
        context={
            "id":consult_t.id,
            "information": result.information,
            "send_time":result.send_time,
            "send_name":send.doctor_name
        }
        return render(request,'resident/resident_receive_message.html',context=context)
    else:
        response_information=request.POST.get("response_information")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message.objects.create(message_send=resident_tel, message_receive=response_tels, send_time=t,
                               information=response_information,doctor_IsRead="未读")
        results=message.objects.filter(message_receive=resident_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'resident/consult_message.html', context=context)
# def resident_contact_shortcut(request):
#     global resident_tel
#     if request.method=="GET":
#         id=request.GET.get("consult_id")
#         doctor_tel=message.objects.filter(id=id).message_send
#


def resident_delete_message(request):
    global resident_tel
    if request.method == "GET":
        id=request.GET.get("message_id")
        message.objects.filter(id=id).delete()
        results = message.objects.filter(message_receive=resident_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'resident/consult_message.html', context=context)
    else:
        results = message.objects.filter(message_receive=resident_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'resident/consult_message.html', context=context)
def delete_appoint(request):
    if request.method == "GET":
        status=request.GET.get("status")
        id=request.GET.get("appoint_id")
        appoint.objects.filter(id=id).delete()
        results = appoint.objects.filter(Q(resident_telephone=resident_tel) & ~Q(appoint_result=''))
        context = {
            "results": results
        }
        return render(request, 'resident/appoint_message.html', context=context)
def alter_password(request):
    global resident_tel
    if request.method == "GET":
        result = user.objects.filter(user_telephone=resident_tel).first()
        context = {
            "user_telephone": result.user_telephone,
            "user_password": result.user_password
        }
        return render(request, 'resident/alter_password.html', context=context)
    else:
        user_telephone = request.POST.get("user_telephone")
        user_password = request.POST.get("user_password")
        user.objects.filter(user_telephone=resident_tel).update(user_telephone=user_telephone,
                                                              user_password=user_password)
        context = {
            "user_telephone": user_telephone,
            "user_password": user_password
        }
        return render(request, 'resident/alter_password.html', context=context)
def home_page(request):
    if request.method == "GET":
        return render(request,'resident/resident_homepage.html')
    else:
        return render(request,'resident/family_calculate.html')
def consult_doctor(request):
    global consult_tel,resident_tel
    if request.method == "GET":
        appoint_id=request.GET.get("consult_id")
        a=appoint_id
        r=appoint.objects.filter(id=appoint_id).first()
        resident_tel=r.resident_telephone
        consult_tel=r.doctor_telephone
        d=doctor.objects.filter(doctor_telephone=r.doctor_telephone).first()
        receive_name=d.doctor_name
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # ms=message.objects.filter(message_send=consult_tel,message_receive=resident_tel).order_by("send_time")
        # mrs=message.objects.filter(message_send=resident_tel,message_receive=consult_tel).order_by("send_time")
        # mylist = zip(mrs, ms)
        mylists = message.objects.order_by("send_time")
        try:
            message.objects.filter(message_send=consult_tel,message_receive=resident_tel).update(resident_IsRead="已读")
            return render(request, 'resident/consult_doctor.html',
                          context = {"receive_name": receive_name, "now_time": t, "mylists": mylists, "appoint_id": a,
                                     "receive_id": consult_tel, "send_id": resident_tel, })
        except AttributeError:
            return render(request, 'resident/consult_doctor.html',
                          context = {"receive_name": receive_name, "now_time": t, "mylists": mylists, "appoint_id": a,
                                     "receive_id": consult_tel, "send_id": resident_tel, })
    else:
        information=request.POST.get("information")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message.objects.create(message_send=resident_tel,message_receive=consult_tel,send_time=t,information=information,doctor_IsRead="未读")
        results = appoint.objects.filter(resident_telephone=resident_tel, appoint_result="签约成功")
        context = {
            "results": results
        }
        return render(request,'resident/appoint_doctor.html',context=context)
def cancel_appoint(request):
    global resident_tel
    if request.method=="GET":
        id=request.GET.get("id")
        a=appoint.objects.filter(id=id).first()
        rd=a.doctor_telephone
        print(id)
        resident.objects.filter(resident_telephone = resident_tel).update(resident_condition = "")
        appoint.objects.filter(resident_telephone=resident_tel).delete()
        try:
            message.objects.filter(message_send=resident_tel).delete()
            message.objects.filter(message_receive=resident_tel).delete()
            return render(request,"resident/appoint_doctor.html",)
        except AttributeError:
            return render(request, "resident/appoint_doctor.html", )
    else:
        results = appoint.objects.filter(resident_telephone = resident_tel)
        context = {
            "results": results
        }
        return render(request, "resident/appoint_doctor.html", context = context)
        # else:
        #     results=appoint.objects.filter(resident_telephone=resident_tel)
        #     context={
        #         "results":results
        #     }
        #     return render(request,"resident/appoint_doctor.html",context = context)


#医生
def alter_doctor_password(request):
    global doctor_tel
    if request.method == "GET":
        result = user.objects.filter(user_telephone=doctor_tel).first()
        context = {
            "user_telephone": result.user_telephone,
            "user_password": result.user_password
        }
        return render(request,'doctor/alter_doctor_password.html',context=context)
    else:
        user_telephone = request.POST.get("user_telephone")
        user_password = request.POST.get("user_password")
        user.objects.filter(user_telephone=doctor_tel).update(user_telephone=user_telephone,user_password=user_password)
        context = {
            "user_telephone": user_telephone,
            "user_password": user_password
        }
        return render(request,'doctor/alter_doctor_password.html',context=context)
def appoint_resident(request):
    global doctor_tel
    if request.method == "GET":
        results = appoint.objects.filter(doctor_telephone=doctor_tel, appoint_result="签约成功")
        context = {
            "results": results
        }
        return render(request,'doctor/appoint_resident.html',context=context)
def contact_resident(request):
    global doctor_tel,contact_id
    if request.method == "GET":
        resident_id=request.GET.get("resident_id")
        ri=resident_id
        r=appoint.objects.filter(id=resident_id).first()
        contact_id=r.resident_telephone
        a=resident.objects.filter(resident_telephone=r.resident_telephone).first()
        doctor_tel=appoint.objects.filter(resident_telephone=r.resident_telephone).first().doctor_telephone
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # ms=message.objects.filter(message_send=r.resident_telephone,message_receive=doctor_tel).all()
        # mrs=message.objects.filter(message_send=doctor_tel,message_receive=r.resident_telephone).all()
        # mylist=zip(ms,mrs)
        # print(mrs)
        mylists = message.objects.order_by("send_time")
        try:
            message.objects.filter(message_send=r.resident_telephone,message_receive=doctor_tel).update(doctor_IsRead="已读")
            context = {
                "now_time": t,
                "receive_name": a.resident_name,
                "receive_id": contact_id,
                "mylists": mylists,
                "resident_id": ri,
            }
            return render(request, 'doctor/contact_resident.html', context = context)
        except AttributeError:
            context = {
                "now_time": t,
                "receive_name": a.resident_name,
                "receive_id": contact_id,
                "mylists": mylists,
                "resident_id": ri,
            }
            return render(request, 'doctor/contact_resident.html', context = context)
    else:
        information = request.POST.get("information")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message.objects.create(message_send=doctor_tel, message_receive=contact_id, send_time=t,
                               information=information, resident_IsRead="未读")
        results = appoint.objects.filter(doctor_telephone=doctor_tel, appoint_result="签约成功")
        context = {
            "results": results
        }
        return render(request, 'doctor/appoint_resident.html', context=context)
def appoint_service_team(request):
    global doctor_tel
    if request.method == "GET":
        results=Service_Team.objects.filter(team_appoint_doctor=doctor_tel)
        context={
            "results":results
        }
        return render(request,'doctor/appoint_service_team.html',context=context)
def doctor_home_page(request):
    global doctor_tel
    if request.method == "GET":
        signal=doctor.objects.filter(doctor_telephone=doctor_tel).first().doctor_condition
        if signal=="空闲":
            return render(request, 'doctor/doctor_homepage.html', context={"signal1": 1})
        else:
            doctor.objects.filter(doctor_telephone=doctor_tel).update(doctor_condition="忙碌")
            return render(request, 'doctor/doctor_homepage.html', context={"signal1": 0})
    else:
        signal=request.POST.get("signal")
        if signal=="空闲":
            doctor.objects.filter(doctor_telephone=doctor_tel).update(doctor_condition="空闲")
            return render(request,'doctor/doctor_homepage.html',context={"signal1":1})
        else:
            doctor.objects.filter(doctor_telephone=doctor_tel).update(doctor_condition="忙碌")
            return render(request,'doctor/doctor_homepage.html',context={"signal1":0})
def doctor_personal_info(request):
    global doctor_tel
    if request.method == "GET":
        result = doctor.objects.filter(doctor_telephone=doctor_tel).first()
        if result is None:
            return render(request, 'doctor/doctor_personal_info.html',context={"status":1})
        else:
            context = {
                "doctor_name": result.doctor_name,
                "doctor_sex": result.doctor_sex,
                "doctor_age": result.doctor_age,
                "doctor_work_time": result.doctor_work_time,
                "doctor_dept": result.doctor_dept,
                "doctor_level": result.doctor_level,
                "doctor_hospital": result.doctor_hospital,
            }
            return render(request, 'doctor/doctor_personal_info.html', context=context)
    else:
        doctor_name = request.POST.get("doctor_name")
        doctor_sex = request.POST.get("doctor_sex")
        doctor_age = request.POST.get("doctor_age")
        doctor_work_time = request.POST.get("doctor_work_time")
        doctor_dept = request.POST.get("doctor_dept")
        doctor_level = request.POST.get("doctor_level")
        doctor_hospital = request.POST.get("doctor_hospital")
        result=doctor.objects.filter(doctor_telephone=doctor_tel).first()
        if result is None:
            doctor.objects.create(doctor_name=doctor_name, doctor_sex=doctor_sex, doctor_age=doctor_age,
                                  doctor_telephone=doctor_tel, doctor_work_time=doctor_work_time,
                                  doctor_dept=doctor_dept,
                                  doctor_level=doctor_level, doctor_hospital=doctor_hospital,)
        else:
            doctor.objects.filter(doctor_telephone=doctor_tel).update(doctor_name=doctor_name, doctor_age=doctor_age,
                                                                      doctor_work_time=doctor_work_time,
                                                                      doctor_dept=doctor_dept, doctor_sex=doctor_sex,
                                                                      doctor_level=doctor_level,
                                                                      doctor_hospital=doctor_hospital,
                                                                     )

            context = {
                "doctor_name": doctor_name,
                "doctor_sex": doctor_sex,
                "doctor_age": doctor_age,
                "doctor_work_time": doctor_work_time,
                "doctor_dept": doctor_dept,
                "doctor_level": doctor_level,
                "doctor_hospital": doctor_hospital,
            }
            return render(request, 'doctor/doctor_personal_info.html', context=context)
def doctor_new_message(request):
    global doctor_tel
    if request.method == "GET":
        results=appoint.objects.filter(Q(doctor_telephone=doctor_tel)&~Q(appoint_result='签约失败'))
        context={     #把签约成功和未处理的签约消息显示出来
            "results":results,
        }
        return render(request, 'doctor/doctor_appoint_message.html',context=context)
    else:
        results=message.objects.filter(message_receive=doctor_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'doctor/doctor_consult_message.html',context=context)
def doctor_appoint_message(request):
    global doctor_tel
    if request.method == "GET":
        id=request.GET.get("appoint_id")
        appoint.objects.filter(id=id).update(doctor_IsRead="已读")
        result=appoint.objects.filter(id=id).first()
        resident_telephone=result.resident_telephone
        final_result=result.appoint_result
        r=resident.objects.filter(resident_telephone=resident_telephone).first()
        d=doctor.objects.filter(doctor_telephone=doctor_tel).first()
        if final_result=="签约成功":
            context={
                "resident_name":r.resident_name,
                "resident_sex":r.resident_sex,
                "resident_age":r.resident_age,
                "resident_telephone":r.resident_telephone,
                "resident_address":r.resident_address,
                "doctor_name":d.doctor_name,
                "doctor_sex":d.doctor_sex,
                "doctor_age":d.doctor_age,
                "doctor_hospital":d.doctor_hospital,
                "doctor_telephone":d.doctor_telephone,
                "status":1
            }
            return render(request,'doctor/appoint_info.html',context=context)
        else:
            context = {
                "resident_name": r.resident_name,
                "resident_sex": r.resident_sex,
                "resident_age": r.resident_age,
                "resident_telephone": r.resident_telephone,
                "resident_address": r.resident_address,
                "doctor_name": d.doctor_name,
                "doctor_sex": d.doctor_sex,
                "doctor_age": d.doctor_age,
                "doctor_hospital": d.doctor_hospital,
                "doctor_telephone": d.doctor_telephone,
            }
            return render(request, 'doctor/appoint_info.html', context=context)
def appoint_detail(request):
    global doctor_tel
    if request.method == "GET":
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        resident_telephone=request.GET.get("resident_telephone")
        print(resident_telephone)
        doctor_telephone=request.GET.get("doctor_telephone")
        r=resident.objects.filter(resident_telephone=resident_telephone).first()
        print(r)
        print("doctor_telephone")
        d=doctor.objects.filter(doctor_telephone=doctor_telephone).first()
        appoint.objects.filter(resident_telephone=resident_telephone,doctor_telephone=doctor_telephone).update(doctor_deal_time=t,appoint_result="签约成功",resident_IsRead="未读")
        resident.objects.filter(resident_telephone=resident_telephone).update(resident_condition="已签约")
        context = {
            "resident_name": r.resident_name,
            "resident_sex": r.resident_sex,
            "resident_age": r.resident_age,
            "resident_telephone": r.resident_telephone,
            "resident_address": r.resident_address,
            "doctor_name": d.doctor_name,
            "doctor_sex": d.doctor_sex,
            "doctor_age": d.doctor_age,
            "doctor_hospital": d.doctor_hospital,
            "doctor_telephone": d.doctor_telephone,
            "status": 1
        }
        return render(request, 'doctor/appoint_info.html', context=context)
    else:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        resident_telephone = request.POST.get("resident_telephone")
        doctor_telephone = request.POST.get("doctor_telephone")
        appoint.objects.filter(resident_telephone=resident_telephone, doctor_telephone=doctor_telephone).update(
        doctor_deal_time=t, appoint_result="签约失败",resident_IsRead="未读")
        results = appoint.objects.filter(Q(doctor_telephone=doctor_tel) & ~Q(appoint_result='签约失败'))
        context = {
            "results": results,
        }
        return render(request,'doctor/doctor_appoint_message.html',context=context)
def doctor_receive_message(request):
    global doctor_tel,response_tel
    if request.method == "GET":
        message_id=request.GET.get("message_id")
        result=message.objects.filter(id=message_id).first()
        message.objects.filter(id=message_id).update(doctor_IsRead="已读")
        response_tel=result.message_send
        a=appoint.objects.filter(resident_telephone=response_tel,doctor_telephone=doctor_tel).first()
        send=resident.objects.filter(resident_telephone=result.message_send).first()
        context = {
            "information": result.information,
            "send_time": result.send_time,
            "send_name": send.resident_name,
            "resident":a,
        }
        return render(request,'doctor/receive_message.html',context=context)
    else:
        response_information=request.POST.get("response_information")
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message.objects.create(message_send=doctor_tel, message_receive=response_tel, send_time=t,
                               information=response_information,resident_IsRead="未读")
        results=message.objects.filter(message_receive=doctor_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request,'doctor/doctor_consult_message.html',context=context)
def doctor_delete_message(request):
    global doctor_tel
    if request.method == "GET":
        id = request.GET.get("message_id")
        message.objects.filter(id=id).delete()
        results = message.objects.filter(message_receive=doctor_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'doctor/doctor_consult_message.html', context=context)
    else:
        results = message.objects.filter(message_receive=doctor_tel).order_by("-id")
        context = {
            "results": results
        }
        return render(request, 'doctor/doctor_consult_message.html', context=context)
def search_service_team(request):
    global doctor_tel
    if request.method == "GET":
        team_id = request.GET.get("team_id")
        results = Service_Team.objects.filter(team_condition = "空闲")
        context = {
            "results": results,
            "status": 1,
        }
        Service_Team.objects.filter(id = team_id).update(team_appoint_doctor = doctor_tel,team_condition="已签约")
        return render(request, 'doctor/search_service_team.html', context = context)
    else:
        results = Service_Team.objects.filter(team_condition = "空闲")
        dt_c=Service_Team.objects.filter(team_appoint_doctor=doctor_tel).first()
        context = {
            "results": results,
            "doctor_appoint_condition":dt_c,
        }
        return render(request, 'doctor/search_service_team.html', context = context)
def search_teams(request):
    global doctor_tel
    if request.method == "GET":
        team_name = request.GET.get("team_name")
        teams = Service_Team.objects.filter(team_name__icontains = team_name)
        dt_c = Service_Team.objects.filter(team_appoint_doctor = doctor_tel).first( )
        context = {
            "results": teams,
            "team_name": team_name,
            "doctor_appoint_condition": dt_c,
        }
        return render(request, 'doctor/search_service_team.html', context = context)
def delete_teams(request):
    global doctor_tel
    id=request.GET.get("team_id")
    Service_Team.objects.filter(id=id).update(team_appoint_doctor="",team_condition="")
    results = Service_Team.objects.filter(team_appoint_doctor=doctor_tel)
    context = {
        "results": results
    }
    return render(request, 'doctor/appoint_service_team.html', context=context)
def delete_appoint(request):
    appoint_id=request.GET.get("appoint_id")
    appoint.objects.filter(id=appoint_id).delete()
    return render(request,'doctor/appoint_resident.html')
def resident_info(request):
    global doctor_tel
    if request.method=="GET":
        resident_id=request.GET.get("resident_id")
        r=appoint.objects.filter(id=resident_id).first()
        doctor_tel=r.doctor_telephone
        contact_tel=r.resident_telephone
        print(contact_tel)
        results=resident.objects.filter(resident_telephone=contact_tel).first()
        context={
            "results":results
        }
        return render(request,'doctor/resident_info.html',context = context)
    else:
        results = appoint.objects.filter(doctor_telephone = doctor_tel, appoint_result = "签约成功")
        context = {
            "results": results
        }
        return render(request, 'doctor/appoint_resident.html', context = context)
def resident_health_report(request):
    global r_name,contact_tel,doctor_tel
    if request.method=="GET":
        resident_id=request.GET.get("resident_id")
        r=appoint.objects.filter(id=resident_id).first()
        contact_tel=r.resident_telephone
        doctor_tel=r.doctor_telephone
        re=resident.objects.filter(resident_telephone=contact_tel).first()
        r_name=re.resident_name
        results=Health_Report.objects.filter(report_telephone=contact_tel, report_name=r_name).first()
        if results is None:
            results = appoint.objects.filter(doctor_telephone = doctor_tel, appoint_result = "签约成功")
            context = {
                "results": results,
                "status":1
            }
            return render(request, 'doctor/appoint_resident.html', context = context)
        else:
            name=r_name
            results=Health_Report.objects.filter(report_telephone=contact_tel, report_name=name)
            context={
                "results":results,
                'name':name
            }
            return render(request,'doctor/resident_health_report.html',context = context)
    else:
        results = appoint.objects.filter(doctor_telephone = doctor_tel, appoint_result = "签约成功")
        context = {
            "results": results
        }
        return render(request, 'doctor/appoint_resident.html', context = context)
def resident_family(request):
    global r_name, resident_tel, doctor_tel
    if request.method == "GET":
        resident_id = request.GET.get("resident_id")
        r = appoint.objects.filter(id = resident_id).first( )
        resident_tel = r.resident_telephone
        doctor_tel = r.doctor_telephone
        rr = resident.objects.filter(resident_telephone = resident_tel).first( )
        rf = family.objects.filter(family_telephone = resident_tel).first( )
        r_name = rr.resident_name
        if rf is None:
            results = appoint.objects.filter(doctor_telephone = doctor_tel, appoint_result = "签约成功")
            context = {
                "results": results,
                "status": 1
            }
            return render(request, 'doctor/appoint_resident.html', context = context)
        else:
            name=r_name
            results = family.objects.filter(family_telephone=resident_tel)
            context = {
                "results": results,
                "name":name
            }
            return render(request, 'doctor/resident_family.html', context = context)
    else:
        results = appoint.objects.filter(doctor_telephone = doctor_tel, appoint_result = "签约成功")
        context = {
            "results": results
        }
        return render(request, 'doctor/appoint_resident.html', context = context)


def resident_family_health_report(request):
    global r_name,resident_tel,doctor_tel
    if request.method=="GET":
        family_id=request.GET.get("family_id")
        r=family.objects.filter(id=family_id).first()
        rp_name=r.family_name
        resident_tel=r.family_telephone
        rr=resident.objects.filter(resident_telephone=resident_tel).first()
        rf=family.objects.filter(family_telephone=resident_tel).first()
        rfh=Health_Report.objects.filter(report_telephone=resident_tel,report_name=rp_name).first()
        r_name=rr.resident_name
        if rfh is None:
            name = r_name
            results = family.objects.filter(family_telephone = resident_tel)
            context = {
                "results": results,
                "name": name,
                "status":1
            }
            return render(request, 'doctor/resident_family.html', context = context)
        else:
            name=rp_name
            results=Health_Report.objects.filter(report_telephone=resident_tel,report_name=rp_name)
            context={
                "results":results,
                "name":name
            }
            return render(request,'doctor/resident_family_health_report.html',context = context)
    else:
        name = r_name
        results = family.objects.filter(family_telephone = resident_tel)
        context = {
            "results": results,
            "name": name
        }
        return render(request, 'doctor/resident_family.html', context = context)

#管理员
def manager_home_page(request):
    if request.method == "GET":
        return render(request,'manager/manager_homepage.html')
def alter_manager_password(request):
    global manager_tel
    if request.method == "GET":
        result=user.objects.filter(user_telephone=manager_tel).first()
        context={
            "user_telephone":result.user_telephone,
            "user_password":result.user_password
        }
        return render(request,'manager/alter_manager_password.html',context=context)
    else:
        user_telephone = request.POST.get("user_telephone")
        user_password = request.POST.get("user_password")
        user.objects.filter(user_telephone=manager_tel).update(user_telephone=user_telephone,user_password=user_password)
        context={
            "user_telephone":user_telephone,
            "user_password":user_password
        }
        return render(request, 'manager/alter_manager_password.html', context=context)
def search_resident(request):
    if request.method == "GET":
        results = resident.objects.all( )
        context = {
            "results": results
        }
        return render(request, 'manager/search_resident.html', context = context)
    else:
        resident_name = request.POST.get("resident_name")
        residents = resident.objects.filter(resident_name__icontains = resident_name)
        context = {
            "results": residents,
            "resident_name": resident_name,
        }
        return render(request, 'manager/search_resident.html', context = context)
def search_doctors(request):
    if request.method == "GET":
        results = doctor.objects.all( )
        context = {
            "results": results
        }
        return render(request, 'manager/search_doctors.html', context = context)
    else:
        doctor_name = request.POST.get("doctor_name")
        doctors = doctor.objects.filter(doctor_name__icontains = doctor_name)
        context = {
            "results": doctors,
            "doctor_name": doctor_name,
        }
        return render(request, 'manager/search_doctors.html', context = context)
def search_team(request):
    if request.method == "GET":
        results = Service_Team.objects.all( )
        context = {
            "results": results
        }
        return render(request, 'manager/search_team.html', context = context)
    else:
        team_name = request.POST.get("team_name")
        teams = Service_Team.objects.filter(team_name__icontains = team_name)
        context = {
            "results": teams,
            "team_name": team_name,
        }
        return render(request, 'manager/search_team.html', context = context)
def search_account(request):
    if request.method == "GET":
        results = user.objects.all( )
        context = {
            "results": results
        }
        return render(request, 'manager/search_account.html', context = context)
    else:
        account_type = request.POST.get("account_type")
        accounts = user.objects.filter(user_identity__icontains = account_type)
        context = {
            "results": accounts,
            "account_type": account_type,
        }
        return render(request, 'manager/search_account.html', context = context)
def delete_doctor(request):
    if request.method == "GET":
        id=request.GET.get("id")
        doctor_tel=doctor.objects.filter(id=id).first().doctor_telephone
        delete_a=appoint.objects.filter(doctor_telephone=doctor_tel).first()
        delete_m=message.objects.filter(message_send=doctor_tel).first()
        update_t=Service_Team.objects.filter(team_appoint_doctor=doctor_tel).first()
        if delete_a is not None and delete_m is not None and update_t is not None:
            doctor.objects.filter(id=id).delete()
            user.objects.filter(user_telephone=doctor_tel).delete()
            appoint.objects.filter(doctor_telephone=doctor_tel).delete()
            message.objects.filter(message_send = doctor_tel).delete()
            Service_Team.objects.filter(team_appoint_doctor = doctor_tel).update(team_appoint_doctor=None,team_condition="空闲")
            results = doctor.objects.all()
            context = {
                "results": results
            }
            return render(request,'manager/search_doctors.html',context=context)
        elif delete_a is not None and update_t is not None:
            doctor.objects.filter(id=id).delete()
            user.objects.filter(user_telephone = doctor_tel).delete( )
            appoint.objects.filter(doctor_telephone=doctor_tel).delete()
            Service_Team.objects.filter(team_appoint_doctor = doctor_tel).update(team_appoint_doctor = None,team_condition="空闲")
            results=doctor.objects.all()
            context={
                "results":results
            }
            return render(request,'manager/search_doctors.html',context = context)
        elif delete_m is not None and update_t is not None:
            doctor.objects.filter(id=id).delete()
            user.objects.filter(user_telephone = doctor_tel).delete()
            message.objects.filter(message_send = doctor_tel).delete()
            Service_Team.objects.filter(team_appoint_doctor = doctor_tel).update(team_appoint_doctor = None,team_condition="空闲")
            results=doctor.objects.all()
            context={
                "results":results
            }
            return render(request,"manager/search_doctors.html",context = context)
        elif delete_m is not None and delete_a is not None:
            doctor.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = doctor_tel).delete( )
            appoint.objects.filter(doctor_telephone = doctor_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            results = doctor.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_doctors.html', context = context)
        elif delete_a is not None:
            doctor.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = doctor_tel).delete( )
            appoint.objects.filter(doctor_telephone = doctor_tel).delete( )
            results = doctor.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_doctors.html', context = context)
        elif delete_m is not None:
            doctor.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = doctor_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            results = doctor.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_doctors.html', context = context)
        elif update_t is not None:
            doctor.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = doctor_tel).delete( )
            Service_Team.objects.filter(team_appoint_doctor = doctor_tel).update(team_appoint_doctor = None,team_condition="空闲")
            results = doctor.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_doctors.html', context = context)
        else:
            doctor.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = doctor_tel).delete( )
            results = doctor.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_doctors.html', context = context)
def delete_resident(request):
    if request.method == "GET":
        id=request.GET.get("id")
        resident_tel=resident.objects.filter(id=id).first().resident_telephone
        delete_a = appoint.objects.filter(resident_telephone = resident_tel).first()
        delete_m = message.objects.filter(message_send = resident_tel).first()
        delete_f = family.objects.filter(family_telephone=resident_tel).first()
        delete_h = Health_Report.objects.filter(report_telephone=resident_tel).first()
        if delete_a is not None and delete_m is not None and delete_f is not None and delete_h is not None:
            resident.objects.filter(id = id).delete()
            user.objects.filter(user_telephone = resident_tel).delete()
            appoint.objects.filter(resident_telephone = resident_tel).delete()
            message.objects.filter(message_send = doctor_tel).delete()
            family.objects.filter(family_telephone=resident_tel).delete()
            Health_Report.objects.filter(report_telephone=resident_tel).delete()
            results = resident.objects.all()
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None and delete_f is not None and delete_h is not None:
            resident.objects.filter(id = id).delete()
            user.objects.filter(user_telephone = resident_tel).delete()
            appoint.objects.filter(resident_telephone = resident_tel).delete()
            family.objects.filter(family_telephone = resident_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all()
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_m is not None and delete_f is not None and delete_h is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            message.objects.filter(message_send = resident_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, "manager/search_resident.html", context = context)
        elif delete_a is not None and delete_m is not None and delete_f is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None and delete_m is not None and delete_h is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None and delete_m is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None and delete_h is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None and delete_f is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_m is not None and delete_f is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_m is not None and delete_h is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_h is not None and delete_f is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_h is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            Health_Report.objects.filter(report_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_m is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            message.objects.filter(message_send = doctor_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_f is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            family.objects.filter(family_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        elif delete_a is not None:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            appoint.objects.filter(resident_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        else:
            resident.objects.filter(id = id).delete( )
            user.objects.filter(user_telephone = resident_tel).delete( )
            results = resident.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_resident.html', context = context)
        # resident.objects.filter(id=id).delete()
        # appoint.objects.filter(resident_telephone=resident_tel).delete()
        # message.objects.filter(message_send=resident_tel).delete()
        # message.objects.filter(message_receive = resident_tel).delete()
        # results = resident.objects.all()
        # context = {
        #     "results": results
        # }
        # return render(request,'manager/search_resident.html',context=context)
def delete_team(request):
    if request.method == "GET":
        id=request.GET.get("id")
        # 只有team中有医生的账号信息，删除掉就不需要涉及到医生的信息变动反过来需要更新团队的信息和状态
        Service_Team.objects.filter(id=id).delete()
        results = Service_Team.objects.all()
        context = {
            "results": results
        }
        return render(request,'manager/search_team.html',context=context)
def delete_account(request):
    if request.method == "GET":
        telephone=request.GET.get("telephone")
        u =user.objects.filter(user_telephone=telephone).first()
        identity=u.user_identity
        if identity=="居民":
            user.objects.filter(user_telephone = telephone).delete( )
            resident.objects.filter(resident_telephone=telephone).delete()
            family.objects.filter(family_telephone=telephone).delete()
            Health_Report.objects.filter(report_telephone=telephone).delete()
            appoint.objects.filter(resident_telephone=telephone).delete()
            message.objects.filter(message_send=telephone).delete()
            results = user.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_account.html', context = context)
        elif identity=="医生":
            user.objects.filter(user_telephone = telephone).delete( )
            doctor.objects.filter(doctor_telephone=telephone).delete()
            appoint.objects.filter(doctor_telephone=telephone).delte()
            Service_Team.objects.filter(team_appoint_doctor=telephone).update(team_appoint_doctor=None,team_condition="空闲")
            message.objects.filter(message_send=telephone).delete()
            results = user.objects.all( )
            context = {
                "results": results
            }
            return render(request, 'manager/search_account.html', context = context)
    else:
        results = user.objects.all()
        context = {
            "results": results
        }
        return render(request,'manager/search_account.html',context=context)#这个功能不要了要改的太多
def manager_search_message(request):
    if request.method == "GET":
        results=message.objects.all()
        context={
            "results":results
        }
        return render(request,'manager/manager_search_message.html',context=context)
    else:
        send_tel=request.POST.get("send_tel")
        results=message.objects.filter(message_send__icontains=send_tel)
        context={
            "results": results,
            "send_tel":send_tel
        }
        return render(request,'manager/manager_search_message.html',context=context)
def manager_delete_message(request):
    id = request.GET.get("id")
    message.objects.filter(id=id).delete()
    results = message.objects.all()
    context = {
        "results": results
    }
    return render(request, 'manager/manager_search_message.html', context=context)
def manager_search_appoint(request):
    if request.method == "GET":
        results = appoint.objects.all()
        context = {
            "results": results
        }
        return render(request, 'manager/manager_search_appoint.html', context=context)
def manager_search_a(request):
    if request.method == "GET":
        resident_tel = request.GET.get("resident_tel")
        print(resident_tel)
        results = appoint.objects.filter(resident_telephone__icontains=resident_tel)
        context = {
            "results": results,
            "resident_tel": resident_tel
        }
        return render(request, 'manager/manager_search_appoint.html', context=context)
    else:
        doctor_tel = request.POST.get("doctor_tel")
        results = appoint.objects.filter(doctor_telephone__icontains=doctor_tel)
        context = {
            "results": results,
            "doctor_tel": doctor_tel
        }
        return render(request, 'manager/manager_search_appoint.html', context=context)
def manager_delete_appoint(request):
    id = request.GET.get("id")
    appoint.objects.filter(id=id).delete()
    results = appoint.objects.all()
    context = {
        "results": results
    }
    return render(request, 'manager/manager_search_appoint.html', context=context)

def back1(request):
    global resident_tel
    if request.method == "GET":
        return render(request,'login.html')
    else:
        results = family.objects.filter(family_telephone=resident_tel)
        context = {
            "results": results
        }
        return render(request, 'resident/search_family.html', context=context)
def back2(request):
    global resident_tel
    if request.method == "GET":
        results = family.objects.filter(family_telephone=resident_tel)
        context = {
            "results": results
        }
        return render(request,'resident/search_family.html',context=context)
    else:
        results = appoint.objects.filter(Q(doctor_telephone__icontains=doctor_tel) & ~Q(appoint_result='签约失败'))
        context = {  # 把签约成功和未处理的签约消息显示出来
            "results": results,
        }
        return render(request, 'doctor/doctor_appoint_message.html', context=context)


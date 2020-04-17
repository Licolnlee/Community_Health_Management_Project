from django.db import models


class resident(models.Model):  #居民信息表
    gender=(
        ('male','男'),
        ('female','女'),
    )
    resident_name=models.CharField(max_length=20)#姓名
    resident_sex=models.CharField(max_length=10,choices = gender,default = '男')#性别
    resident_age=models.CharField(max_length=10)#年龄
    resident_telephone=models.CharField(max_length = 20,unique = True)#电话/账号
    resident_address=models.CharField(max_length = 20)#住址
    resident_condition=models.CharField(max_length = 20,null = True)#居民签约状态


    def __str__(self):
        return self.resident_telephone

    class Meta:
        ordering=['resident_telephone']

class doctor(models.Model):  #医生信息表
    gender=(
        ('男','男'),
        ('女','女'),
    )
    doctor_name=models.CharField(max_length = 20)#医生姓名
    doctor_sex=models.CharField(max_length = 20,choices = gender,default = '男')#医生性别
    doctor_age=models.CharField(max_length = 20)#医生年龄
    doctor_telephone = models.CharField(max_length=20,unique = True)#医生电话/账号
    doctor_work_time = models.CharField(max_length=50)#医生工作经验
    doctor_level = models.CharField(max_length=50)#医生等级
    doctor_dept = models.CharField(max_length=50)#科室
    doctor_condition = models.CharField(max_length=50,null=True)#医生出诊状态(改成booleanfield）
    doctor_hospital = models.CharField(max_length=50)#所属医院


    def __str__(self):
        return self.doctor_telephone

    class Meta:
        ordering=['doctor_telephone']

class user(models.Model):  #用户表
    user_telephone=models.CharField(max_length = 50,primary_key=True,unique = True)#用户手机号/账号
    user_password=models.CharField(max_length = 20)#用户密码
    user_identity=models.CharField(max_length = 20)#用户身份

    def __str__(self):
        return self.user_telephone

    class Meta:
        ordering=['user_telephone']

class Health_Report(models.Model):  #健康报表
    report_name=models.CharField(max_length = 20)#姓名
    report_telephone=models.CharField(max_length = 20)#账号
    report_height=models.CharField(max_length = 20)#身高
    report_weight=models.CharField(max_length = 20)#体重
    result_num=models.CharField(max_length = 20)#BMI值
    result_condition=models.CharField(max_length = 20)#测试结果
    report_time=models.CharField(max_length = 20)#测试时间

    def __str__(self):
        return self.report_name

    class Meta:
        ordering = ['report_telephone']



class family(models.Model):  #家庭成员信息表
    family_name=models.CharField(max_length=20)#姓名
    family_sex=models.CharField(max_length=10)#性别
    family_age=models.CharField(max_length=10)#年龄
    family_relationship=models.CharField(max_length=10)#关系
    family_telephone=models.CharField(max_length=20)#所属账户

    def __str__(self):
        return self.family_name

    class Meta:
        ordering = ['family_telephone']


class Service_Team(models.Model):#服务团队表
    team_name=models.CharField(max_length=30)#公司名称
    team_telephone=models.CharField(max_length=20)#联系电话
    team_introduction=models.CharField(max_length=50,null=True)#简介
    team_condition=models.CharField(max_length=20)#团队状态
    team_appoint_doctor=models.CharField(max_length=20,null=True)#当前签约医生
    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ['team_name']







class appoint(models.Model):  #签约表
    resident_telephone=models.CharField(max_length = 20)#居民账户
    doctor_telephone=models.CharField(max_length = 20)#医生账户
    resident_appoint_time=models.CharField(max_length = 20)#居民预约时间
    resident_request_time = models.CharField(max_length=20)#发送时间
    doctor_IsRead = models.CharField(max_length=20, null=True)  # 医生消息是否已读
    resident_IsRead = models.CharField(max_length = 20,null = True) #居民消息是否已读
    doctor_deal_time = models.CharField(max_length=20,null=True)  # 医生处理请求的时间
    appoint_result = models.CharField(max_length=20,null=True)  # 签约结果


    def __str__(self):
        return self.resident_telephone

    class Meta:
        ordering = ['resident_telephone']








class message(models.Model):  #消息表
    message_send = models.CharField(max_length=20)  # 发送者账户
    message_receive = models.CharField(max_length=20)  # 接收者账户
    send_time = models.CharField(max_length=20,null=True)#发送消息时间
    doctor_IsRead = models.CharField(max_length=20,null=True)  # 医生消息是否已读
    resident_IsRead = models.CharField(max_length = 20, null = True)  #居民消息是否已读
    information = models.CharField(max_length=50,null=True)  # 内容


    def __str__(self):
        return self.message_send

    class Meta:
        ordering = ['message_send']



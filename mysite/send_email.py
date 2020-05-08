import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    send_mail(
        '测试邮件',
        '欢迎访问',
        '951248020@qq.com',
        ['951248020@qq.com'],
    )
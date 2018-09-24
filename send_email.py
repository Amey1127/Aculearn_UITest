# -*- coding:utf-8 -*-
from test_TCsuper import testTCsuper
from test_TCmanager import testTCmanager
from test_TCclass import testTCclass
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import unittest
from HTMLTestRunner import HTMLTestRunner
import os
import time

def report():
    testsuit = unittest.TestSuite()
    report = os.path.join('D:/study/python/TCtest_v1.1/report/TCtest_report.html')
    #testsuit.addTests([testTCsuper('test_TCsuper_login'), testTCsuper('test_TCsuper_logout'), testTCmanager('test_TCmanager_login'), testTCmanager('test_TCmanager_logout'), testTCclass('test_TCclass_login'), testTCclass('test_TCclass_classin'), testTCclass('test_TCclass_YouTube'), testTCclass('test_TCclass_classoff')])
    testsuit.addTests(
        [testTCsuper('test_TCsuper_login'),testTCmanager('test_TCmanager_login'),
         testTCclass('test_TCclass_login'), testTCclass('test_TCclass_classin'),
         testTCclass('test_TCclass_YouTube'), testTCclass('test_TCclass_classoff')])
    with open(report, 'wb') as fp:  # 定义测试报告
        runner = HTMLTestRunner(fp, verbosity=2, title='TC回归测试报告', description='执行人：Amey')
        result = runner.run(testsuit)

    return result

def send_email():
    username = 'limei.wang@aculearn.com.cn'
    password = 'xxxxxx'

    replyto = '***'
    rcptto = ['junhong.Jiang@aculearn.com.cn', 'jiaqi.chai@aculearn.com.cn']

    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('TC自动化测试报告').encode()
    msg['From'] = '%s <%s>' % (Header('Amey').encode(), username)
    msg['To'] = ','.join(rcptto)
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()

    # 构建alternative的text部分
    text = MIMEText('测试点：TC超管登录；TC管理后台登录；TC上课系统登录、上课、YouTube视频、下课', _charset='UTF-8')
    msg.attach(text)

    #添加附件
    rep = os.path.join('D:/study/python/TCtest_v1.1/report/TCtest_report.html')
    part = MIMEApplication(open(rep,'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="TCtest_report.html")
    msg.attach(part)

    # 发送邮件
    try:
        client = smtplib.SMTP()
        client.connect('smtp.mxhichina.com', 25)

        client.set_debuglevel(0)

        client.login(username, password)

        client.sendmail(username, rcptto, msg.as_string())
        client.quit()
        print('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', e.message)
    except Exception as e:
        print('邮件发送异常, ', str(e))

if  __name__ == '__main__':
    while(1):
        result = report()
        if result.error_count + result.failure_count > 0:
            send_email()
        time.sleep(1500)

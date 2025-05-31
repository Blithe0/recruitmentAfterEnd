import smtplib
from email.mime.text import MIMEText

def send_invitation_email(candidate_id, interviewer_id, time, method, link):
    content = f"""您有一场新的面试：
面试时间：{time}
面试方式：{method}
面试链接：{link}
"""
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = '面试邀约通知'

    # 假设邮件系统为 SMTP 发送
    server = smtplib.SMTP('smtp.163.com', 25)
    server.login('your_email@163.com', '授权码')
    server.sendmail('your_email@163.com', ['candidate@example.com', 'interviewer@example.com'], msg.as_string())
    server.quit()

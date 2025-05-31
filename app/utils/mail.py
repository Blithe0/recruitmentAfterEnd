import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_invitation_email(candidate_id, interviewer_id, time, method, link):
    # 面试方式映射
    method_map = {
        'one': '一对一面试',
        'group': '无领导小组',
        'structured': '结构化面试'
    }
    method_cn = method_map.get(method, method)  # 若无法映射保留原值

    content = f"""您有一场新的面试：
面试时间：{time}
面试方式：{method_cn}
面试链接：{link}
"""
    msg = MIMEText(content, 'plain', 'utf-8')
    # msg['Subject'] = '面试邀约通知'
    msg['Subject'] = Header('面试邀约通知', 'utf-8')
    msg['From'] = '1761516187@qq.com'
    msg['To'] = '21301100@bjtu.edu.cn'

    # 假设邮件系统为 SMTP 发送
    # server = smtplib.SMTP('smtp.163.com', 25)
    # server.login('your_email@163.com', '授权码')
    # server.sendmail('your_email@163.com', ['candidate@example.com', 'interviewer@example.com'], msg.as_string())

    #  QQ邮箱的SMTP(SLL)端口为465或587
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login('1761516187@qq.com', 'trefroajncfqdgcg')
    server.sendmail('1761516187@qq.com', ['21301100@bjtu.edu.cn'], msg.as_string())

    # server = smtplib.SMTP('mail.bjtu.edu.cn', 143)
    # server.login('21301100@bjtu.edu.cn', 'mm525zjlxy')
    # server.sendmail('21301100@bjtu.edu.cn', ['21301100@bjtu.edu.cn', '21301100@bjtu.edu.cn'], msg.as_string())
    server.quit()

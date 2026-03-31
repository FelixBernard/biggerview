import os
import sql.sql as sql
from datetime import datetime, timezone
# from scripts.token_google import TOKEN
TOKEN = "aaa"

def check_user_name():
    pass

def check_user_adress():
    pass

def check_user_data():
    check_user_adress()

def send_admin_flag(aktion):
    send_email(
        'Flag',
        f'Flag -- {aktion}',
        'contact@iamhiding.online')
    
def send_admin_alert(aktion):
    send_email(
        'Alert',
        f'Alert -- {aktion}',
        'contact@iamhiding.online')

def send_email(subject, massage, to_addr):
    try:
        import smtplib
        from email.mime.text import MIMEText
        # print(subject, massage, to_addr)
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        # with open(textfile, 'rb') as fp:
        #     # Create a text/plain message
        msg = MIMEText(massage)
        me = 'flag@felix-bernard.de'
        you = to_addr
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('felixs.infos@gmail.com', TOKEN)
        s.sendmail(me, [you], msg.as_string())
        s.quit()
    except:
        print('Wanted to send email, but fail')

def prevent_sql_inqeckt(text:str, want_flag:bool):
    flag = False
    if "'" in text:
        text = text.replace("'", "Hochkomma")
        flag = True
    if '"' in text:
        text = text.replace('"', "Hochkomma")
        flag = True
    if "-" in text:
        text = text.replace("--", 'Kommentar')
        flag = True
    if "%" in text:
        text = text.replace("%", 'Prozent')
        flag = True
    if want_flag:
        return text, flag
    else:
        return text

def handle_flag(ip):
    known_ip = sql.search_sus_ip(ip)
    if known_ip != None:
        ki_count = sql.get_sus_ip_count(ip) + 1
        sql.insert_sus_ip_count(ki_count)

def log_admin(id):
    sql.insert_admin_log(id, datetime.now(timezone.utc))

def is_blocked(ip):
    foo, err = sql.search_blocked_ip(ip)
    if err:
        return False
    return True
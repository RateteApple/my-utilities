import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText

def send_mail(from_address, password, to_address, subject, body):
    '''
    メールを送信する

    Args:
        from_address (str): 送信元のメールアドレス
        password (str): パスワード
        to_address (str): 送信先のメールアドレス
        subject (str): 件名
        body (str): 本文

    Returns:
        None

    '''
    # SMTPサーバーに接続
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    # TLS暗号化の設定
    server.starttls()
    # ログイン
    login_address = from_address 
    login_password = password
    server.login(login_address, login_password)
    # 送信メールの生成
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = from_address 
    message["To"] = to_address
    text = MIMEText(body)
    message.attach(text)
    # メールの送信
    server.send_message(message)
    # SMTPサーバーとの接続を閉じる
    server.quit()
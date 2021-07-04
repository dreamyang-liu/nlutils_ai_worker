from ubuntu:xenial
RUN apt-get update  && apt-get install -y wget sendmail && \
    wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz && \
    tar xvzf Python-3.7.6.tgz && \
    cd Python-3.7.6 && \
    ./configure && \
    make -j8 && \
    make install
RUN pip3 install --upgrade pip &&  pip3 install PyEmail
ENTRYPOINT /bin/bash


send_user = "lmy@nlutils.org"       # 发件人的邮箱账号
rec_user = "1539078757@qq.com"

msg = MIMEText("这是测试邮箱发送内容！", "plain", "utf-8")
msg["From"] = formataddr(["FromSMTPQQ", send_user])  # 括号中对应发件人邮箱昵称、发件人邮箱账号
msg["To"] = formataddr(["RecSMTP"], rec_user)  # 括号中对应收件人邮箱昵称、收件人邮箱账号
msg["Subject"] = "这是邮件的主题"  # 邮件的主题或标题
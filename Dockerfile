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
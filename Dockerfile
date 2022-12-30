FROM python:latest

# install chromium, unzip and xvfb (used to emulate chrome)
RUN apt-get update && \
    apt-get install -yq chromium \
                        xvfb \
                        unzip \
                        tzdata

# chromeDriver v90
RUN wget -q "https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

# xvfb - X server display: Xvfb is an X server that can run on machines with no display hardware and no physical input devices.
COPY xvfb-chromium /usr/bin/xvfb-chromium
RUN ln -s /usr/bin/xvfb-chromium /usr/bin/google-chrome && \
    chmod 777 /usr/bin/xvfb-chromium

# create symlinks to chromedriver (to the PATH)
RUN ln -s /usr/bin/chromium && \
    chmod 777 /usr/bin/chromium

# create project folder with the name code
RUN mkdir /code

# project scope
WORKDIR /code

# install requirements (i.e.: python modules)
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# copy the script 
COPY whatsappMessage.py .
COPY gymbot.py .

# create a use and sign as the user to run the script as non-root
#RUN adduser worker
#USER worker

#Set the timezone
ENV TZ Canada/Eastern

# execute the python script
ENTRYPOINT ["python3", "gymbot.py"]
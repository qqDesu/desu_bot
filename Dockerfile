FROM python:latest
WORKDIR /waifu_bot/
ADD 2D_bot.py /waifu_bot/
#RUN pip3 install --upgrade pip
RUN pip3 install pyTelegramBotAPI
RUN pip3 install requests
RUN pip3 install redis
COPY config.txt config.txt
CMD [ "python3", "./2D_bot.py"]

FROM python:stretch

ENV PYTHONUNBUFFERED 1

# This is important!!! Remember the port number for the Web App step
ENV PRODIGY_PORT=8081

# EXPOSE 8081

# I found the verbose logs helpful for debugging problems 
ENV PRODIGY_LOGGING=verbose

# This is your prodigy wheel thats given to you
COPY *linux_x86_64.whl /root

RUN pip install /root/prodigy*.whl 

# Download the language embeddings you need
RUN python -m spacy download en_core_web_md

# store your config & settings here
RUN mkdir -p /root/.prodigy/

# dependencies to run screenshot script
RUN pip install selenium==3.141.0
RUN apt-get update
RUN apt install nano
RUN apt install chromedriver -y
RUN apt install lsof

# Your prodigy settings
COPY prodigy.json /root/.prodigy/prodigy.json
COPY help.txt /root/.prodigy/help.txt

# Your data
COPY ./checkin_four_all_labels_download.096f6496-127f-4543-b5bc-8318659f2413_corrected.jsonl /root/
COPY ./screenshot_prepare.py /root/

# Install your database ORM/driver here + any additional installs. We're using postgreSQL 
RUN pip install psycopg2


# Put your prodigy task
# ENTRYPOINT prodigy rel.manual main_batchA en_core_web_md ./root/randomized_sentences_for_entity_labeling_batchA.jsonl --label Concept_Member,Contributes_To,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --patterns ./root/patterns.jsonl --wrap

CMD ["root/screenshot_prepare.py"]

ENTRYPOINT ["python"]
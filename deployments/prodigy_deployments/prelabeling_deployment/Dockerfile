FROM python:stretch

ENV PYTHONUNBUFFERED 1
ENV PRODIGY_PORT=8000
ENV PRODIGY_LOGGING=verbose

COPY *linux_x86_64.whl /root
RUN pip install /root/prodigy*.whl
RUN python -m spacy download en_core_web_md
RUN mkdir -p /root/.prodigy/
COPY ProdigyLicenseKey.txt /root/.prodigy/
COPY help.txt /root/.prodigy/
COPY prodigy.json /root/.prodigy/prodigy.json
COPY ./data.jsonl /root/
RUN pip install psycopg2

ENTRYPOINT prodigy prelabel_rel prelabel_test_deploy_one en_core_web_md ./root/data.jsonl  --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate
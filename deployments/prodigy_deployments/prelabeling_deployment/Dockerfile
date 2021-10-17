FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PRODIGY_PORT=8000
ENV PRODIGY_LOGGING=verbose

COPY *linux_x86_64.whl /root
RUN pip install /root/prodigy*.whl
RUN python -m spacy download en_core_web_md
RUN mkdir -p /root/.prodigy/
COPY ProdigyLicenseKey.txt /root/.prodigy/
COPY help.txt /root/.prodigy/
COPY prelabel_rel.py /root/
COPY prodigy.json /root/.prodigy/prodigy.json
COPY ./data.jsonl /root/
COPY ./pattern_matching_rules.csv /root/
RUN pip install psycopg2
RUN pip install pandas

ENTRYPOINT prodigy prelabel_rel prelabel_test_deploy_one en_core_web_md ./root/data.jsonl -l Concept_Member,Contributes_To -sl base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate -F ./root/prelabel_rel.py
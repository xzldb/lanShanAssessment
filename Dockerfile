FROM python:3.10.9
 
WORKDIR ./lanShanAssessment
 
ADD . .
 
RUN pip install -r requirements.txt

RUN apt-get update && apt -y install iputils-ping
 
CMD sleep infinity

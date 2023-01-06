FROM python:3.9
 
WORKDIR ./lanShanAssessment
 
ADD . .
 
RUN pip install -r requirements.txt
 
CMD ["python", "./src/main.py"]
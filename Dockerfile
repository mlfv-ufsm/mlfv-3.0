FROM ubuntu:18.04
COPY server/. home/MLFV/
RUN apt-get update
WORKDIR home/MLFV/
RUN apt-get install -y  python-pip
RUN pip install scikit-learn==0.20.0
RUN pip install rpyc
RUN pip install pandas
RUN pip install pydblite
RUN apt-get clean
EXPOSE 15088
EXPOSE 15089
CMD ["python", "MLFV_Module.py"]
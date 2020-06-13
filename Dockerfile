FROM clearlinux/numpy-mp:latest
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip
ENTRYPOINT ["python", "sphere.py"]

FROM clearlinux/numpy-mp:latest
COPY . /usr/src/app
WORKDIR /usr/src/app
ENTRYPOINT ["python", "sphere.py"]

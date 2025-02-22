FROM arm32v7/python:3.9

RUN apt-get update
RUN apt-get install cmake -y

# print versions
RUN python --version && curl --version

# install hello world app
RUN pip install flask gunicorn

COPY utils/build/docker/python/flask.py app.py
ENV FLASK_APP=app.py

COPY utils/build/docker/python/install_ddtrace.sh utils/build/docker/python/get_appsec_rules_version.py binaries* /binaries/
RUN /binaries/install_ddtrace.sh

# docker startup
RUN echo '#!/bin/bash \n\
ddtrace-run gunicorn -w 2 -b 0.0.0.0:7777 app:app \n' > /app.sh
RUN chmod +x /app.sh
CMD ./app.sh

# docker build -f utils/build/docker/python.flask-poc.Dockerfile -t test .
# docker run -ti -p 7777:7777 test


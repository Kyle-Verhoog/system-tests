FROM arm32v7/node:14

RUN apt-get update && apt-get install -y jq

RUN uname -r

# print versions
RUN node --version && npm --version && curl --version

COPY utils/build/docker/nodejs/express4 /usr/app

WORKDIR /usr/app

RUN npm install

EXPOSE 7777

# docker startup
RUN echo '#!/bin/sh\nnode app.js\n' > app.sh
RUN chmod +x app.sh
CMD ./app.sh

COPY utils/build/docker/nodejs/install_ddtrace.sh binaries* /binaries/
RUN /binaries/install_ddtrace.sh

# docker build -f utils/build/docker/nodejs.datadog.Dockerfile -t test .
# docker run -ti -p 7777:7777 test

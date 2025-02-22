FROM golang:1.18

# print versions
RUN go version && curl --version

COPY utils/build/docker/golang/install_ddtrace.sh binaries* /binaries/
COPY utils/build/docker/golang/app /app
COPY utils/build/docker/golang/app.sh /app/app.sh
COPY utils/build/docker/set-uds-transport.sh set-uds-transport.sh

WORKDIR /app

RUN apt-get update && apt-get -y install jq
RUN /binaries/install_ddtrace.sh
ENV DD_TRACE_HEADER_TAGS='user-agent'

RUN go build -v -tags appsec -o weblog ./echo.go ./common.go ./grpc.go ./weblog_grpc.pb.go ./weblog.pb.go

ENV DD_APM_RECEIVER_SOCKET=/var/run/datadog/apm.socket
ENV UDS_WEBLOG=1

CMD ["./app.sh"]

# Datadog setup
ENV DD_LOGGING_RATE=0

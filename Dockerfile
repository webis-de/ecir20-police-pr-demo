FROM python:3.6

COPY Query /Query/
COPY Evaluierung /Evaluierung/
COPY blaulicht-client /blaulicht-client/
COPY Topics /Topics/
COPY web-app /web-app
RUN cd /web-app && make clean && make .venv
WORKDIR /web-app

ENTRYPOINT make

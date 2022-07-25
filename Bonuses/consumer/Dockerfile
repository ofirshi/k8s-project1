FROM python:3.9-slim as builder
LABEL org.opencontainers.image.authors="75673005+chkp-ofirs@users.noreply.github.com" \
      version="1.0"
USER root
ENV PYTHONPATH /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
EXPOSE 9422/tcp
ADD --chown=app:app consumer.py /app/
ADD --chown=app:app requirements.txt /app/
ADD --chown=app:app run.sh /app/ 
RUN apt-get update && apt-get install -y \
    && apt-get install curl -y \
    && rm -rf /var/lib/apt/lists/* \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && /usr/local/bin/python -m pip install -r /app/requirements.txt
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/bash --disabled-password --uid 1001 --system --group app && \
    chmod a+x /app/run.sh
USER app
#CMD ["/usr/local/bin/python", "/app/consumer.py"]
CMD ["./run.sh"]
#ENTRYPOINT ["python", "/app/consumer.py" , "-p" , "5672", "-s", "rabbitmq" , "-m" , "Hello"]
HEALTHCHECK --interval=5m --timeout=3s CMD curl --fail http://localhost:9422 || exit 1
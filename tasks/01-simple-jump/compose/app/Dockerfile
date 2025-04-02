FROM ubuntu:24.04

RUN apt update && apt install -y socat

WORKDIR /app/

RUN chown nobody:nogroup ./

COPY src/ ./

RUN chmod +x main ./entrypoint.sh

USER nobody:nogroup

ENV FLAG="flag{redacted}"

#CMD ["socat", "TCP-LISTEN:9000,reuseaddr,fork,keepalive", "EXEC:./main"]
ENTRYPOINT ["./entrypoint.sh"]
FROM python:3.13-slim

RUN apt-get -q -y update

ENV USERNAME=repmate
ENV WORKING_DIR=/home/repmate

WORKDIR ${WORKING_DIR}

COPY migrations migrations
COPY repmate repmate
COPY requirements.txt .
COPY entrypoint.sh .

RUN groupadd ${USERNAME} && \
    useradd -g ${USERNAME} ${USERNAME}

RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH="$PATH:/home/${USERNAME}/.local/bin"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=repmate
RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]

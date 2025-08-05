#  docker build -f Dockerfile -t meenibatch/ai-py-app:latest .
# docker push meenibatch/ai-py-app:latest
# docker compose run backend /bin/bash
# docker build -f Dockerfile -t pyapp .
FROM python:latest

# create venv in optional environment
RUN python -m venv /opt/venv
#python path
ENV PATH=/opt/venv/bin:$PATH 

WORKDIR /app
#RUN mkdir -p /static_folder
#COPY local_folder/file container_destination
COPY requirements.txt /tmp/requirements.txt

# Run within container while building
RUN pip install -r /tmp/requirements.txt

COPY ./src .
#RUN echo "hello world" > index.html

# python -m http.server 8000
# docker run -t -p 8080:8000
CMD ["python", "-m", "http.server", "8000"]
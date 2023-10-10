# python image
FROM python:3.10-alpine
# copy all files to the container
COPY . .
# install dependencies
RUN pip install -r requirements.txt
# command to run on container start
CMD [ "python", "./main.py" ]
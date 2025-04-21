# use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# copy the requirements file into the container
COPY requirements.txt /app/

# install dependencies based on the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code into the container
COPY . /app

# expose the port the app runs on
EXPOSE 5000

# environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# run the application
CMD ["flask", "run", "--host=0.0.0.0"]
FROM python:3.8

WORKDIR /src

COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY files/ ./files
COPY app.py .

Expose 5000

# CMD ["sleep" , "300"]
CMD ["python" , "app.py"]
# Dockerfile
FROM apache/airflow:2.9.2

# Set the working directory
WORKDIR /opt/airflow

# Install dependencies from requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

# Add src to the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"
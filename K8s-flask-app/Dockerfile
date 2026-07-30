# stage 1: build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# copy requirements.txt first for layer caching
# if requirements.txt changes, only this layer will be rebuilt 
# if requirements.txt does not change, this layer will be cached and reused
COPY requirements.txt .

# install dependencies to separate folder to avoid polluting the final image
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# stage 2: build production image
FROM python:3.11-slim AS production

#create a non-root user and switch to it
RUN useradd -m  -u 1000 appuser

WORKDIR /app

# copy installed dependencies from builder stage
COPY --from=builder /install /usr/local 

# copy application code
COPY app/ .

# change ownership of the application code to the non-root user
RUN chown -R appuser:appuser /app
# switch to non-root user
USER appuser

# expose port 5000 for the Flask app
EXPOSE 5000 

# set the CMD to run the Flask app
CMD ["python", "app.py"]
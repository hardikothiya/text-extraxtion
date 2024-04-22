FROM python:3.8
# Set environment variables for FastAPI application
ENV APP_HOME /app
ENV PORT 8000

# Set the working directory in the container
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y antiword

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY . .

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

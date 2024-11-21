# Specify the base image to start from
FROM python:3.10-slim

# Set environment variables for Python Logs and for poetry
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies into a venv using poetry in workdir
RUN pip install --timeout=120 poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock /app/
RUN poetry install
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

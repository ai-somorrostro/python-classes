FROM python:3.11-slim

WORKDIR /src

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the build context into /src/app so the package `app` is located at
# /src/app and is importable as `app.*` when the working directory is /src.
COPY . /src/app

EXPOSE 8000

# Import the FastAPI app as a package: app.main:app
# Running from /src makes /src available on sys.path so `import app` works.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
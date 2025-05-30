FROM python:3.13-slim@sha256:026dd417a88d0be8ed5542a05cff5979d17625151be8a1e25a994f85c87962a5   
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY main.py database.py requirements.txt ./
COPY routers/*.py /app/routers/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN adduser app_user && chown -R app_user:app_user /app
USER app_user
CMD ["python", "main.py"]

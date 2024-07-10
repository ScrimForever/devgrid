FROM python:3.11-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


COPY . .

RUN chmod +x manager.sh

CMD ["./manager.sh", "&&", "fastapi", "run", "src.app"]

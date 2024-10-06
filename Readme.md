Steps:
*** python3 -m venv ./venv;source venv/bin/activate
*** pip3 install -r requirements.txt
*** uvicorn src.main:app --reload


# production
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
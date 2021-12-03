Steps:
*** python3 -m venv ./venv;source venv/bin/activate
*** pip3 install -r requirements.txt
*** cd src
*** uvicorn src.main:app --reload


# production
gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker# fastapi-python-apitemplate

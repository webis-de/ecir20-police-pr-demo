VENV-DIR = .venv
PIP = $(VENV-DIR)/bin/pip3
PYTHON = $(VENV-DIR)/bin/python3


run-server: $(VENV-DIR)
	PYTHONPATH=../Query/:../Evaluierung/:../blaulicht-client/ $(PYTHON) .venv/bin/gunicorn police_pr_web_app.wsgi -w 1 --threads 10 --timeout 1500 --bind 0.0.0.0:8000

run-test-server: $(VENV-DIR)
	PYTHONPATH=../Query/:../Evaluierung/:../blaulicht-client/ $(PYTHON) manage.py runserver

persist-examples: $(VENV-DIR)
	PYTHONPATH=../Query/:../Evaluierung/:../blaulicht-client/ $(PYTHON) persist_examples.py

clean:
	rm -Rf $(VENV-DIR)

$(VENV-DIR):
	mkdir $(VENV-DIR) &&\
	python3 -m venv .venv &&\
	$(PIP) install --upgrade pip &&\
	$(PIP) install django==2.1.5 pillow==5.4.1 bs4==0.0.1 elasticsearch==5.5.3 python-dateutil==2.8.0 gunicorn==19.9.0 whitenoise==4.1.4


eval:
	@./create-dedicated-difficulties.sh &&\
	./Evaluierung/evaluate.sh runBlaulichtTitleSearch &&\
	./Evaluierung/evaluate.sh runcomplex_query &&\
	./Evaluierung/evaluate.sh runtitle_query &&\
	./Evaluierung/evaluate.sh runfull_text_query &&\
	./Evaluierung/evaluate.sh runBlaulichtFullTextSearch

delete-from-k8s:
	kubectl --namespace webisservices delete -f deployment.yml

deploy-to-k8s:
	kubectl --namespace webisservices apply -f deployment.yml

create-police-pr-run-file:
	PYTHONPATH=blaulicht-client:Query python3 Evaluierung/evaluate2.py

create-blaulicht-run-file:
	PYTHONPATH=blaulicht-client:Query python3 Query/blaulicht_run_files.py

publish-docker:
	docker build -t mam10eks/tmp-mam10eks:0.0.14 . &&\
	docker login &&\
	docker push mam10eks/tmp-mam10eks:0.0.14

update-urls:
	docker run --rm -v ${PWD}/crawling:/crawling python:3.6-stretch bash -c "pip install requests==2.22 && python /crawling/api-request.py"

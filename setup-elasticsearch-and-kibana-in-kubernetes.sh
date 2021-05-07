#!/bin/bash -e

NAMESPACE="wstud-thesis-schwanke"
ES_NAME="${NAMESPACE}-elasticsearch"
KIBANA_NAME="${NAMESPACE}-kibana"

helm repo add elastic https://helm.elastic.co
helm repo update

helm delete ${ES_NAME} --purge || echo "ES is already deleted"
helm delete ${KIBANA_NAME} --purge || echo "Kibana is already deleted"
sleep 20s
kubectl --namespace=${NAMESPACE} delete pvc elasticsearch-master-elasticsearch-master-0 || echo "PVC is already deleted"

helm install    --namespace=${NAMESPACE} \
		--replace \
		--name ${ES_NAME} \
		--set replicas=1 \
		--set minimumMasterNodes=1 \
		--set service.type=NodePort \
		--set volumeClaimTemplate.resources.requests.storage=15Gi \
		--set service.nodePort=30770 \
		elastic/elasticsearch --version 7.2.0

sleep 5s

helm install    --namespace=${NAMESPACE} \
		--replace \
		--name ${KIBANA_NAME} \
		--set service.type=NodePort \
		--set service.nodePort=30771 \
		elastic/kibana --version 7.2.0

sleep 15s
echo "Upload synonyms_de.txt and CustomStopwords to elasticsearch-pod"

kubectl cp synonyms_de.txt wstud-thesis-schwanke/elasticsearch-master-0:/usr/share/elasticsearch/config/synonyms_de.txt
kubectl cp CustomStopwords wstud-thesis-schwanke/elasticsearch-master-0:/usr/share/elasticsearch/config/CustomGermanStopwords

echo "Done!"

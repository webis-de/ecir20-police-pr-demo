#!/bin/bash -e

SOURCE_DIR="/home/maik/workspace/wstud-thesis-schwanke/irlecture-ss18-police-pr-search/02Data"
TARGET_DIR="/home/maik/workspace/wstud-thesis-schwanke/ecir20-police-pr-demo"

rm -Rf ${TARGET_DIR}
mkdir ${TARGET_DIR}

cd ${SOURCE_DIR}
for FILE in *.json
do
	cat ${SOURCE_DIR}/${FILE}| sed 's/"_index" : "reports"/"_index" : "ecir20-police-pr-demo"/' > ${TARGET_DIR}/${FILE}
done


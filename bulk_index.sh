#! /bin/bash

# This script sets up the index setting and mappings then navigates to the consolidated test corpus and sends it to the Elasticsearch instance for bulk indexing. You'll have to start the Elasticsearch instance first for this to work. 

# Delets the index 'reports' if it exists.
ELASTICSEARCH_ADDRESS="betaweb023:9200"
INDEX="ecir20-police-pr-demo"
curl -s -X DELETE "${ELASTICSEARCH_ADDRESS}/${INDEX}?pretty"

# Creates the settings for the index 'reports' including the analyzer (which implements stopping, stemming, normalization and synonyms for german) and the mapping.
# The following is an example of a command used to test the analyzer: curl -X GET "localhost:9200/reports/_analyze?pretty" -H 'Content-Type: application/json' -d' { "analyzer" : "german", "text" : "die deutschen Männer kammen spät an." }'

curl -X PUT "${ELASTICSEARCH_ADDRESS}/${INDEX}?pretty" -H 'Content-Type: application/json' -d'
{ 
	"settings": {
	"index" : {
		"number_of_shards" : 1,
		"number_of_replicas" : 4
        },
    	"analysis": {
        	"filter": {
	            "german_stop": {
	                "type": "stop",
	                "language": "light_german"
	            },
	            "german_stemmer": {
	                "type": "stemmer",
	                "language": "light_german"
	            }
         	},
         	"analyzer": {
            	"german": {
	                "tokenizer": "standard",
	                "filter": [
	                    "lowercase",
	                    "german_stop",
	                    "german_normalization",
	                    "german_stemmer"
	                ]
             	}
        	}
    	}
	},
  	"mappings" : { 
	    "doc" : {
	      	"properties" : {
		        "ID" : {
		          	"type" : "text"
		        },
		        "URL" : {
		          	"type" : "text"
		        },
		        "body" : {
		          	"type" : "text",
		          	"analyzer": "german"
		        },
		        "keywords" : {
		          	"type" : "text"
		        },
		        "officeID" : {
		          	"type" : "text"
		        },
		        "officeName" : { 
		          	"type" : "keyword"
		        },
		        "officeURL" : {
		          	"type" : "text"
		        },
		        "published" : {
		          	"type" : "date"
		        },
		        "title" : {
		          	"type" : "text",
		          	"analyzer": "german"
		        },		        
		        "complete" : {
		        	"type" : "text"
		        }
	    	}
    	}
  	}
}'

for file in /mnt/ceph/storage/data-in-production/ecir20-police-pr-demo/*.json
do
  curl -s -H "Content-Type: application/x-ndjson" -XPOST ${ELASTICSEARCH_ADDRESS}/_bulk --data-binary @"$file"
done

# This script fills the completion field of every doc with the doc's title.
curl -X POST "${ELASTICSEARCH_ADDRESS}/${INDEX}/_update_by_query" -H 'Content-Type: application/json' -d'
{
    "script" : {
     "lang": "painless",
      "source" : "ctx._source.complete = ctx._source.title; "
    }
}
'


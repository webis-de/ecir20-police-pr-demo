from start_page_app import views
import json
examples = {}
for example in views.EXAMPLES:
    url = example['href']
    print('Fill cache for query ' + url)
    examples[url] = views.execute_query_url(url)
print('Done: Caches are filled')

with open('persisted-examples.jsonl', 'w') as f:
    json.dump(examples, f)


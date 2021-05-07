def run_file(file_name, topic_to_ranking, tag):
    with open(file_name, 'w') as f:
        f.write(create_run_file_content(topic_to_ranking, tag))

def create_run_file_content(topicToRanking, tag):
    ret = ''
    for topic in topicToRanking.keys():
        ranking = topicToRanking[topic]
        if len(ranking) == 0:
            ranking = ['EMPTY_RANKING_DOCUMENT']
        for rank, doc in enumerate(ranking):
            rank += 1
            score = len(ranking) - rank
            ret += run_line(topic, doc, score, rank, tag)
    return ret

def run_line(topic, document_id, score, rank, tag):
    return str(topic) + ' Q0 ' + str(document_id) + ' ' + str(rank) + ' ' + str(score) + ' ' + str(tag) + '\n'


from very_clevr.models import Query


def tokenize_query(query: Query):
    """Breaks the query into spaces"""
    query = query.split(" ")
    return query

import json
import gzip
from application import mongo


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


for l in parse("reviews_Books.json.gz"):
    mongo.db.reviews.insert(l)

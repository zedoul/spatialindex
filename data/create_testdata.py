#!/usr/bin/env python2
"""
    create testdata
    ~~~~~~

    Creates test data

"""

# thread has messages, and each thread has its tags 
from pandas import DataFrame, Series, HDFStore
from numpy.random import normal, uniform, randint
import hashlib

# fake data creation
messages = ["message A", "message B", "message C"]
convthread_titles = ["thread A", "thread B","thread C"]
tags = ["cafe", "school", "boring"]

message_ids = []
for message_title in messages :
    message_ids.append(hashlib.md5(message_title).hexdigest())
popularities = uniform(0,1,len(messages))

convthread_ids = []
for convthread_title in convthread_titles :
    convthread_ids.append(hashlib.md5(convthread_title).hexdigest())
lats = 59.33258 + 0.001 * normal(0,0.1,size=len(convthread_ids))
lngs = 18.06490 + 0.001 * normal(0,0.1,size=len(convthread_ids))

tag_ids = []
for tag in tags :
    tag_ids.append(hashlib.md5(tag).hexdigest())

tagging_ids = []
tagging_convthread_ids = []
tagging_tag_ids = []

for convthread_id in convthread_ids :
    tag_id = tag_ids[randint(0,len(tag_ids))]
    tagging_ids.append(hashlib.md5(convthread_id).hexdigest())
    tagging_convthread_ids.append(convthread_id)
    tagging_tag_ids.append(tag_id)

# message threads
d = {
    'message_id':Series(message_ids),
    'convthread_id':Series(convthread_ids),
    'message':Series(messages),
    'popularity':Series(popularities),
}
d = DataFrame(d)
d.to_pickle("messages.pkl")

# thread
d = {
    'convthread_id':Series(convthread_ids),
    'title':Series(convthread_titles),
    'lat':Series(lats),
    'lng':Series(lngs)
}
d = DataFrame(d)
d.to_pickle("convthreads.pkl")

# taggings
d = {
    'tagging_id':Series(tagging_ids),
    'convthread_id':Series(tagging_convthread_ids),
    'tag_id':Series(tagging_tag_ids),
}
d = DataFrame(d)
d.to_pickle("taggings.pkl")

# tags
d = {
    'tag_id':Series(tag_ids),
    'tag':Series(tags)
}
d = DataFrame(d)
d.to_pickle("tags.pkl")

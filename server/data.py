# -*- coding: utf-8 -*-
"""
    data
    ~~~~~~~~~~~~~

    A database for topics and conversation threads based on Pandas.

"""

import pandas as pd
import numpy as np

DATAFILES = {
    "messages": "messages.pkl",
    "convthreads": "convthreads.pkl",
    "taggings": "taggings.pkl",
    "tags" : "tags.pkl"
}

class Database(object):
    def __init__(self,datapath):
        #: A dataframe that contains database from datafiles 
        self.dfs = self.create_table(datapath)

    def create_table(self, datapath):
        """Create database class with pkl files. 
        """
        dfs = {}

        for key, filepath in DATAFILES.items():
            try :
                buf = '%s/%s' % (datapath, filepath)
            except IOError as e :
                assert False, "I/O error({0}): {1}".format(e.errno, e.strerror)
            except:
                import sys
                assert False, "Unexpected error: %s" % sys.exc_info()[0]
            print buf
            df = pd.read_pickle(buf)
            dfs[key] = df

        # Following codes require a bit of explanation: the basic idea is to 
        # make a refined database to boost search performance and to select 
        # database for time-consuming queries in advance. 

        # data preprocessing for "messages" datatable.
        messages_df = dfs["messages"]
        # - sorts messages by "popularity" feature in ascending order
        messages_df = messages_df.sort(['popularity'],ascending=[True])

        # data preprocessing for "convthreads" datatable
        # - selects messages for each convthread beforehand
        #   and adds "easy to read/access" convthread information for each message
        convthreads_df = dfs["convthreads"]
        for convthread_id in convthreads_df["convthread_id"].values:
            # get all messages of this convthread
            convthread_messages = messages_df[messages_df.convthread_id == convthread_id].values
            refined_convthread_messages = []
            for convthread_message in convthread_messages:
                convthread_message = list(convthread_message)
                del convthread_message[1]
                convthread_df = convthreads_df[convthreads_df.convthread_id == convthread_id]
                convthread_record = convthread_df.head(0).values.tolist()[0]
                
                record = dict(zip(["message_id","title","popularity","convthread_id"],
                    convthread_message + 
                    [dict(zip(["convthread_id", "lat", "lng", "title"], convthread_record))] 
                    ))

                refined_convthread_messages.append(record)
            dfs[convthread_id] = refined_convthread_messages
        # - creates refined database merging convthreads with tags
        convthreads_with_tags = convthreads_df.merge(dfs["taggings"], on="convthread_id")

        print convthreads_with_tags
        dfs["convthreads_with_tags"] = convthreads_with_tags

        return dfs

    def convthreads(self,tag_id=None):
        """Returns convthreads from datatable. 

        : param tag_id: if set, this method will return convthreads 
                        have ``tag_id`` only 
        """
        if None == tag_id:
            return self.dfs["convthreads"].values
        else :
            df = self.dfs["convthreads_with_tags"]
            return df[df.tag_id == tag_id].values

    def convthread(self, convthread_id):
        """Returns convthread by ``convthread_id````. 
        """

        df = self.dfs["convthreads"]
        tag_records = df[df.id == convthread_id]
        if 1 == len(tag_records): 
            return tag_records.values[0]
        elif 1 < len(tag_records): 
            raise Exception("More than one record exist by convthread_id")
        else :
            import warnings
            warnings.warn("No record matched with convthread_id", Warning)
            return None

    def tag_ids(self, convthread_id=None):
        """Returns ``tag_ids`` from datatable. 

        : param convthread_id: if set, this method will return tag_ids 
                         related to ``convthread_id`` only
        """
        if None == convthread_id:
            return [tag[0] for tag in self.dfs["tags"][["tag_id"]].values]
        else :
            df = self.dfs["convthreads_with_tags"]
            tag_records = df[df.convthread_id == convthread_id]
            return tag_records["tag_id"].values

    def tag_id(self, tag):
        """Returns ``tag_ids`` of ``tag``. 
        """
        assert isinstance(tag, str)

        df = self.dfs["tags"]
        tag_records = df[df.tag == tag]
        if 1 == len(tag_records): 
            return tag_records["id"].values[0]
        elif 1 < len(tag_records): 
            raise Exception("More than one record exist by tag")
        else :
            # We should not be strict to tag name since it is a user input.
            import warnings
            warnings.warn("No record matched with tag", Warning)
            return None

    def popular_messages(self, convthread_id):
        """Returns popular convthreads of ``convthread_id``. 
        It is sorted in ascending order.
        """
        if self.dfs.has_key(convthread_id):
            return self.dfs[convthread_id]
        else:
            import warnings
            warnings.warn("No record matched with convthread_id", Warning)
            return []


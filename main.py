import group
import page
from pymongo import MongoClient

#convert time to sort
def convertTime(str):
    from datetime import datetime
    import numpy as np
    dt = datetime.utcnow()
    ts = np.datetime64(str)
    dt64 = np.datetime64(dt)
    tsa = (dt64 - ts)/np.timedelta64(1,'s')
    return tsa

if __name__ == "__main__":
    try:

        postUpdate, postInsert = group.graphGroups()
        print()
        # postUpdatePage, postInsertPage = ([], [])
        postUpdatePage, postInsertPage = page.graphPages()
        
        for x in postUpdatePage:
            postUpdate.append(x)
        for x in postInsertPage:
            postInsert.append(x)

        if len(postInsert) > 0 or len(postUpdate) > 0 :
            # Init mongoclient 
            client = MongoClient()
            # Init connect 
            client = MongoClient('localhost', 27017)
            # Select database timtro
            db = client['timtro']
            # Select collection page
            collection = db['posts']
            bulk = collection.initialize_ordered_bulk_op()
            for post in postInsert:
                bulk.insert(post)
                # print('IN', post)
            for post in postUpdate:
                bulk.find({'_id':post['_id']}).update({'$set': {'updated_time': post['updated_time']}})

            result = bulk.execute()

            print(result)

        print('Main run success')
        exit(0)
    except Exception as e:
        print('Error', e)
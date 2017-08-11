import group
import page
from pymongo import MongoClient
import geocoder
import pprint
import requests
import json
from money import Money

def getNotificationPrice(db, pricess):
    notifications = []
    platformPrice = []
    collectionPrices = db['prices']
    index = 0
    for prices in pricess:
        index += 1
        if(len(prices) > 0):
            cursorPrices = collectionPrices.find({"_id": str(index)})
            platforms = []
            for cursorPlatform in cursorPrices:
                platforms = cursorPlatform['platform']
            for platform in platforms:
                platformPrice.append(platform['playerId'])
                for price in prices:
                    notifications.append((platform['userId'], platform['playerId'], price[1], price[0], price[2]))
    return (notifications, platformPrice)

def getNotificationLocation(db, locationss):
    notifications = []
    platformLocation = []
    collectionLocations = db['locations']
    index = 0
    for locations in locationss:
        cursorLocations = collectionLocations.find({"lat": locations[0], "lng": locations[1]})
        platforms = []
        for cursorPlatform in cursorLocations:
            platforms = cursorPlatform['platform']
        for platform in platforms:
            platformLocation.append(platform['playerId'])
            for location in locations[2]:
                notifications.append((platform['userId'], platform['playerId'], location[0], location[1], location[2]))
    return (notifications, platformLocation)

def getNotificationAll(db, postInsert):
    notifications = []
    platformAll = []
    collectionAlls = db['alls']
    index = 0
    cursorAlls = collectionAlls.find({})
    platforms = []
    for cursorAll in cursorAlls:
        platformAll.append(cursorAll['playerId'])
        for post in postInsert:
            notifications.append((cursorAll['id'], cursorAll['playerId'], post['group_id'] + '_' + post['_id'], post['created_time']))
    return (notifications, platformAll)

if __name__ == "__main__":
    try:

        postUpdate, postInsert = group.graphGroups()
        print()
        # postUpdatePage, postInsertPage = ([], [])
        # postUpdatePage, postInsertPage = page.graphPages()

        # for x in postUpdatePage:
        #     postUpdate.append(x)
        # for x in postInsertPage:
        #     postInsert.append(x)

        if len(postInsert) > 0 or len(postUpdate) > 0 :
            # Init mongoclient
            client = MongoClient()
            # Init connect
            # client = MongoClient('localhost', 27017)
            client = MongoClient('mongodb://timtro:Qu%40ng.b%40o1994@45.77.33.147:27017/timtro')
            # Select database timtro
            db = client['timtro']
            # Select collection page
            collection = db['posts']
            bulk = collection.initialize_ordered_bulk_op()
            pricess = [[],[],[],[]]
            locationss = []
            for post in postInsert:
                # print(type(post), 'Insert:',post)
                if 'address' in post:
                    g = geocoder.google(post['address'])
                    if(len(g.latlng)> 0):
                        lat = g.latlng[0]
                        lng = g.latlng[1]
                        # print(lat, lng)
                        latDu = lat % 0.02;
                        latNguyen = lat - latDu;
                        lngDu = lng % 0.02;
                        lngNguyen = lng - lngDu;
                        hasExist = False
                        for location in locationss:
                            if location[0] == latNguyen and location[1] == lngNguyen:
                                hasExist = True
                                location[2].append((post['_id'] + '' + post['group_id'], post['address'], post['created_time']))
                        if hasExist == False:
                            locationss.append((latNguyen, lngNguyen, [(post['group_id'] + '_' + post['_id'], post['address'], post['created_time'])]))
                        post['location'] = {'lat': lat, 'lng': lng}
                        print('Address', post['address'], g.latlng)
                    else:
                        post.pop('address', None)
                if 'price' in post:
                    price = int(post['price'])
                    if price < 1000000:
                        pricess[0].append((post['price'], post['group_id'] + '_' + post['_id'], post['created_time']))
                    elif price >= 1000000 and price < 2000000:
                        pricess[1].append((post['price'], post['group_id'] + '_' + post['_id'], post['created_time']))
                    elif price >= 2000000 and price < 5000000:
                        pricess[2].append((post['price'], post['group_id'] + '_' + post['_id'], post['created_time']))
                    elif price > 5000000:
                        pricess[3].append((post['price'], post['group_id'] + '_' + post['_id'], post['created_time']))

                    # print('Price', post['price'])
                bulk.insert(post)
                # print('IN', post)
            for post in postUpdate:
                # print('Update:', post)
                bulk.find({'_id':post['_id']}).update({'$set': {'updated_time': post['updated_time']}})

            result = bulk.execute()
            print(result)

            print('Tu mongo')
            pricesNoti, platformPrice = getNotificationPrice(db, pricess)
            locationsNoti, platformLocation = getNotificationLocation(db, locationss)
            allsNoti, platformAll = getNotificationAll(db, postInsert)

            print('Loc duoc')
            print(pricess)
            print(locationss)
            print(pricesNoti)
            print(locationsNoti)
            print(allsNoti)
            print(platformPrice, platformLocation, platformAll)
            collectionNotifications = db['notifications']
            bulkNotofications = collectionNotifications.initialize_ordered_bulk_op()
            for x in pricesNoti:
                bulkNotofications.insert({'userId': x[0], 'postId': x[2], 'content': 'Có phòng trọ mới giá: ' + str(Money(x[3], 'VND')), 'read': 0, 'created_time': x[4]})
            for x in locationsNoti:
                bulkNotofications.insert({'userId': x[0], 'postId': x[2], 'content': 'Có phòng trọ mới tại: ' + str(x[3]), 'read': 0, 'created_time': x[4]})
            for x in allsNoti:
                bulkNotofications.insert({'userId': x[0], 'postId': x[2], 'content': 'Có phòng trọ mới', 'read': 0, 'created_time': x[3]})

            resultNotofications = bulkNotofications.execute()
            print(bulkNotofications)

            platformToPush = platformPrice + platformLocation + platformAll
            print(platformToPush)
            header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Basic NDYyODdlZTMtOGU3My00YjAwLWFhNmMtNWYyMWZhM2NlZjgw"}
            payload = {"app_id": "f7e1a174-3a0c-43ce-96dd-720fcb5d0b97",
           "include_player_ids": platformToPush, "contents": {"en": "Có phòng trọ mới"}, "template_id":"7c3f5519-229b-42e1-b5d1-539649c19e0b", "url":"http://tronhanh.net"}
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
            print(req)
            print(req.status_code, req.reason)

        print('Main run success')
        exit(0)
    except Exception as e:
        print('Error', e)

import urllib.request
import json
import ssl
import os, errno
import pymongo
import datetime
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import dateutil.parser as dateparser
from operator import itemgetter

import handleFileJson

def makeGroupIdReady():
    try:
        # Read setting json
        setting = handleFileJson.readJson('data/settingJson.json')

        # Read group and page json
        groupAndPage = handleFileJson.readJson('data/groupAndPage.json')
        groups = []
        
        context = ssl._create_unverified_context()
        for obj in groupAndPage:
            # If type == 0 is group, 1 is page
            if( obj['type'] == '1' ):
                # If id == '', get id
                if( obj['id'] == '' ):
                    print('Group hasn\'t id ', obj)
                    urlGetGroupInfo = setting['apiURL'] + "search?q=" + obj['name'] + "&type=page&" + setting['accessToken']
                    print('Get group id: ', urlGetGroupInfo)
                    f = urllib.request.urlopen(urlGetGroupInfo, context=context)
                    fJSON = json.loads(f.read())
                    data = fJSON['data'][0]
                    obj['id'] = data['id']
                    print('Group has id: ', obj)
                groups.append(obj)  
        
        # Overwite group and page json
        handleFileJson.writeJson('data/groupAndPage.json', groupAndPage)

        # Return groups json and setting json
        return (groups, setting)

    except Exception as e:
        print("Error", e)

def makeGroupPathReady(groupId):
    try:
        # If path doesn't exists, create
        directory = 'data/pages/' + groupId + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
            # Create file info
            fileInfo = directory + "info.json"
            with open(fileInfo, 'w') as outfile:
                json.dump(json.loads('{"lastPostId": "0"}'), outfile)

    except Exception as e:
        print("Error", e)
def filterPost(posts):
    keysBad = [" đồ ăn ","nhân viên"," tín dụng "," đào tạo ", " sản phẩm "," đặc trị ", " hàng ", " da trắng ", " mất ", " gầy ", " ăn ", " ship ", " ctv ", " tuyển ", " sim ", " số đẹp ", " đầu số ", " bán ", " cung cấp ", " thanh lý "]
    try:
        results = []
        # Loop all post
        for post in posts:
            # If post has field messenge
            if post.get('message'):
                post['message'] = post['message'].lower()
                message = post['message']
                # Check true post
                truePost = True
                for key in keysBad:
                    if message.find(key) > -1:
                        truePost = False
                        break
                # If true post, add tu results
                if truePost is True:
                    results.append(post)
        # Return results
        return results

    except Exception as e:
        print("Error", e)
def getPhone(str):
	phone = ''
	# tim 01
	count01 = str.count('01')
	if count01 == 0:
		return phone
	if count01 == 1:
		index = str.find('01')
		phone =  str[index:index+11]
		if phone.isdigit():
			return phone
		else:
			phone = ''
	else:
		last = str.find('01')
		while last != -1:
			phone = str[last:last+11]
			if phone.isdigit():
				return phone
			else:
				phone = ''
			last = str.find('01', last+2, len(str))
	#tim 09
	count09 = str.count('09')
	#print count09
	if count09 == 0:
		return phone
	if count09 == 1:
		index = str.find('09')
		phone =  str[index:index+10]
		if phone.isdigit():
			return phone
		else:
			phone = ''
	else:
		last = str.find('09')
		while last != -1:
			phone = str[last:last+10]
			if phone.isdigit():
				return phone
			else:
				phone = ''
			last = str.find('09', last+2, len(str))
	#tim 08
	count08 = str.count('08')
	#print count08
	if count08 == 0:
		return phone
	if count08 == 1:
		index = str.find('08')
		phone =  str[index:index+10]
		if phone.isdigit():
			return phone
		else:
			phone = ''
	else:
		last = str.find('08')
		while last != -1:
			phone = str[last:last+10]
			if phone.isdigit():
				return phone
			else:
				phone = ''
			last = str.find('08', last+2, len(str))
	#tim so may ban 11 s0
	count02 = str.count('02')
	#print count02
	if count02 == 0:
		return phone
	if count02 == 1:
		index = str.find('02')
		phone =  str[index:index+11]
		if phone.isdigit():
			return phone
		else:
			phone = ''
	else:
		last = str.find('02')
		while last != -1:
			phone = str[last:last+11]
			if phone.isdigit():
				return phone
			else:
				phone = ''
			last = str.find('02', last+2, len(str))
	#tim so may ban 10 s0
	count02 = str.count('02')
	#print count02
	if count02 == 0:
		return phone
	if count02 == 1:
		index = str.find('02')
		phone =  str[index:index+10]
		if phone.isdigit():
			return phone
		else:
			phone = ''
	else:
		last = str.find('02')
		while last != -1:
			phone = str[last:last+10]
			if phone.isdigit():
				return phone
			else:
				phone = ''
			last = str.find('02', last+2, len(str))
	return phone
def getPrice(str):
    keyPrice = ["giá phòng:","giá:", "giá","giá tầm","tầm ", "giá khoảng", "giá từ", "giá dưới","khoảng ", "tháng"]
    keyFindRes = ["triệu/", "triệu", "triệu.","trieu/","trieu","trieu.","tr/","tr5", "tr ","tr.","k/ ","0k ","0k.","5k "]
    price = ''
    #tim nguoc với <-keyFindRes
    test = 1
    try:
        for key in keyFindRes:  
            index = str.find(key)
            if index > 8:
                for i in range(index - 8, index):
                    if str[i].isdigit():
                        for j in range(i, index):
                            price += str[j]
                        if index == (len(str) - 1):
                            return price + key
                        for k in range(index + 1, len(str)-1):
                            if str[k].isdigit():
                                price+=str[k]
                            else:
                                return price + key
                        return price + key
                break
        if price == '':
            # tim xuoi
            for keyx in keyPrice:
                indexx = str.find(keyx)
                if indexx > -1:
                    temp = str.split(keyx,1)[1]
                    end = -1
                    keyT = ''
                    for keyE in keyFindRes:
                        end = temp.find(keyE)
                        if end > -1:
                            keyT = keyE
                            break
                    if end > -1:
                        for x in range(0, end):
                            price += temp[x]
                        price += keyT
                    else:
                    #tim khi ko co keyEnd
                        ii = indexx
                        for z in range(indexx,len(temp)-1):
                            if z.isdigit():
                                for t in range(ii, len(temp) - 1):
                                    if t.isdigit():
                                        price += temp[t]
                                    else:
                                        return price
                            ii = ii + 1  
                    break
    except Exception as e:
        price = ''
    return ''
def findInfoOfPost(posts):
    # keysPhone = ["lh ", "sđt ", "số điện thoại", "lh :", "sđt :", "số điện thoại :", "lh:", "sđt:", "số điện thoại:"] # call 
    keysAddress = ["ở khu vực", "khu vực", "gần trường","gần trg","ở hẻm", "gần chợ", "gần trung tâm","gần phường","trên đường","hẻm","hem", "gần chỗ","ở chỗ","gần khu","địa chỉ","ở gần", "ở tại","ở ngay", "gần","phường", "tại", "đường ", "đc","đ/c","d/c","gần cầu","chỗ cầu"]
    try:
        results = []
        # Loop all post
        for post in posts:
            # print(post['updated_time'])

            updated_time = int(dateparser.parse(post['updated_time']).timestamp())
            created_time = int(dateparser.parse(post['created_time']).timestamp())

            message = post['message'].lower()
            # print(message)
            phone = ""
            address = ""
            price = ""
            postId = post['id']
            # Find phone
            phone = getPhone(message)
            # Find price
            price = getPrice(message).replace('/','').replace('k','000').replace('tr1','100000').replace('tr2','200000').replace('tr4','400000').replace('tr5','500000').replace('tr6','600000').replace('tr7','700000').replace('tr8','800000').replace('tr9','900000').replace('tr5','500000').replace('tr','000000').replace('triệu','000000').replace('trieu','000000').replace(' ','')
            if price.isdigit():
                price = price
            else:
                price = ''
            # Find address
            for key in keysAddress:
                index = message.find(key)
                if index > -1:
                    # print(message)
                    temp = message.split(key,1)[1]
                    temp = temp.split('\n')[0]
                    if key =='chợ' or key == 'trường' or key == 'truog' or key == 'phường' or key == 'phuong' or key == 'truong' or key == 'trường' or key =='cầu' or key == 'cau' or key == 'hem' or key == 'hẻm':
                        address = key
                    keysEndAddress = [".","(",")","sđt","sdt","có","ai biết","xuống","của", "không","ko","khong","bạn nào","gần","ai có nhu cầu","ai","bạn","hoặc", "...", "\n", "1tr", "1.5tr", "2tr", "triệu","cho"]
                    end = -1
                    for keyEnd in keysEndAddress:
                        end = temp.find(keyEnd)
                        if end > -1:
                            break
                    n = len(temp)
                    if end == -1:
                        if n > 30:
                            end = 30
                        else:
                            end = n
                    for x in range(0 , end):
                        address += temp[x]
                    # print(index, end, '*** DIA CHI:', address)
                    break
            address = address.replace('gần','')
            typePost = '0'
            objPost = {}
            objPost['_id'] = postId.split('_')[1]
            objPost['group_id'] = post['group_id']
            objPost['created_time'] = created_time
            objPost['updated_time'] = updated_time
            objPost['type'] = typePost
            if address is not "":
                if len(address) > 3:
                    objPost['address'] = address +', Đà Nẵng'
                else:
                    objPost['address'] = 'Đà Nẵng'
                
            if price is not "":
                objPost['price'] = price
            if phone is not "":
                objPost['phone'] = phone
        return results
    except Exception as e:
        print("Error", e)

def readGroupInfoFromFile(groupId):
    try:
        infoFile = 'data/pages/' + groupId + "/" + 'info.json'
        info = handleFileJson.readJson(infoFile)
        return info
    except Exception as e:
        print("Error", e)

def graphPages():
    try:
        # Ready group from file
        groupReady, setting = makeGroupIdReady()
        print('1. Pages info:', groupReady)

        context = ssl._create_unverified_context()
        # Loop every group
        for group in groupReady:
            # Check path ready
            makeGroupPathReady(group['id'])

            urlGraphGroupFeeds = setting['apiURL'] + group['id'] + "/feed?fields=created_time,updated_time,message&limit=" + str(setting['numOfFeeds']) + '&' + setting['accessToken']
            print('2. Graph group feed: ', urlGraphGroupFeeds)
            f = urllib.request.urlopen(urlGraphGroupFeeds, context=context)
            fJSON = json.loads(f.read().decode('utf-8'))
            posts = filterPost(fJSON['data'])

            # Init mongoclient 
            client = MongoClient()
            # Init connect 
            client = MongoClient('localhost', 27017)
            # Select database timtro
            db = client['timtro']
            # Select collection page
            collection = db['posts']

            postsMongoCursors = collection.find({"group_id": group['id']}).sort("created_time", pymongo.DESCENDING).limit(100)
            
            # Cursor mongo to array _id
            postsMongo = []
            for postMongoCursor in postsMongoCursors:
                postsMongo.append(postMongoCursor['_id'])

            # Find what post are new, or exist in mongodb
            postNew = []
            postUpdate = []
            for post in posts:
                post['group_id'] = group['id']
                post['_id'] = post['id'].split('_')[1]
                postExist = False
                for postM in postsMongo:
                    if post['_id'] == postM:
                        postExist = True
                        objPost = {}
                        objPost['_id'] = postM
                        objPost['updated_time'] = post['updated_time']
                        postUpdate.append(objPost)
                        break
                if postExist is False:
                    postNew.append(post)
            postUpdate.sort(key=itemgetter('updated_time'), reverse=True)
            postUpdate = postUpdate[:30]
            print('3. Update', len(postUpdate))

            postInsert = findInfoOfPost(postNew)
            if len(postInsert) > 0:
                postInsert.sort(key=itemgetter('created_time'))
                
            print('4. Insert', len(postInsert))

            return (postUpdate, postInsert)
        # Graph success
    except Exception as e:
        print("Error", e)

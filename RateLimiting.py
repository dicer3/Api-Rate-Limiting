from flask import Flask,request,abort
import redis
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
def SuccessCountReturn(count):
	#return according to count which successfull ping has to be returned
	if count==1:
		return "1st Successful Ping" 
	elif count==2: 
		return "2nd Successfull Ping"
	elif count==3:
		return "3rd Successful Ping"
	else:	
		return str(count)+"th Successful Ping"
def ClearAllKeys():
	global client #making Redis Client global so it could used in this function
	AllKeys=client.keys()#Retrieve all keys
	for key in AllKeys:
		client.delete(key)#Deleting all keys
def DecodeHashvalue(HashValue):
	#----
	#  The Hash Value obtained from is of bytes form
	#  It has to be converted to integer to processed
	#----
	encoding = 'utf-8'
	HashValue=str(HashValue, encoding)#Matched with utf decoding 
	HashValue=int(HashValue)#Converted to integer
	HashValue=HashValue-1
	return HashValue
def RateLimiter(thersold,IpHash):
	
	global client
	if client.exists(IpHash)==False:#Checking if specfic Hash key exists
	   client.set(str(IpHash),1,ex=time)#if not then making it's Hash Value as 1 and setting it's expiry time as 10 secs
	   DevRouteSucc=True
	   count=1
	else:
		client.incr(IpHash)#incrementing the Hash Value Everytime
		HashValue=client.get(IpHash)
		HashValue=DecodeHashvalue(HashValue)
		if HashValue>=int(thersold):#if Hash Value exceeds the Thersold then limit has exceeded
			DevRouteSucc=False #setting DevRouteSucc according limit is excedded or not 
		else:
			DevRouteSucc=True	
		count=HashValue+1 #making count value as how many times user has accessed the Route 
	return DevRouteSucc,count

global time,client,DefaultRouteRate
time=10
client=redis.Redis(host='localhost',port=6379) #Defining Redis Object with port Number 6379
DefaultRouteRate=10 #Setting Default Route Rate as 10
@app.route("/developers",methods=["POST"])
def developers():
	message=request.get_json(force=True) #Retriving Message got from Request
	reset=message['reset']
	if reset==True:#if reset value is True reset all the keys
		ClearAllKeys()
	ThDevRoute=message['ThDevRoute']	
	global DefaultRouteRate	
	if not ThDevRoute.strip(): #if string is empty setting Default Route Rate
		ThDevRoute=DefaultRouteRate
	ip=request.remote_addr #Retriving ip
	IpHash=ip+str("developers") #adding route name so it differentiated from other route
	success,count=RateLimiter(ThDevRoute,IpHash)
	if success==False:
		abort(401) #if limit has been exceeded then abort the call 
	else:
		return SuccessCountReturn(count)  #else return success count that how many times request has been processed

@app.route("/organisations",methods=["POST"])
def organisations():
	message=request.get_json(force=True) #Retriving Message got from Request
	reset=message['reset'] #if reset value is True reset all the keys
	if reset==True:
		ClearAllKeys()
	global DefaultRouteRate
	ThOrgRoute=message['ThOrgRoute']
	if not ThOrgRoute.strip(): #if string is empty setting Default Route Rate
		ThOrgRoute=DefaultRouteRate 
	ip=request.remote_addr #Retriving ip
	IpHash=ip+str("organisations") #adding route name so it differentiated from other route
	success,count=RateLimiter(ThOrgRoute,IpHash)
	if success==False: 
		abort(401) #if limit has been exceeded then abort the call 
	else:
	   return SuccessCountReturn(count) #else return success count that how many times request has been processed
	
if __name__=="__main__":
	app.run()
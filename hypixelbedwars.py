import requests,time,sys,math
from mojang import API
api = API()
key=""
#key = "c1bb38ba-bfdf-46bf-a421-abf38b73b478"
def setkey():
    global key
    with open("bwconfig.txt",'r') as f:
        key=f.readlines()[0].split()[0]

def getguildmemberuuids(guild):
    uuidlist=[]
    data = requests.get(
        url = "https://api.hypixel.net/guild",
        params = {
            "key": key,
            "name": guild
        }
    ).json()

    members=data['guild']['members']
    for member in members:
        uuid=member['uuid']
        print(uuid)
        uuidlist.append(uuid)

    return uuidlist

def getign(uuid):
    ign = api.get_username(uuid)
    return ign

def getuuid(ign):
    uuid=api.get_uuid(username=ign)
    return uuid

def getignlist(uuidlist):
    ignlist=[]
    for uuid in uuidlist:
        ign=getign(uuid)
        ignlist.append(ign)
    return ignlist

def getfinals(uuid):
    
    statuscode=0
    while statuscode!=200:
        data = requests.get(
            url = "https://api.hypixel.net/player",
            params = {
                "key": key,
                "uuid": uuid
            }
        )
        statuscode=data.status_code
        if statuscode!=200:
            print("Error stat checking. Delaying before trying again")
            time.sleep(10)
    totaldata=data.json()
    try:
        statdata=totaldata['player']['stats']['Bedwars']
        leveldata=totaldata['player']['achievements']
        star = leveldata['bedwars_level']
    except:
        return None
    try: fk=statdata['final_kills_bedwars'] 
    except: fk=0
    try: fd=statdata['final_deaths_bedwars']
    except: fd=0
    if fd!=0: fkdr=round(fk/fd,2)
    else: fkdr=fk
    rank = getrank(totaldata=totaldata)
    dict={"fk":fk,"fd":fd,"fkdr":fkdr,"star":star,"rank":rank}
    return dict

def getstats(ign):
    try:
        uuid=getuuid(ign)
    except:
        return "Account doesn't exist"
    finals=getfinals(uuid)
    if finals==None:
        return "Account has not played bedwars."
    return f'[{finals["star"]}] [{finals["rank"]}] {ign}\tFinals: {finals["fk"]}\tFinal deaths: {finals["fd"]}\n\tFKDR: {finals["fkdr"]}\tFinals per star: {math.floor(finals["fk"]/finals["star"])}'

def checkMVPpp(totaldata):
    try:
        month=totaldata['player']['monthlyPackageRank']
        if month=="SUPERSTAR":
            return True
        else:
            #Have had mvp++ before. return False
            return False
    except KeyError:
        return None

def getformattedrank(rank):
    rankdict={
        "VIP":"VIP",
        "VIP_PLUS":"VIP+",
        "MVP":"MVP",
        "MVP_PLUS":"MVP+",
        "NON":"non"
    }
    try:
        return rankdict[rank]
    except KeyError:
        return rank

def getrank(totaldata):
    try:
        rank=totaldata['player']['newPackageRank']
    except KeyError:
        rank="NON"
    if checkMVPpp(totaldata):
        rank="MVP++"
    else:
        rank=getformattedrank(rank)
    return rank

def main():
    setkey()
    while True:
        player=input("Username:\t")
        if player=="exit":
            sys.exit()
        print("\n"+getstats(player)+"\n")

if __name__=="__main__":
    main()
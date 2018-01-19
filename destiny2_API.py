import requests
import json

#Bungie membership ID     : 17673335
#Bungie memberShip Type   : 254
#Destiny 2 display name   : guitarhead42#1725
#Destiny 2 membership ID  : 4611686018472070177
#Destiny 2 character ID   : 2305843009310558777 (0 to access all characters on account)
#Destiny 2 membershipType : 4

#query component code     : "/?lc=en&components=100, 101,.."
#Destiny componenets      :  https://bungie-net.github.io/#/components/schemas/Destiny.DestinyComponentType

#EXAMPLE of query to get specific value from JSON file:
#   print (r.json()["Response"]["raid"]["allTime"]["highestCharacterLevel"]["basic"]["displayValue"])   

HEADERS = {"X-API-Key":'3065cd06b2144575996ebf0844ced696'}

#base URL for all Destiny 2 related calls
base_url = "https://www.bungie.net/platform/Destiny2" 

def jsonify_to_console(request):
    print (request)         #prints <202> or <404> response from server
    jsonify = request.json()
    print(jsonify)          #prints actual data in JSON form to console

def dump_json_to_file(filename, json_data):
    #request = request.json()
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)
    
def authorize():
    r = requests.get("https://www.bungie.net/en/OAuth/Authorize", headers=HEADERS)
    return r

def searchUsers(query):
    tack = "?q=" + query
    r = requests.get("https://www.bungie.net/platform/User/SearchUsers/" + tack, headers=HEADERS)
    #print (r.json())
    return r.json()

def getEquippedInventory(destinyMembershipType, destinyMembershipId):    
    r = requests.get(base_url + "/" + str(destinyMembershipType) + "/Profile/" + str(destinyMembershipId) + "/?lc=en&components=205", headers=HEADERS);
    return r.json()

def getMembershipsById(membershipId, membershipType):    
    r = requests.get("https://www.bungie.net/platform/User/GetMembershipsById/" + str(membershipId) + "/" + str(membershipType) + "/", headers=HEADERS);
    return r.json()

def getManifest():
    r = requests.get(base_url + "/Manifest", headers=HEADERS)
    return r.json()

def getHistoricalStats(destinyMembershipType, destinyMembershipId, characterId):
    r = requests.get(base_url + "/"+ str(destinyMembershipType) + "/Account/" + str(destinyMembershipId) + "/Character/" + str(characterId) + "/Stats/", headers=HEADERS);
    return r.json()

def getActivityHistory(destinyMembershipType, destinyMembershipId, characterId, activity_mode):    
    r = requests.get(base_url + "/" + str(destinyMembershipType) + "/Account/" + str(destinyMembershipId) + "/Character/" + str(characterId) + "/Stats/Activities/?lc=en&components=" + str(activity_mode), headers=HEADERS);
    return r.json()
    
def getCharacter(destinyMembershipType, destinyMembershipId):    
    r = requests.get(base_url + "/" + str(destinyMembershipType) + "/Profile/" + str(destinyMembershipId) + "/?lc=en&components=200", headers=HEADERS);
    return r.json()

def destinyManifestRequestStatDefinition(stat_id):
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/DestinyStatDefinition/" + str(stat_id) + "/", headers=HEADERS)
    return r.json()
    
def destinyManifestRequestInventoryDefinition(hash_id):
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/DestinyInventoryItemDefinition/" + str(hash_id) + "/", headers=HEADERS)
    return r.json()

def updateLocalFiles():
    #authorize()                 #WIP

    print ("Getting profile...")
    r = getEquippedInventory(4, 4611686018472070177)         #working    
    dump_json_to_file('d2_user_equipped_inventory.json', r)
    print ("    " + r['ErrorStatus'])
    print ("    Output succesfully dumped to file d2_user_equipped_inventory.json")

    print ("Getting D2 memberships by Bungie ID...")
    r = getMembershipsById(17673335, 254)    #working
    dump_json_to_file('d2_memberships_by_id_data.json', r)
    print ("    " + r['ErrorStatus'])
    print ("    Output succesfully dumped to file d2_memberships_by_id_data.json")
    
    print ("Getting D2 Manifest...")
    r = getManifest()           #working
    dump_json_to_file('d2_manifest.json', r)
    print ("    " + r['ErrorStatus'])
    print ("    Output succesfully dumped to file d2_manifest.json")

    print ("Getting D2 Character Stats...")
    r = getCharacter(4, 4611686018472070177)          #working
    dump_json_to_file('d2_character_data.json', r)
    print ("    " + r['ErrorStatus'])
    print ("    Output succesfully dumped to file d2_character_stats.json")

    print ("Getting D2 Character Historical Stats...")
    r = getHistoricalStats(4, 4611686018472070177, 2305843009310558777)    #working
    dump_json_to_file('d2_historical_data.json', r)
    print ("    " + r['ErrorStatus'])
    print ("    Output succesfully dumped to file d2_historical_data.json")
    print ()
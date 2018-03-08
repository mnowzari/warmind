import json
import requests
import destiny2_API as d2

#data = load_json_file("d2_historical_data.json")
#print (data["Response"]["raid"]["allTime"]["highestCharacterLevel"]["basic"]["displayValue"])

membershipID          = 0
membershipType        = -1 #or 254 for PC-only
destinyMembershipType = 0
destinyMembershipID   = 0
destinyCharacters     = []

def load_json_file(filename):
    data = 0
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def reset_access_information():
    global membershipID, destinyMembershipType, destinyMembershipID, destinyCharacters
    membershipID = 0
    membershipType = -1
    destinyMembershipType = 0
    destinyMembershipID = 0
    destinyCharacters = []
    
def get_access_information(username): #returns array of access creds 
    global membershipID, destinyMembershipType, destinyMembershipID, destinyCharacters
    access_info = []

    if membershipID == 0:
        info = d2.searchUsers(username)

        if len(info['Response']) > 0:
            
            membershipID = int(info['Response'][0]['membershipId'])

            info = d2.getMembershipsById(membershipID, membershipType)

            if 'destinyMemberships' in info['Response'] and len(info['Response']['destinyMemberships']) > 0:
                destinyMembershipType = int(info['Response']['destinyMemberships'][0]['membershipType'])
                destinyMembershipID = int(info['Response']['destinyMemberships'][0]['membershipId'])

                character = d2.getCharacter(destinyMembershipType, destinyMembershipID)
                if character['ErrorCode'] != 1601: #in the event Bungie's servers cannot find a Destiny account
                    character = character['Response']['characters']['data']

                    for key, value in character.items():
                        destinyCharacters.append(key)
                        
                    access_info = [membershipID, membershipType, destinyMembershipType, destinyMembershipID, destinyCharacters]
                    return access_info
                else: 
                    return 0
            else:
                return 0
        else: 
            return 0
    
def print_basic_info(data):
    print ()
    print ("Bungie and Destiny 2 Account Data")
    print ("------------------------------------------------------------------------------")
    print ("-Display Name               : " + data['Response']['bungieNetUser']['displayName'])
    print ("-Bungie Membership ID       : " + data['Response']['bungieNetUser']['uniqueName'])
    print ("-Destiny 2 Membership ID    : " + data['Response']['destinyMemberships'][0]['membershipId'])

    membershipType = data['Response']['destinyMemberships'][0]['membershipType']

    if (membershipType == 0):
        print ("-Destiny 2 Membership Type  : " + str(data['Response']['destinyMemberships'][0]['membershipType']) + " (None)")
    elif (membershipType == 1):
        print ("-Destiny 2 Membership Type  : " + str(data['Response']['destinyMemberships'][0]['membershipType']) + " (Xbox)")
    elif (membershipType == 2):
        print ("-Destiny 2 Membership Type  : " + str(data['Response']['destinyMemberships'][0]['membershipType']) + " (PlayStation)")
    elif (membershipType == 4):
        print ("-Destiny 2 Membership Type  : " + str(data['Response']['destinyMemberships'][0]['membershipType']) + " (PC)")
    print ()
#the following are helper functions for determining race, gender, and class names from the given int values
def parse_race(race_type):
    if race_type == 0:
        return "Human"
    elif race_type == 1:
        return "Awoken"
    elif race_type == 2:
        return "Exo"
    elif race_type == 3:
        return "Unknown"

def parse_gender(gender_type):
    if gender_type == 0:
        return "Male"
    elif gender_type == 1:
        return "Female"
    elif gender_type == 2:
        return "Unkown"

def parse_class(class_type):
    if class_type == 0:
        return "Titan"
    elif class_type == 1:
        return "Hunter"
    elif class_type == 2:
        return "Warlock"
    elif class_type == 3:
        return "Unknown"

def print_character_sheet(data):
    global destinyMembershipType
    global destinyMembershipID
    print ()
    print ("Destiny 2 Character Sheet")
    print ("------------------------------------------------------------------------------")
    
    data = data['Response']['characters']['data']
    #i = 1
    for key, value in data.items(): #key is the character ID. This is to handle accounts with more than one character
        print ("Character ID: ", key)
        print ("    Race   : " + parse_race(data[key]['raceType']))
        print ("    Gender : " + parse_gender(data[key]['genderType']))
        print ()
        print ("    Class  : " + parse_class(data[key]['classType']))
        print ("    Level  : " + str(data[key]['baseCharacterLevel']))
        print ("    Power  : " + str(data[key]['light']))
        print ()
        
        stats = data[key]['stats'] #The following makes an API call to determine stat names from the hash codes
        for i, k in stats.items():
            
            stat_def = d2.destinyManifestRequestStatDefinition(i)
            
            if 'name' in stat_def['Response']['displayProperties']:
                name = stat_def['Response']['displayProperties']['name']
                if name != 'Power':
                    if stats[i] != 0:
                        print ("    " + name + ": " + str(stats[i]))
        
        print ()
        print ("    Level Cap              : " + str(data[key]['levelProgression']['levelCap']))
        print ("    Weekly Progress        : " + str(data[key]['levelProgression']['weeklyProgress']))
        print ("    Daily Progress         : " + str(data[key]['levelProgression']['dailyProgress']))
        print ("    Progress to Next Level : " + str(data[key]['levelProgression']['progressToNextLevel']))
        print ()
        
        time_spent_playing = round(int(data[key]['minutesPlayedTotal']) / 60)
        
        inven_data = d2.getEquippedInventory(destinyMembershipType, destinyMembershipID)
        inven_data = inven_data['Response']['characterEquipment']['data']
        items = inven_data[key]["items"]
        
        print ("    Equipped Items:")
        for t in range (0, len(items)):
            hash_id = items[t]['itemHash']
            name_json = d2.destinyManifestRequestInventoryDefinition(hash_id)
            name = name_json['Response']['displayProperties']['name']
            type_and_tier = name_json['Response']['itemTypeAndTierDisplayName']
            if (type_and_tier != ""): 
                type_and_tier = ", " + type_and_tier
            print ("     -" + name + type_and_tier)
            t = t + 1
        
        print ()
        print ("    ~"+ str(time_spent_playing) + " hours on record")

def historical_data_helper(data):
    kills = int(data['kills']['basic']['displayValue'])
    deaths = int(data['deaths']['basic']['displayValue'])
    print ("    Efficiency             : " + data['efficiency']['basic']['displayValue'])
    print ("    Total Kills            : " + str(kills))
    print ("    Total Deaths           : " + str(deaths))
    print ("    Assists                : " + data['assists']['basic']['displayValue'])
    print ("    K/D                    : " + str(kills/deaths))
    print ()
    print ("    Best Weapon Type       : " + data['weaponBestType']['basic']['displayValue'])
    print ("    Precision Kills        : " + data['precisionKills']['basic']['displayValue'])
    print ("    Longest Kill Distance  : " + data['longestKillDistance']['basic']['displayValue'] + "m")
    print ("    Average Kill Distance  : " + data['averageKillDistance']['basic']['displayValue'] + "m")

    print ("        -Grenade Kills           : " + data["weaponKillsGrenade"]['basic']['displayValue'])
    print ("        -Melee Kills             : " + data["weaponKillsMelee"]['basic']['displayValue'])
    print ("        -Sidearm Kills           : " + data["weaponKillsSideArm"]['basic']['displayValue'])
    print ("        -Handcannon Kills        : " + data["weaponKillsHandCannon"]['basic']['displayValue'])
    print ("        -SMG Kills               : " + data["weaponKillsSubmachinegun"]['basic']['displayValue'])
    print ("        -Pulse Rifle Kills       : " + data["weaponKillsPulseRifle"]['basic']['displayValue'])
    print ("        -Auto Rifle Kills        : " + data["weaponKillsAutoRifle"]['basic']['displayValue'])
    print ("        -Shotgun Kills           : " + data["weaponKillsShotgun"]['basic']['displayValue'])
    print ("        -Scout Rifle Kills       : " + data["weaponKillsScoutRifle"]['basic']['displayValue'])
    print ("        -Sniper Rifle Kills      : " + data["weaponKillsSniper"]['basic']['displayValue'])
    print ("        -Rocket Launcher Kills   : " + data["weaponKillsRocketLauncher"]['basic']['displayValue'])
    print ("        -Grenade Launcher Kills  : " + data["weaponKillsGrenadeLauncher"]['basic']['displayValue'])
    print ("        -Trace Rifle Kills       : " + data["weaponKillsTraceRifle"]['basic']['displayValue'])
    print ("        -Fusion Rifle Kills      : " + data["weaponKillsFusionRifle"]['basic']['displayValue'])
    print ("        -Grenade Launcher Kills  : " + data["weaponKillsGrenadeLauncher"]['basic']['displayValue'])
    print ("        -Sword Kills             : " + data["weaponKillsSword"]['basic']['displayValue'])
    print ("        -Relic Kills             : " + data["weaponKillsRelic"]['basic']['displayValue'])
    print ("        -Ability Kills           : " + data["weaponKillsAbility"]['basic']['displayValue'])
    print ("        -Super Kills             : " + data["weaponKillsSuper"]['basic']['displayValue'])
    print ()
    print ("    Best Single-Game Kills  : " + data['bestSingleGameKills']['basic']['displayValue'])
    print ("    Longest Killing Spree   : " + data['longestKillSpree']['basic']['displayValue'])
    print ()
    print ("    Orbs Dropped            : " + data['orbsDropped']['basic']['displayValue'])
    print ("    Orbs Gathered           : " + data['orbsGathered']['basic']['displayValue'])
    print ()
    print ("    Suicides                : " + data['suicides']['basic']['displayValue'])
    print ("    Average Lifespan        : " + data['averageLifespan']['basic']['displayValue'])
    print ("    Resurrections Performed : " + data['resurrectionsPerformed']['basic']['displayValue'])
    print ("    Resurrections Recieved  : " + data['resurrectionsReceived']['basic']['displayValue'])
    print ()
        
def print_historical_strike_data(input_data):
    print ("***All Historical Strike Data***")
    if 'allTime' in input_data['Response']['allStrikes']:
        data = input_data['Response']['allStrikes']['allTime']
        historical_data_helper(data)
        print ("    "+ data['secondsPlayed']['basic']['displayValue'] + " spent in activity")
        print ()
    else:
        print ("NO DATA FOUND FOR THIS GUARDIAN")
    
def print_historical_pvp_data(input_data):    
    print ("***All Historical PvP Data***")
    if 'allTime' in input_data['Response']['allPvP']:
        data = input_data['Response']['allPvP']['allTime']

        print ("    Combat Rating          : " + data["combatRating"]['basic']['displayValue'])
        print ()
        historical_data_helper(data)
        print ("    Objectives Completed    : " + data["objectivesCompleted"]['basic']['displayValue'])
        print ("    Activities Won          : " + data["activitiesWon"]['basic']['displayValue'])
        print ("    Win-Loss Ratio          : " + data["winLossRatio"]['basic']['displayValue'])
        print ("    Best Single Game Score  : " + data["bestSingleGameScore"]['basic']['displayValue'])
        print ("    Avg per-game Team Score : " + data["teamScore"]['pga']['displayValue'])
        print ("    Avg Score per life      : " + data["averageScorePerLife"]['basic']['displayValue'])

        print ()
        print ("    "+ data['secondsPlayed']['basic']['displayValue'] + " spent in activity")
        print ()
    else:
        print ("NO DATA FOUND FOR THIS GUARDIAN")
        
def print_historical_raid_data(input_data):
    print ("***All Historical Raid Data***")
    if 'allTime' in input_data['Response']['raid']:
        data = input_data['Response']['raid']['allTime']
        historical_data_helper(data)
        print ("    "+ data['secondsPlayed']['basic']['displayValue'] + " spent in activity")
        print ()
    else:
        print ("INSUFFICIENT DATA FOR MEANINGFUL ANSWER.")
        
def print_historical_story_data(input_data):
    print ("***All Historical Story Data***")
    if 'allTime' in input_data['Response']['story']:    
        data = input_data['Response']['story']['allTime']
        historical_data_helper(data)
        print ("    "+ data['secondsPlayed']['basic']['displayValue'] + " spent in activity")
        print ()
    else: 
        print ("NO DATA FOUND FOR THIS GUARDIAN")
        
def print_historical_pve_data(input_data):
    print ("***All Historical PvE Data***")
    if 'allTime' in input_data['Response']['patrol']:    
        data = input_data['Response']['patrol']['allTime']
        historical_data_helper(data)
        print ("    Objectives Completed    : " + data["objectivesCompleted"]['basic']['displayValue'])
        print ("    Adventures Completed    : " + data["adventuresCompleted"]['basic']['displayValue'])
        print ("    Public Events Completed : " + data["publicEventsCompleted"]['basic']['displayValue'])
        print ("    Heroic Events Completed : " + data["heroicPublicEventsCompleted"]['basic']['displayValue'])
        print ("    Activities Entered      : " + data["activitiesEntered"]['basic']['displayValue'])
        print ()
        print ("    " + data['secondsPlayed']['basic']['displayValue'] + " spent in activity")
        print ()
    else:
        print ("NO DATA FOUND FOR THIS GUARDIAN")

def print_calculated_stats(input_data):
    print ("***AGGREGATE STATS***")
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_revives_perf = 0
    total_revives_rec = 0
    
    raid_efficiency = 0
    strike_efficiency = 0
    pvp_efficiency = 0
    story_efficiency = 0
    patrol_efficiency = 0
    
    data = input_data['Response']
    if 'allTime' in data['raid']:
        raid_efficiency = data['raid']['allTime']['efficiency']['basic']['value']
        total_kills = total_kills + data['raid']['allTime']['kills']['basic']['value']
        total_deaths = total_deaths + data['raid']['allTime']['deaths']['basic']['value']
        total_assists = total_assists + data['raid']['allTime']['assists']['basic']['value']
        total_revives_perf = total_revives_perf + data['raid']['allTime']['resurrectionsPerformed']['basic']['value']
        total_revives_rec = total_revives_rec + data['raid']['allTime']['resurrectionsReceived']['basic']['value']
        
    data = input_data['Response']
    if 'allTime' in data['allStrikes']:
        strike_efficiency = data['allStrikes']['allTime']['efficiency']['basic']['value']
        total_kills = total_kills + data['allStrikes']['allTime']['kills']['basic']['value']
        total_deaths = total_deaths + data['allStrikes']['allTime']['deaths']['basic']['value']       
        total_assists = total_assists + data['allStrikes']['allTime']['assists']['basic']['value']
        total_revives_perf = total_revives_perf + data['allStrikes']['allTime']['resurrectionsPerformed']['basic']['value']
        total_revives_rec = total_revives_rec + data['allStrikes']['allTime']['resurrectionsReceived']['basic']['value']
    
    data = input_data['Response']
    if 'allTime' in data['patrol']:
        patrol_efficiency = data['patrol']['allTime']['efficiency']['basic']['value']
        total_kills = total_kills + data['patrol']['allTime']['kills']['basic']['value']
        total_deaths = total_deaths + data['patrol']['allTime']['deaths']['basic']['value']
        total_assists = total_assists + data['patrol']['allTime']['assists']['basic']['value']
        total_revives_perf = total_revives_perf + data['patrol']['allTime']['resurrectionsPerformed']['basic']['value']
        total_revives_rec = total_revives_rec + data['patrol']['allTime']['resurrectionsReceived']['basic']['value']
        
    data = input_data['Response']
    if 'allTime' in data['allPvP']:
        pvp_efficiency = data['allPvP']['allTime']['efficiency']['basic']['value']
        total_kills = total_kills + data['allPvP']['allTime']['kills']['basic']['value']
        total_deaths = total_deaths + data['allPvP']['allTime']['deaths']['basic']['value']
        total_assists = total_assists + data['allPvP']['allTime']['assists']['basic']['value']
        total_revives_perf = total_revives_perf + data['allPvP']['allTime']['resurrectionsPerformed']['basic']['value']
        total_revives_rec = total_revives_rec + data['allPvP']['allTime']['resurrectionsReceived']['basic']['value']
        
    data = input_data['Response']
    if 'allTime' in data['story']:
        story_efficiency = data['story']['allTime']['efficiency']['basic']['value']
        total_kills = total_kills + data['story']['allTime']['kills']['basic']['value']
        total_deaths = total_deaths + data['story']['allTime']['deaths']['basic']['value']        
        total_assists = total_assists + data['story']['allTime']['assists']['basic']['value']
        total_revives_perf = total_revives_perf + data['story']['allTime']['resurrectionsPerformed']['basic']['value']
        total_revives_rec = total_revives_rec + data['story']['allTime']['resurrectionsReceived']['basic']['value']
        
    print ("    Total Kills   : " + str(total_kills))
    print ("    Total Deaths  : " + str(total_deaths))
    
    if total_deaths != 0:
        print ("    K/D           : " + str(total_kills / total_deaths))
        calc_eff = (total_kills + total_assists) / total_deaths

    else: 
        print ("    K/D           : " + str(total_kills))
        calc_eff = (total_kills + total_assists)
        
    print ("    Total Assists : " + str(total_assists))
    print ()
    print ("    Calculated Efficiency  : " + str(calc_eff))
    print ("        Raid   : " + str(raid_efficiency))
    print ("        Strike : " + str(strike_efficiency))
    print ("        PvE    : " + str(patrol_efficiency))
    print ("        PvP    : " + str(pvp_efficiency))
    print ("        Story  : " + str(story_efficiency))
    print ()
    print ("    Total Resurrections Performed  : " + str(total_revives_perf))
    print ("    Total Resurrections Recieved   : " + str(total_revives_rec))
    print ("    Resurrection Efficiency        : " + str(total_revives_perf / total_revives_rec))
    
def print_current_milestone_information(input_data): #WIP
    data = input_data['Response']
    print ("***MILESTONE INFORMATION***")
    for key, value in data.items():
        mile_hash = key
        
        if 'availableQuests' in data[mile_hash]:            
            if 'activity' in data[mile_hash]['availableQuests'][0]:
                act_hash = data[mile_hash]['availableQuests'][0]['activity']['activityHash']
                print (act_hash)
                act_json = d2.destinyManifestRequestActivityDefinition(int(act_hash))
                print (act_json)
            elif 'questItemHash' in data[mile_hash]['availableQuests'][0]:
                print ()

def print_activity_history(input_data):
    data = input_data['Response']
    
    if 'activities' in data:
        for i in range(len(data['activities'])):
            act_hash = data['activities'][i]['activityDetails']['directorActivityHash']
            act_period = data['activities'][i]['period']
            act_time_played = data['activities'][i]['values']['timePlayedSeconds']['basic']['displayValue']
            
            #act_json = d2.getPostGameCarnageReport(act_hash)
            #print (act_json)
            print (act_period)
            print ("    Time Played: " + act_time_played)

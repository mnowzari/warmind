import sys
import destiny2_parser as dparse
import destiny2_API as d2

membershipID          = 0
membershipType        = -1 #or 254 for PC-only
destinyMembershipType = 0
destinyMembershipID   = 0
destinyCharacters     = []  

def stats_handler():
    global destinyCharacters
    
    print ("Select a Guardian: ")
    for i in range (0, len(destinyCharacters)):
        print (str(i + 1) + ".) " + str(destinyCharacters[i]))
        i = i + 1
    user_in = input()
    
    if int(user_in) <= len(destinyCharacters):
        data = d2.getHistoricalStats(destinyMembershipType, destinyMembershipID, destinyCharacters[int(user_in) - 1])
        return data
    else:
        return 0

def main():
    global membershipID, membershipType, destinyMembershipType, destinyMembershipID, destinyCharacters
    print ("___DESTINY 2 WARMIND___")
    
    print ("Enter Complete Destiny 2 gamertag")
    user_in = str(input())
    
    access_creds = dparse.get_access_information(user_in)

    if (access_creds != 0):       
        membershipID = access_creds[0]
        membershipType = access_creds[1]
        destinyMembershipType = access_creds[2]
        destinyMembershipID = access_creds[3]
        destinyCharacters = access_creds[4]
        
        while True:
            print ("Enter a command. Type '!help' for a list of commands.")
            user_in = str(input())
            
            if user_in == "!help":
                display_help()
            elif user_in == "basic_info":
                dparse.print_basic_info(d2.getMembershipsById(membershipID, membershipType))
            elif user_in == "char_sheet":
                data = d2.getCharacter(destinyMembershipType, destinyMembershipID)
                #d2.dump_json_to_file("debug.json", data)
                dparse.print_character_sheet(data)   
            elif user_in == "stats_pve":
                data = stats_handler()
                if data != 0:   
                    dparse.print_historical_pve_data(data)
            elif user_in == "stats_pvp":
                data = stats_handler()
                if data != 0:   
                    dparse.print_historical_pvp_data(data)
            elif user_in == "stats_raid":
                data = stats_handler()
                if data != 0:   
                    dparse.print_historical_raid_data(data)
            elif user_in == "stats_strike":
                data = stats_handler()
                if data != 0:   
                    dparse.print_historical_strike_data(data)
            elif user_in == "stats_story":
                data = stats_handler()
                if data != 0:   
                    dparse.print_historical_story_data(data)
            elif user_in == "new_guard":
                print ("WIP")
            elif user_in == "!dump":
                d2.updateLocalFiles()
            elif user_in == "!q":
                break
            else: print ("Unkown command.")
    else:
        print ("Could not find the requested Guardian. Maybe the Guardian is missing its Ghost?")
        
def display_help():
    print ("***DESTINY 2 WARMIND HELP***")
    file = open("d2_warmind_help.txt", "r")
    s = file.readlines()
    for i in s:
        print("-" + i)
    print ()
main()
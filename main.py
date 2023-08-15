import json
import os 
import gc
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize an empty list to store the JSON objects
data = []
unique_users = []
data_length = 0

directory = '/home/lambda3/socialNetwork/txt'

file_list = os.listdir(directory)

output_file = 'tweet_retweet_data.json'
output_file_2 = "tweeter_language_data.json"

geolocator = Nominatim(user_agent="Twitter_Analysis")

# Extracts Unique First Keys of a Dictionary List
def firstKey(data_list): 
    unique_first_keys = set()
    for dictionary in data_list:
        first_key = next(iter(dictionary.keys()))
        unique_first_keys.add(first_key)
    # Convert the set back to a list if needed
    return list(unique_first_keys)

# Traverse through nested dictionary structure and prints all keys 
def print_all_keys(obj):
    if isinstance(obj, dict):
        for key in obj.keys():
            print(key)
            print_all_keys(obj[key])
    elif isinstance(obj, list):
        for item in obj:
            print_all_keys(item)

start_time = time.time()

################################################################################################
################################    Read 1 File     ############################################
################################################################################################

# with open('/home/lambda3/socialNetwork/txt/Gardenhose.1420848060', 'r') as json_file:
#     for line in json_file:
#         if line.strip():
#             try:
#                 tweet = json.loads(line)
#                 data.append(tweet)
#             except json.JSONDecodeError as e:
#                 print(f"Error decoding JSON: {e}")


# val = list(data.keys())
# print(val)

# print(print_all_keys(data[1]))


################################################################################################
######################  Read 1 File, Output: User, Retweeters     ##############################
################################################################################################

# with open('/home/lambda3/socialNetwork/txt/Gardenhose.1420901404', 'r') as json_file:
#     for line in json_file:
#         if line.strip():
#             try:
#                 tweet = json.loads(line)
#                 # Ignores delete lines and will only append if retweet count > 0
#                 if not tweet.get('delete') and tweet.get('retweeted_status') and tweet['retweeted_status'].get('retweet_count', 0) > 0:
#                     original_user = tweet['retweeted_status']['user']['screen_name']
#                     retweeters = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
#                     data.append({'original_user': original_user, 'retweeters': retweeters})
#             except json.JSONDecodeError as e:
#                 print(f"Error decoding JSON: {e}")
# print("Length of Data from file: " + str(len(data))) 
# NOTE: File contains 3043, check if multiple file section is the same

################################################################################################
############################    Read Multiple File     #########################################
################################################################################################

# for filename in file_list[:10]:  # Slice the list to only include desired files
#     data = []
    
#     file_path = os.path.join(directory, filename)
#     with open(file_path, 'r') as json_file:
#         print(file_path)
#         for line in json_file:
#             if line.strip():
#                 try:
#                     tweet = json.loads(line)
#                     data.append(tweet)
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON in file {filename}: {e}")

#         if data:
#             print(firstKey(data))
#         else:
#             print("No data loaded.")
#         del data
#         gc.collect()

################################################################################################
######################    Read Multiple File  w/ Outputs   #####################################
################################################################################################

# with open(output_file_2, 'w') as output:
#     for filename in file_list:
#         file_path = os.path.join(directory, filename)
#         with open(file_path, 'r') as json_file:
#             print(file_path)
#             for line in json_file:
#                 if line.strip():
#                     try:
#                         tweet = json.loads(line)
#                         # Ignores delete lines and will only append if retweet count > 0
#                         if not tweet.get('delete') and tweet.get('retweeted_status') and tweet['retweeted_status'].get('retweet_count', 0) > 0:
#                             original_user = tweet['retweeted_status']['user']['screen_name']
#                             retweeters = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
#                             data = {'original_user': original_user, 'retweeters': retweeters}
#                             output.write(json.dumps(data) + '\n')
#                             data_length = data_length + 1
#                     except json.JSONDecodeError as e:
#                         print(f"Error decoding JSON in file {filename}: {e}")

# end_time = time.time()
# total_time = end_time - start_time

# print("Time Taken: " + str(total_time) + " seconds")
# print("Length of Data from file: " + str(data_length))

# Loading all this to variable data is ineffective
# Write data into a .json file after each file

################################################################################################
###############    Read Multiple File for users w/ language   ##################################
################################################################################################

with open(output_file_2, 'w') as output:
    for filename in file_list:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as json_file:
            print(file_path)
            for line in json_file:
                if line.strip():
                    try:
                        tweet = json.loads(line)
                        # Ignores delete lines and will only append if retweet count > 0
                        if not tweet.get('delete') and tweet.get('retweeted_status') and tweet['retweeted_status'].get('retweet_count', 0) > 0:
                            original_user = tweet['retweeted_status']['user']['screen_name']
                            language = tweet['retweeted_status']['user']['lang']
                            if language == 'Select Language...':
                                language = None
                            data = {'original_user': original_user, 'language': language}
                            output.write(json.dumps(data) + '\n')
                            data_length = data_length + 1
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")

end_time = time.time()
total_time = end_time - start_time

print("Time Taken: " + str(total_time) + " seconds")
print("Length of Data from file: " + str(data_length))


# NOTE: Runtimes per file
#   1
#       Time Taken: 0.254284143447876 seconds
#       Length of Data from file: 3043
#   2 
#       Time Taken: 0.5080451965332031 seconds
#       Length of Data from file: 5901
#   10 
#       Time Taken: 2.199260950088501 seconds
#       Length of Data from file: 27413
#   100
#       Time Taken: 23.94064688682556 seconds
#       Length of Data from file: 300518
#   1000 
#       Time Taken: 241.542733669281 seconds
#       Length of Data from file: 2991134
#   All 2971
#       Time Taken: 715.9926760196686 seconds
#       Length of Data from file: 8914313


# NOTE: File contains 10,000, seems like all files have same amount of rows 
# NOTE: There are 2971 files
# NOTE: Seems like there are 2 different actions: created_at & delete



################################################################################################
############################    JSON File Structure   #########################################
################################################################################################
#           Created_at keys:
                #{"created_at":"Sat Jan 10 00:00:51 +0000 2015",
                # "id":553702977064931329,
                # "id_str":"553702977064931329",
                # "text":"RT @Yildiraycicek9: TUNCEL\u0130 MESELES\u0130 B\u00dcY\u00dcK DERS OLMU\u015e! \/ Y\u0131ld\u0131ray \u00c7i\u00e7ek http:\/\/t.co\/VLraHWm5QS http:\/\/t.co\/2SFwpOqUqk",
                # "source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e",
                # "truncated":false,"in_reply_to_status_id":null,
                # "in_reply_to_status_id_str":null,
                # "in_reply_to_user_id":null,
                # "in_reply_to_user_id_str":null,
                # "in_reply_to_screen_name":null,
                # "user":
                #       {"id":214219042,
                #        "id_str":"214219042",
                #        "name":"Tahir Demirel",
                #        "screen_name":"tahirdemirel66",
                #        "location":"T\u00dcRK\u0130YE",
                #        "url":"http:\/\/instagram.com\/tahirdemirel", 
                #        "description":"Selenge M\u00fch.Mim.\u0130n\u015f.Enj.Rek.San.Tic.Ltd.\u015eti. (Mak. M\u00fch.\u015eirket Sahibi) - MMO Yozgat \u0130l Temsilcisi. - 2009-2014 MHP Sorgun Bel.Mec.\u00dcyesi - K\u0131z\u0131lay Sorgun \u015eube Sek",
                #        "protected":false,
                #        "verified":false,
                #        "followers_count":1345,
                #        "friends_count":1546,
                #        "listed_count":0,
                #        "favourites_count":8,
                #        "statuses_count":2992,
                #        "created_at":"Wed Nov 10 21:37:25 +0000 2010",
                #        "utc_offset":7200,
                #        "time_zone":"Istanbul",
                #        "geo_enabled":false,
                #        "lang":"tr",
                #        "contributors_enabled":false,
                #        "is_translator":false,
                #        "profile_background_color":"C0DEED",
                #        "profile_background_image_url":"http:\/\/pbs.twimg.com\/profile_background_images\/777370688\/d3c4b8a2e7ea1207b93212a5a19a53a4.jpeg",
                #        "profile_background_image_url_https":"https:\/\/pbs.twimg.com\/profile_background_images\/777370688\/d3c4b8a2e7ea1207b93212a5a19a53a4.jpeg",
                #        "profile_background_tile":true,
                #        "profile_link_color":"0084B4",
                #        "profile_sidebar_border_color":"FFFFFF",
                #        "profile_sidebar_fill_color":"DDEEF6",
                #        "profile_text_color":"333333",
                #        "profile_use_background_image":true,
                #        "profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/378800000617267826\/f043a99af9f94ce43c989e44da5cadde_normal.jpeg",
                #        "profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/378800000617267826\/f043a99af9f94ce43c989e44da5cadde_normal.jpeg",
                #        "profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/214219042\/1408283630",
                #        "default_profile":false,
                #        "default_profile_image":false,
                #        "following":null,
                #        "follow_request_sent":null,
                #        "notifications":null},
                #        "geo":null,
                #        "coordinates":null,
                #        "place":null,
                #        "contributors":null,
                #        "retweeted_status":
                #                          {"created_at":"Fri Jan 09 23:59:27 +0000 2015",
                #                           "id":553702623317344256,
                #                           "id_str":"553702623317344256",
                #                           "text":"TUNCEL\u0130 MESELES\u0130 B\u00dcY\u00dcK DERS OLMU\u015e! \/ Y\u0131ld\u0131ray \u00c7i\u00e7ek http:\/\/t.co\/VLraHWm5QS http:\/\/t.co\/2SFwpOqUqk",
                #                           "source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e",
                #                           "truncated":false,
                #                           "in_reply_to_status_id":null,
                #                           "in_reply_to_status_id_str":null,
                #                           "in_reply_to_user_id":null,
                #                           "in_reply_to_user_id_str":null, 
                #                           "in_reply_to_screen_name":null,
                #                           "user":
                #                                 {"id":205777651,
                #                                  "id_str":"205777651",
                #                                  "name":"Y\u0131ld\u0131ray \u00c7\u0130\u00c7EK",
                #                                  "screen_name":"Yildiraycicek9",
                #                                  "location":"Ankara",
                #                                  "url":"http:\/\/www.yildiraycicek.com",
                #                                  "description":"Ortado\u011fu Gazetesi K\u00f6\u015fe Yazar\u0131 \/\r\n\r\nKutlu Sesleni\u015f Dergisi Yaz\u0131 \u0130\u015fleri M\u00fcd\u00fcr\u00fc",
                #                                  "protected":false,
                #                                  "verified":false,
                #                                  "followers_count":26948,
                #                                  "friends_count":685,
                #                                  "listed_count":84,
                #                                  "favourites_count":8318,
                #                                  "statuses_count":22009,
                #                                  "created_at":"Thu Oct 21 15:47:33 +0000 2010",
                #                                  "utc_offset":7200,
                #                                  "time_zone":"Istanbul",
                #                                  "geo_enabled":true,
                #                                  "lang":"tr",
                #                                  "contributors_enabled":false,
                #                                  "is_translator":false,
                #                                  "profile_background_color":"DBE9ED",
                #                                  "profile_background_image_url":"http:\/\/pbs.twimg.com\/profile_background_images\/344918034407992492\/8f829d3cc417bfc0b39832dde50c141f.jpeg",
                #                                  "profile_background_image_url_https":"https:\/\/pbs.twimg.com\/profile_background_images\/344918034407992492\/8f829d3cc417bfc0b39832dde50c141f.jpeg",
                #                                  "profile_background_tile":true,
                #                                  "profile_link_color":"CC3366",
                #                                  "profile_sidebar_border_color":"000000",
                #                                  "profile_sidebar_fill_color":"E6F6F9",
                #                                  "profile_text_color":"333333",
                #                                  "profile_use_background_image":true,
                #                                  "profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/542242710657056768\/cncaUrxD_normal.jpeg",
                #                                  "profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/542242710657056768\/cncaUrxD_normal.jpeg",
                #                                  "profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/205777651\/1399325281",
                #                                  "default_profile":false,
                #                                  "default_profile_image":false,
                #                                  "following":null,
                #                                  "follow_request_sent":null,
                #                                  "notifications":null},
                #                           "geo":null,
                #                           "coordinates":null,
                #                           "place":null,
                #                           "contributors":null,
                #                           "retweet_count":2,
                #                           "favorite_count":2,
                #                           "entities":{
                #                                   "hashtags":[],
                #                                   "trends":[],
                #                                    "urls":[{
                #                                             "url":"http:\/\/t.co\/VLraHWm5QS",
                #                                             "expanded_url":"http:\/\/yildiraycicek.com\/makale\/5070\/tunceli_meselesi_buyuk_ders_olmus.html#.VLBq3P5xnIU",
                #                                             "display_url":"yildiraycicek.com\/makale\/5070\/tu\u2026",
                #                                             "indices":[52,74]}],
                #                                             "user_mentions":[],
                #                                             "symbols":[],
                #                                             "media":[{"id":553702622411366401,
                #                                                       "id_str":"553702622411366401",
                #                                                       "indices":[75,97],
                #                                                       "media_url":"http:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg",
                #                                                       "media_url_https":"https:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg",
                #                                                       "url":"http:\/\/t.co\/2SFwpOqUqk",
                #                                                       "display_url":"pic.twitter.com\/2SFwpOqUqk",
                #                                                       "expanded_url":"http:\/\/twitter.com\/Yildiraycicek9\/status\/553702623317344256\/photo\/1",
                #                                                       "type":"photo",
                #                                                       "sizes":{"medium":{"w":600,"h":240,"resize":"fit"},"large":{"w":750,"h":300,"resize":"fit"},"small":{"w":340,"h":136,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"}}}]},"extended_entities":{"media":[{"id":553702622411366401,"id_str":"553702622411366401","indices":[75,97],"media_url":"http:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","media_url_https":"https:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","url":"http:\/\/t.co\/2SFwpOqUqk","display_url":"pic.twitter.com\/2SFwpOqUqk","expanded_url":"http:\/\/twitter.com\/Yildiraycicek9\/status\/553702623317344256\/photo\/1","type":"photo","sizes":{"medium":{"w":600,"h":240,"resize":"fit"},"large":{"w":750,"h":300,"resize":"fit"},"small":{"w":340,"h":136,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"}}}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"tr"},"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"trends":[],"urls":[{"url":"http:\/\/t.co\/VLraHWm5QS","expanded_url":"http:\/\/yildiraycicek.com\/makale\/5070\/tunceli_meselesi_buyuk_ders_olmus.html#.VLBq3P5xnIU","display_url":"yildiraycicek.com\/makale\/5070\/tu\u2026","indices":[72,94]}],"user_mentions":[{"screen_name":"Yildiraycicek9","name":"Y\u0131ld\u0131ray \u00c7\u0130\u00c7EK","id":205777651,"id_str":"205777651","indices":[3,18]}],"symbols":[],"media":[{"id":553702622411366401,"id_str":"553702622411366401","indices":[95,117],"media_url":"http:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","media_url_https":"https:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","url":"http:\/\/t.co\/2SFwpOqUqk","display_url":"pic.twitter.com\/2SFwpOqUqk","expanded_url":"http:\/\/twitter.com\/Yildiraycicek9\/status\/553702623317344256\/photo\/1","type":"photo","sizes":{"medium":{"w":600,"h":240,"resize":"fit"},"large":{"w":750,"h":300,"resize":"fit"},"small":{"w":340,"h":136,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"}},"source_status_id":553702623317344256,"source_status_id_str":"553702623317344256"}]},"extended_entities":{"media":[{"id":553702622411366401,"id_str":"553702622411366401","indices":[95,117],"media_url":"http:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","media_url_https":"https:\/\/pbs.twimg.com\/media\/B68lmfgIIAEoe-S.jpg","url":"http:\/\/t.co\/2SFwpOqUqk","display_url":"pic.twitter.com\/2SFwpOqUqk","expanded_url":"http:\/\/twitter.com\/Yildiraycicek9\/status\/553702623317344256\/photo\/1","type":"photo","sizes":{"medium":{"w":600,"h":240,"resize":"fit"},"large":{"w":750,"h":300,"resize":"fit"},"small":{"w":340,"h":136,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"}},"source_status_id":553702623317344256,"source_status_id_str":"553702623317344256"}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"medium","lang":"tr","timestamp_ms":"1420848051693"}
                # THERE IS STILL MORE

#           Delete keys: Technically has one key but in that key there is more elements
                # "delete":
                        # {"status":
                                # {"id":,
                                #  "id_str":"",
                                #  "user_id":,
                                #  "user_id_str":""},
                        # "timestamp_ms":""}}



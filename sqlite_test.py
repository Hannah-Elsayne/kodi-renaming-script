#---------------------------#
#   Author: Hannah Elsayne
#---------------------------#
import sqlite3 as sqlite
import sys
import os
import re
#---------------------------#

"""
Url: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
"""

import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=''):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    

#---------------------------#

def renamefile(filepath, seasonN, episodeN, title):

    if (os.path.isfile(filepath)) and ("\\Anime\\" in filepath):
        try:
            newName = ""
            fileExtension = filepath[-3:]
            newSeasonN = seasonN
            newEpisodeN = episodeN
    
            if (seasonN < 10):
                newSeasonN = "0{0}".format(seasonN)
            if (episodeN < 10):
                newEpisodeN = "0{0}".format(episodeN)
        
            print("Current File: {0}".format(filepath))
    
            newName += os.path.dirname(os.path.abspath(filepath))
            filename = "- S{0}E{1}. {2}.{3}".format(newSeasonN, newEpisodeN, title, fileExtension)
    
            temp = clean_filename(filename)
            final = newName + "\\" + temp
    
            print("New File: {0}".format(final))


            if filepath == temp:
                print("No Changes Made")
            else:
                os.rename(filepath, final)
        except Exception as e:
            print("failed rename")
            print(e)
        
    else:
        print("Internal Error")

#---------------------------#

try:

    dbcon = sqlite.connect(r"C:\Users\Jeth Elsayne\AppData\Roaming\Kodi\userdata\Database\MyVideos107.db")
    dbcon.row_factory = sqlite.Row

    #sql = "SELECT episode.c00 as etitle, CAST (episode.c12 AS INTEGER) AS snumber, CAST (episode.c13 AS INTEGER) AS enumber, episode.c18 AS file, tvshow.c00 as title FROM episode JOIN tvshow USING (idShow) WHERE title='RWBY' ORDER BY snumber ASC, enumber ASC"

    #sql = "SELECT episode.c18 as filepath, CAST (episode.c12 AS INTEGER) AS seasonnumber, CAST (episode.c13 AS INTEGER) AS episodenumber, episode.c00 AS title, tvshow.c00 AS show FROM episode JOIN tvshow USING (idShow) WHERE title='RWBY' ORDER BY seasonnumber ASC, episodenumber ASC"

    sql = "SELECT tvshow.c00 AS show, episode.c18 as filepath, episode.c00 as title, CAST (episode.c12 AS INTEGER) AS seasonnumber, CAST (episode.c13 AS INTEGER) AS episodenumber FROM episode JOIN tvshow USING (idShow) WHERE show='Violet Evergarden' ORDER BY show"
        
    for row in dbcon.execute(sql):
        print("------------------------------------------------")
        print(row['show'])
        renamefile(row['filepath'], row['seasonnumber'], row['episodenumber'], row['title'])
        #print(row['show'])
        #print(row['title'])
    
except Exception as e:
    print("failed")
    print(e, file=sys.stderr)
    sys.exit(3)
    
finally:
    dbcon.close()

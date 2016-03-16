import modsqual
import csv

#Create the list of the valid MODS resource types that we'll use for checking typeOfResource against
resource_types = ["text", "cartographic", "notated music", "sound recording-musical", "sound recording-nonmusical",
              "sound recording", "still image", "moving image", "three dimensional object", "software, multimedia",
              "mixed material"]

#Function that takes in a boolean value and returns a score. The default is set to score 1 for True and 0 for False
def score(bool, point=True, value=1):
    """assign points if bool value matches point argument value"""
    if bool == point:
        score = value
    else:
        score = 0
    return score

#Function to test the existence of a top-level element and pass the result to score() to return a score
def exists(element):
    """top-level element exists"""
    s = score(element.exists)
    return s

#Function to test if a text element's value is present in a given list. Returns a score of 1 if true or 0 if False
def inList(element, list):
    """element value matches a value from a controlled vocabulary"""
    if element.exists == True:
        s = score(all(i in list for i in element.text()))
    else:
        s = 0
    return s

#Function to test the presence of an element or value based on an xpath match. Returns a score of 1 if true or 0 if False
def xpathexists(match, min=1):
    """result from xpath match contains at least one element match"""
    try:
        s = score(len(match) >= min)
    except:
        s = 0
    return s

#Create a new csv file that we'll write our scores to
z = open('sample_mods_scores.csv', 'wb')
header = ['uuid', 'division', 'collection', 'title', 'typeOfResource', 'genre', 'date', 'identifier', 'location', 'total']
writer = csv.DictWriter(z, fieldnames=header)
writer.writeheader()

#Open our source MODS data file. this file has one MODS XML record per line, so we can iterate through the file line by line
f = open('sample_mods_data.txt')

#Iterate through each line (along with its row index (idx) in the file) to parse each MODS record and collect the scores
for idx, line in enumerate(f):
    #load the MODS recrod into a modsqual Mods object
    mods = modsqual.Mods(line)
    
    #Get some basic identifying information
    #Get uuid identifier
    uuids = mods.identifier.match(attr=['@type="uuid"'])
    uuid = uuids[0]
    #Get collection name. Collection is the most deeply nested relatedItem, so get all descendents and take the last in the list.
    collections = mods.relatedItem.match(xpath='.//m:relatedItem/m:titleInfo/m:title/text()')
    if collections > 0:
        coll_name = collections[-1]
    else:
        coll_name = 'Null'
    
    #Get the scores
    #Test true/false (1/0) if title exists. Use the exists() function to calculate score
    title = exists(mods.titleInfo)
    #Do the same for genre
    genre = exists(mods.genre)
    #Test true/false (1/0) if all typeOfResource values are in the resource_types list. Use the inList() function to calculate score
    typeOfResource = inList(mods.typeOfResource, resource_types)
    #Use xpathexists() function to test if at least one of the three recommended date types are present
    date = xpathexists(mods.originInfo.match(xpath='./m:originInfo/m:dateCreated|./m:originInfo/m:dateIssued|./m:originInfo/m:copyrightDate'))
    #Use xpathexists() function to test if at least one of the three recommended identifier types are present
    identifier = xpathexists(mods.identifier.match(xpath='./m:identifier[@type="local_bnumber" or @type="local_mss" or @type="local_tms"]'))
    #Use xpathexists() function to test if the physicalLocation of type "division" is present
    location = xpathexists(mods.location.match(xpath='./m:location/m:physicalLocation[@type="division"]'))
    
    #add up the individual scores
    scores = [title, typeOfResource, genre, date, identifier, location]
    total = sum(scores)
    
    #Get curatorial division name. First check if division location is present, then take the first one listed. If none, then Null.
    if (location == 1):
        division = mods.location.match(xpath='./m:location/m:physicalLocation[@type="division"]')[0]
    else:
        division = 'Null'
        
    #Write the row of data and scores to the csv file
    row = {'uuid':uuid, 'division':division, 'collection':coll_name, 'title':title, 'typeOfResource':typeOfResource, 'genre':genre,
           'date':date, 'identifier':identifier, 'location':location, 'total':total}
    writer.writerow(row)
    
f.close()
z.close()
    
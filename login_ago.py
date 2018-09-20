#-------------------------------------------------------------------------------
# Name:        Login to BC's Map Hub with IDIR (aka ESRI Enterprise Account)
# Author:      Michelle Douville
# Created:     19/09/2018
#
# Instructions:

# There are a few steps that you MUST do with your Enterprise Account..before you run this script.

# 1.) If you don't have a usable/designated 'Client ID' and 'Client Secret' - GO HERE FIRST - "ArcGIS for Developers" https://developers.arcgis.com/sign-in/ 
# 2.) Sign in with your enterprise account (IDIR) using the prefix when prompted for https://governmentofbc.maps.arcgis.com/
# 3.) Once signed in you can register a new application in ArcGIS for Developers.
#       a.) click Dashboard + > New Application with the following properties:
#           Title: <name of script/purpose/ yada yada"
#           Tags: <tags you want to describe use yada yada"
#           Click Register your Application.
#       b.) On the right side, make note of the following values created for your application:
#           Client ID
#           Client Secret
#           Temporary Token -- this is what you need and by default will be valid for 2 hrs (this code will re-generate this on the fly with the client ID and Secret combo)

# These steps will allow you to successfully create an access token that you can use to authenticate requests via python.
# To use token generated with ArcGIS.GIS module see https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html#gis
# class arcgis.gis.GIS(url=None, username=None, password=None, key_file=None, cert_file=None, verify_cert=True, set_active=True, client_id=None, profile=None, **kwargs)
#-------------------------------------------------------------------------------

import requests
import json
from arcgis.gis import GIS

def main():

    clientid = "<generated from above steps document>"
    clientSecret = "<generated from above steps document>"
    portal = "https://governmentofbc.maps.arcgis.com"
    url = portal+"/sharing/rest/oauth2/token"
    
    payload = "client_id="+clientid+"&client_secret="+clientSecret+"&grant_type=client_credentials"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    #This will respond in with a valid token that by default is good for 2 hours.
    print(response.text)

    # convert 'str' to Json
    data = json.loads(response.text)

    # Now you can access Json
    tokenhash = data['access_token']
      
    #the next step just tries to connect with the token as an example
    try:
        print('Connecting to {}'.format(portal))
        gis = GIS(url=portal, verify_cert=False, set_active=True, token=tokenhash)
        #this nex line is just for testing the connection
        print(gis.content.search(query="title:road", item_type="Feature Layer"))
    except RuntimeError as ex:
        print('Error Connecting to {}'.format(portal))
    pass

if __name__ == '__main__':
    main()

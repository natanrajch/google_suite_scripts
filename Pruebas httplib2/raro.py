import httplib2
print(httplib2.proxy_info_from_environment("https"))

import os 
import pprint 
  
# Get the list of user's 
# environment variables 
env_var = os.environ
print("User's Environment variable:") 
pprint.pprint(dict(env_var), width = 1) 

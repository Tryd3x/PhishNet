from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
import requests

# having_IP_Address  { -1,1 }
def having_IP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = -1
  return ip

# having_At_Symbol   { 1,-1 }
def having_At_Symbol(url):
  if "@" in url:
    at = 1    
  else:
    at = -1    
  return at

# URL_Length   { 1,0,-1 }
def URL_Length(url):
  if len(url) < 54:
    length = -1
  elif len(url) > 54 and len(url) < 75:
    length = 0
  else:
    length = 1            
  return length

# Redirect  { 0,1 }
def Redirect(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

# HTTPS_token { -1,1 }
def HTTPS_token(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return -1

# Shortining_Service { 1,-1 }
def Shortining_Service(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return -1

# Prefix_Suffix  { -1,1 }
def Prefix_Suffix(url):
    if '-' in urlparse(url).netloc:
        return 1           
    else:
        return -1

# DNSRecord   { -1,1 }
def DNSRecord(url):
  try:
    domain_name = whois.whois(urlparse(url).netloc)
    if(domain_name.status is not None):
      dns = -1
    else:
      dns = 1
  except:
    dns = 1
  return domain_name,dns if (dns!=1) else dns

# web_traffic  { -1,0,1 }
def web_traffic(url):
  try:
    #Filling the whitespaces in the URL if any
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), features="lxml").find(
        "reach")['rank']
    rank = int(rank)
  except TypeError as e:
    return 1
  if rank <100000:
    return -1
  else: 
    return 0

# age_of_domain  { -1,1 }
def age_of_domain(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date

  #nested function
  def calcAge(creation,expiration):
    ageofdomain = abs((expiration - creation).days)
    if ((ageofdomain/30) > 12):
      return -1
    else:
      return 1

  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1

  if ((expiration_date is None) or (creation_date is None)):
    return 1
  # elif ((type(expiration_date) is list) or (type(creation_date) is list)):
    #handle over here [0,1] -> [0,1]
    # ageList = []
    # if (type(expiration_date) is list) and (type(creation_date) is list):
    #   for creation,expiration in zip(creation_date,expiration_date):
    #     ageList.append(calcAge(creation,expiration))
    # elif (type(expiration_date) is list) and (type(creation_date) != list):
    #   for i in expiration_date:
    #     ageList.append(calcAge(creation_date,i))
    # print(ageList)
    # print("This is printing twice")
    # if ageList.count(1)>0:
    #   return 1
    # else:
    #   return -1

  if (type(expiration_date) is list) and (type(creation_date) is list):
    print("Execute1")
    return calcAge(creation_date[0],expiration_date[0])
  elif (type(expiration_date) is list) and (type(creation_date) != list):
    print("Execute2")
    return calcAge(creation_date,expiration_date[0])
  elif (type(expiration_date) != list) and (type(creation_date) is list):
    print("Execute3")
    return calcAge(creation_date[0],expiration_date)
  else:
    print("default")
    return calcAge(creation_date,expiration_date)

# Iframe { 1,-1 }
def Iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return -1
      else:
          return 1

# on_mouseover  { 1,-1 }
def on_mouseover(response): 
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return -1
    else:
      return 1

# RightClick  { 1,-1 }
def RightClick(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return -1
    else:
      return 1

#########################################################################

#Function to extract features
def featureExtraction(url):
  # feature_names = ['having_IP_Address','having_At_Symbol','URL_Length','Redirect','HTTPS_token',
  #                'Shortining_Service','Prefix_Suffix','DNSRecord','web_traffic','age_of_domain',
  #                'Iframe','on_mouseover','RightClick','Result']
  features = []
  features.append(having_IP(url))
  features.append(having_At_Symbol(url))
  features.append(URL_Length(url))

  try:
    response = requests.get(url)
  except:
    response = ""

  features.append(Redirect(response))
  features.append(HTTPS_token(url))
  features.append(Shortining_Service(url))
  features.append(Prefix_Suffix(url))

  [domain_name,dns] = DNSRecord(url)

  features.append(dns)
  features.append(web_traffic(url))
  features.append(age_of_domain(domain_name))
  features.append(Iframe(response))
  features.append(on_mouseover(response))
  features.append(RightClick(response))
  
  return features

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

#13 independent features, 1 dependent feature (Result)
feature_names = ['having_IP_Address','having_At_Symbol','URL_Length','Redirect','HTTPS_token',
                 'Shortining_Service','Prefix_Suffix','DNSRecord','web_traffic','age_of_domain',
                 'Iframe','on_mouseover','RightClick']
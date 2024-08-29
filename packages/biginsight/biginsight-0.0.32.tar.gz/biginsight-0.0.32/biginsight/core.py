import requests, json

prod = True
routeUrl = "https://api.biginsight.ca/api" if prod == True else "http://10.0.0.60:5002/api"

def fetch(url, info):
  resp = requests.post(
    url,
    json=info["body"],
    headers=info["headers"]
  )

  return resp

class BigInsight:
  def __init__(self, key):
    self.key = key
  
  def track(self, info):
    # page visits, user actions
    userInfo = info["userInfo"] # email or user id or any other id to identify a specific user
    page = info["page"] # optional
    action = info["action"]
    body = { "userInfo": userInfo, "page": page, "action": action }
    
    if self.key == "":
      return "Project Token is missing"
    
    if "log_error" in info:
      body["log_error"] = True

    resp = fetch(routeUrl + "/track", {
      "headers": { "Content-Type": "application/json" },
      "body": { 
        "key": self.key,
        **body
      }
    })

    if resp.status_code == 200:
      return resp.json()
    else:
      return resp.json(), 400
  
biginsight = BigInsight(__name__)

import json
import requests
import urllib
from flask import*

s = Flask(__name__)
@s.route("/",methods=['POST'])
def hi():
# You may need to install Requests pip
# python -m pip install requests


            key = 'OfkP2146kTwMTTGU5h28OvhacBj6HSVV'
            def malicious_url_scanner_api(url: str, vars: dict = {}) -> dict:
                url = 'https://www.ipqualityscore.com/api/json/url/%s/%s' % (key, urllib.parse.quote_plus(url))
                x = requests.get(url, params=vars)
                print(x.text)
                return json.loads(x.text)

                    
            URL = str(request.json.get('url',''))
            strictness = 0
            additional_params = {
                'strictness': strictness
            }
            result =malicious_url_scanner_api(URL, additional_params)
            print("ll",result)
            if 'success' in result and result['success'] == True:
                    print(result)
            return result
if __name__ == "__main__":
    s.run(host='0.0.0.0',port=4000)
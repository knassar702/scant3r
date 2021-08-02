#!/usr/bin/env python3
from urllib.parse import urlparse
from logging import getLogger
from core.libs import alert_bug, Http
from modules import Scan
import re

log = getLogger('scant3r')

regexs = {
    'google_api' : 'AIza[0-9A-Za-z-_]{35}',
    'google_oauth' : 'ya29\.[0-9A-Za-z\-_]+',
    'amazon_aws_access_key_id' : '([^A-Z0-9]|^)(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}',
    'amazon_mws_auth_toke' : 'amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    'amazon_aws_url' : 's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com',
    'firebase_url' : '.firebaseio.com[/]+|[a-zA-Z0-9_-]*\.firebaseio.com',
    'facebook_access_token' : 'EAACEdEose0cBA[0-9A-Za-z]+',
    'authorization_bearer' : 'bearer\s*[a-zA-Z0-9_\-\.=:_\+\/]+',
    'mailgun_api_key' : 'key-[0-9a-zA-Z]{32}',
    'twilio_api_key' : 'SK[0-9a-fA-F]{32}',
    'twilio_account_sid' : 'AC[a-zA-Z0-9_\-]{32}',
    'paypal_braintree_access_token' : 'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}',
    'square_oauth_secret' : 'sq0csp-[ 0-9A-Za-z\-_]{43}',
    'square_access_token' : 'sqOatp-[0-9A-Za-z\-_]{22}',
    'stripe_standard_api' : 'sk_live_[0-9a-zA-Z]{24}',
    'stripe_restricted_api' : 'rk_live_[0-9a-zA-Z]{24}',
    'github_access_token' : '[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*',
    'rsa_private_key' : '-----BEGIN RSA PRIVATE KEY-----',
    'ssh_dsa_private_key' : '-----BEGIN DSA PRIVATE KEY-----',
    'ssh_dc_private_key' : '-----BEGIN EC PRIVATE KEY-----',
    'pgp_private_block' : '-----BEGIN PGP PRIVATE KEY BLOCK-----',
    '!debug_page': "Application-Trace|var TRACEBACK|Routing Error|DEBUG\"? ?[=:] ?True|Caused by:|stack trace:|Microsoft .NET Framework|Traceback|[0-9]:in `|#!/us|WebApplicationException|java\\.lang\\.|phpinfo|swaggerUi|on line [0-9]|SQLSTATE",
    'google_captcha' : '6L[0-9A-Za-z-_]{38}',
    'authorization_api' : 'api[key|\s*]+[a-zA-Z0-9_\-]+',
    'twilio_app_sid' : 'AP[a-zA-Z0-9_\-]{32}',
    'authorization_basic' : 'basic\s*[a-zA-Z0-9=:_\+\/-]+',
    'json_web_token' : 'ey[A-Za-z0-9_-]*\.[A-Za-z0-9._-]*|ey[A-Za-z0-9_\/+-]*\.[A-Za-z0-9._\/+-]*'
} # from https://github.com/BitTheByte/Eagle/blob/master/plugins/spider.py by @BitTheByte

class Secrets(Scan):
    def __init__(self, opts: dict, http : Http):
        super().__init__(opts, http)
        
    def start(self) -> dict:
        try:
            url = self.opts['url']
            Regex = r"[:|=|\'|\"|\s*|`|´| |,|?=|\]|\|//|/\*}]({{REGEX}})[:|=|\'|\"|\s*|`|´| |,|?=|\]|\}|&|//|\*/]"
            
            for method in self.opts['methods']:    
                response = self.send_request(method, url)
                
                if type(response) != list : # list value = Connection Error
                    for option,match in regexs.items():
                        c = re.compile(Regex.replace('{{REGEX}}',match))
                        finder = c.findall(response.text)
                        if len(finder) > 0:
                            alert_bug('SECRET', response, Found=option, Match=finder)
            return {}
        except Exception as e:
            log.debug(e)
            return {}

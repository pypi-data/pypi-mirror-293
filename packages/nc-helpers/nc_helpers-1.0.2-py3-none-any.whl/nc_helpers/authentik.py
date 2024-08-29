import os
import requests

class Authentik():
    def __init__(self, host = None, api_token = None, port=443, secure=True):
        self.port = port
        self.secure = secure
        if host and api_token:
            self.host = host
            self.api_token = api_token
        else:
            from dotenv import load_dotenv
            load_dotenv()

            self.api_token=os.environ.get('AUTHENTIK_TOKEN')
            self.host=os.environ.get('AUTHENTIK_HOST')

    def _get(self,path,params=None):
        r = requests.get(
            f'https://{self.host}/api/v3/{path}', 
            headers = {'Authorization': f"Bearer {self.api_token}", 
                       'accept': 'application/json',
                       'Content-Type': 'application/json'
                       },
            params=params
        )
        if r.status_code == 200:
            return r.json()
        else:
            return {}

    def _post(self,path,data):
        r = requests.post(
            f'https://{self.host}/api/v3/{path}', 
            headers = {'Authorization': f"Bearer {self.api_token}",
                       'accept': 'application/json',
                       'Content-Type': 'application/json'
                       },
            json = data
        )
        if r.status_code == 201 or r.status_code == 400:
            return r.json()
        else:
            return {}
        
    def get_authorization_flow(self):
        self._get('flows/instances/', params={'designation': 'authorization'})

    def get_certificate(self):
        certs = self._get('/crypto/certificatekeypairs/')['results']
        return certs[0]
  
    def create_application(self, appname, auth_method=None, external_url=None, internal_url=None):
        if not external_url: external_url = f"https://{self.host.replace('authentik',appname)}"
        if not internal_url: internal_url = external_url
        
        application = self._get(f'core/applications/{appname}')
        if not application:
            if auth_method:            
                provider= self.create_provider(appname, auth_method)
                
            data = {
                    'name': appname,
                    'slug': appname,
                    'provider': provider.get('pk',None),
                    'open_in_new_tab': True,
                    "meta_launch_url": external_url,
                    "meta_description": "unknown",
                    "meta_publisher": "ncubed",
                    "group": "Tools"
                    }
                
            application = self._post('core/applications/',data)
            icon_status = self._post(f'core/applications/{appname}/set_icon_url',{"url": f"/{appname}"})
            urls = self._get(f"providers/oauth2/{provider['pk']}/setup_urls/")
        return (application, provider, urls)

    def create_group(self, group_name):
        data = {
                'name': group_name,
                'is_superuser': False,
                # 'attributes': None,
                }
            
        group = self._post('core/groups/',data)
        return group

    def get_default_property_mappings(self):
        scope_mappings = self._get('propertymappings/scope/')['results']
        results = [x['pk'] for x in self._get('propertymappings/scope/')['results'] if x['scope_name'] == 'email' or x['scope_name'] == 'openid' or x['scope_name'] == 'profile']
        return results
        
    def create_provider(self, appname, auth_method=None):
        provider_name = f"{appname}_oauth2"
        
        if auth_method == 'oauth2':
            provider = self._get('providers/oauth2/',params={'name':provider_name}).get('results')
            cert = self.get_certificate()
            
            if not provider:
                data = {
                "name": f"{appname}_oauth2",
                "authorization_flow": self._get('flows/instances/default-provider-authorization-explicit-consent/').get('pk'),
                "include_claims_in_id_token": True,
                "property_mappings": self.get_default_property_mappings(),
                "sub_mode": "user_email",
                "signing_key": cert['pk']
                }
                
                provider = self._post('providers/oauth2/',data)
            else:
                provider = provider[0]

            
        
        return provider
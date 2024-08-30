import requests


SESSION = requests.Session()


class TravelManagerAPI:
    @classmethod
    def connect(cls, url, portal_id, token):
        cls.api_url = f"https://{url}/q"
        cls.portal_id = portal_id
        cls.token = token
        cls.basic_params = {
            "portal": TravelManagerAPI.portal_id,
            "token": TravelManagerAPI.token,
        }

    @staticmethod
    def get(endpoint, params={}):
        params = (
            TravelManagerAPI.basic_params
            | params
            | {
                "call": endpoint,
            }
        )

        response = SESSION.get(
            TravelManagerAPI.api_url, params=params, timeout=5
        )
        print(response)
        response.raise_for_status()
        data = response.json()
        if "errorCode" in data:
            raise Exception('ErrorCode: "{}" Error: "{}"'.format(data["errorCode"], data["errorCode"]))
        return data

    @staticmethod
    def post(endpoint, params={}, data={}):
        params = (
            TravelManagerAPI.basic_params
            | params
            | {
                "call": endpoint,
            }
        )

        response = SESSION.post(
            TravelManagerAPI.api_url, json=data, params=params, timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if "errorCode" in data:
            raise Exception('ErrorCode: "{}" Error: "{}"'.format(data["errorCode"], data["errorCode"]))
        return data

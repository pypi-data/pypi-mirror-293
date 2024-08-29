import requests

class Telephony:

    def __init__(self, key: str, isTest: bool = False):
        self.__baseUrl: str = "https://api.pressone.co/"
        self.__testBaseUrl: str = "https://pressone-internal-live.herokuapp.com/"
        if not key:
            raise Exception("Secret key needed for this object")
        self.__accessToken: str = key
        self.__isTest: bool = isTest

    def getBaseUrl(self):
        return self.__testBaseUrl if self.__isTest else self.__baseUrl

    def availableNumbers(self, page:int = 1, count: int = 100):
        url = "api/available_number/numbers/?page_index={}&page_size={}".format(page, count)
        available_number = self.get(url)
        response = {
            "data": [],
            "total": available_number.get("total"),
            "size": available_number.get("page_size")
        }

        for available_number_data in available_number:
            number = {
                "phone_number": available_number_data.get("phone_number"),
                "country_code": available_number_data.get("country_code")
            }
            response.data.append(number)

        return response

    def getNumbers(self, page:int = 1, count: int = 100): 
        url = "api/third-party/sdk/number/?page_index={}&page_size={}".format(page, count)
        data = self.get(url)
        
        response = []

        for number in data:
            phone_number = number.get("phone_number")
            status = number.get("verification_status")
            label = number.get("label")
            number_id = number.get("id")
            response.append({
                "phone_number": phone_number,
                "status": status,
                "label": label,
                "number_id": number_id,
            })

        return response

    def getMembers(self, page: int = 1, count: int = 100):
        url = "api/third-party/sdk/team-member/?page_index={}&page_size={}".format(page, count)
        data = self.get(url)
        
        responseData = data.get("data", [])
        total = data.get("total", 0)
        page_size = data.get("page_size", 0)
        
        response = {
            "data": [],
            "total": total,
            "size": page_size
        }

        for businessData in responseData:
            receivers = businessData.get("receivers", [])
            for receiver in receivers:
                response.data.append({
                    "phone_number" : businessData.get("mobile", ""),
                    "full_name"    : f'{businessData.get("first_name", "")} {businessData.get("last_name", "")}',
                    "receiver_id"  : receiver.get("business_number", 0),
                    "receiver_code": receiver.get("extension_code"),
                })

        return response

    def assignNumber(self, param):

        if ("email" not in param or "phone_number" not in param):
            return {
                "message": "both email and phone_number are required.",
                "code"   : "404"
            }

        if ("number_ids" not in param):
            return {
                "message": "number_ids must be an array of int.",
                "code"   : "401"
            }

        payload = {
            "first_name" : param["first_name"] if "first_name" in param else param["phone_number"],
            "last_name"  : param["last_name"] if "last_name" in param else param["phone_number"],
            "email"      : param["email"],
            "mobile"     : param["phone_number"],
            "role"       : param["role"] if "role" in param else "owner",
            "note"       : None,
            "country"    : param["country"] if "country" in param else "NG",
            "can_make_calls": True,
            "permissions": {
                "can_export_call_logs"  : None,
                "can_view_all_call_logs": None,
                "can_export_contact" : None,
                "can_export_report"  : None,
                "can_manage_billing" : None,
                "can_manage_team"    : None,
                "can_manage_permissions": None,
                "can_manage_personalization": None,
                "can_access_call_recordings": None,
                "can_download_call_recordings"  : None,
                "can_view_performance_report": None,
                "can_view_activity_report": None,
                "business_numbers": param["number_ids"],
                "role"           : param["role"] if "role" in param else "owner",
            }
        }

        data = await self.post("api/third-party/sdk/team-member/", payload)

        if "data" in data and data["data"] == "400":
            return data

        receivers = data.get("receivers", [])
        profile = data.get("profile", {})
        first_name = profile.get("first_name", "")
        last_name = profile.get("last_name", "")

        response = []
        for receiver in receivers:
            business_number = receiver.get("business_number", {})
            response.append({
                "phone_number": profile.get("mobile", None),
                "full_name": f"{first_name} {last_name}",
                "receiver_id": business_number.get("id", receiver.get("id", "")),
                "receiver_code": receiver.get("extension_code", ""),
                "user": profile.get("user", 0)
            })

        if len(response) == 0:
            response.append({
                "phone_number": profile.get("mobile", None),
                "full_name": f"{first_name} {last_name}",
                "receiver_id": None,
                "receiver_code": None,
                "user": profile.get("user", 0)
            })

        return response

    def getCallCredentials(self, receiver_id: str, public_key: str):
        return self.post("api/third-party/sdk/receiver-line/", {
            "public_key": public_key,
            "receiver" : receiver_id
        })

    def getCredentials(self, user_id: int):
        if not user_id:
            return {
                "message": "The user ID is required for this request.",
                "code"   : "400"
            }

        return self.post("api/third-party/sdk/team-member/login/", {
            "user_id": user_id
        })

    def getCallRecords(self, page: int = 1, count: int = 100):
        url = "api/third-party/sdk/contacts/?page_index={}&page_size={}".format(page, count)
        return self.get(url)

    def get_contacts(self, page: int = 1, count: int = 100):
        url = "api/third-party/sdk/contacts/?page_index={}&page_size={}".format(page, count)
        return self.get(url)
    
    def get(self, url: str):
        return self.make_request("GET", url)

    def post(self, url: str, data):
        return self.make_request("POST", url, data)

    def make_request(self, method: str, url: str, body):
        headers = {
            'Authorization': f"Bearer {self.__accessToken}",
            'Pressone-X-Api-Key': self.__accessToken,
        }

        full_url: str = f"{self.getBaseUrl()}{url}"

        try:
            if method == "POST":
                response = requests.post(full_url, json = body, headers = headers)
            if method == "GET":
                response = requests.get(full_url, headers = headers)
            
            statusCode: int = response.status_code

            if ( statusCode == 401 ):
                return response.json()

            if (statusCode > 300):
                raise Exception("Error Processing Request")

            return response.json()
        except:  # noqa: E722
            return {
                "message": "An error occured",
                "code"   : "400"
            }
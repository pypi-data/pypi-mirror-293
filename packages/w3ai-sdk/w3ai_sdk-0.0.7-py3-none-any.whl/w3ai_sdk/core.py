import requests
from web3 import Web3
from decimal import Decimal
from w3ai_sdk.const import Const

class W3AIClient:
    def __init__(self, api_key: str, endpoint = '', api_version: str = 'api/v1'):
        self.api_key = api_key
        self.api_version = api_version
        self.headers = {
            'accept': 'application/json',
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        if endpoint != '':
            self.endpoint = endpoint
        else:
            self.endpoint = Const.DEFAULT_SERVER_ENDPOINT

    def make_request(self, endpoint: str, method: str, payload: object = None):
        url = f"{self.endpoint}{self.api_version}{endpoint}"

        try:
            if method == Const.GET_METHOD_NAME:
                req = requests.get(url, headers=self.headers, verify=False)
            elif method == Const.POST_METHOD_NAME:
                req = requests.post(url,json=payload, headers=self.headers, verify=False)
            
            response = req.json()
            if req.status_code < Const.STATUS_BAD_REQUEST_CODE:
                return True, response['data'], ''
            
            return False, None, response['message']
        except requests.exceptions.RequestException as err:
            return False, None, str(err)

    def conver_to_usd(self, balance: str, debt: str, free_balance: str, token_price: float):
        decimal_balance = Decimal(balance) + Decimal(free_balance) - Decimal(debt)
        aioz_balance = Web3.from_wei(decimal_balance,'ether')
        return float(aioz_balance) * token_price

    def get_balance(self):
        get_balance_endpoint = "/api-key/balance"
        get_token_price_endpoint = "/public/token/price"
        balance_success, balance_data, balance_message = self.make_request(get_balance_endpoint, Const.GET_METHOD_NAME)
        aioz_price_success, aioz_price_data, aioz_price_message = self.make_request(get_token_price_endpoint, Const.GET_METHOD_NAME)

        if balance_success and aioz_price_success:
            usd_balance = self.conver_to_usd(balance_data['balance'], balance_data['debt'], balance_data['free_balance'], aioz_price_data['current_price'])
            origin_balance_result = balance_data
            origin_balance_result['usd_balance'] = str(usd_balance)
            return origin_balance_result, ""
        else :
            if not balance_success:
                return None, f"Get balance error: {balance_message}"
            elif not aioz_price_success:
                return None, f"Get AIOZ price error: {aioz_price_message}"
            else :
                return None, "Unknow error"

    def get_model_info(self, model_id:str):
        endpoint=f"/api-key/model/{model_id}/info"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def check_model_is_serving(self, model_id:str):
        endpoint=f"/api-key/model/{model_id}/serving"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def get_model_statistics(self, model_id:str, date_from:str, date_to:str):
        endpoint=f"/api-key/model/{model_id}/statistics"
        data = {
            'from': date_from,
            'to': date_to
        }
        _, data, message = self.make_request(endpoint, Const.POST_METHOD_NAME, data)
        return data, message

    def get_model_task_cost(self, model_id:str):
        endpoint=f"/api-key/model/{model_id}/task/cost"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def get_api_key_permission(self):
        endpoint=f"/api-key/permission"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def get_api_key_statistics(self, date_from:str, date_to:str):
        endpoint=f"/api-key/statistics"
        data = {
            'from': date_from,
            'to': date_to
        }
        _, data, message = self.make_request(endpoint, Const.POST_METHOD_NAME, data)
        return data, message

    def get_task_histories(self, limit:int, offset:int):
        endpoint=f"/api-key/task/histories?limit={limit}&offset={offset}"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def get_task_result(self, task_id:str):
        endpoint=f"/api-key/task/{task_id}/result"
        _, data, message = self.make_request(endpoint, Const.GET_METHOD_NAME, None)
        return data, message

    def create_task(self,files:list, input_params:dict, model_id:str):
        data = {
            'files': files,
            'input_params': input_params,
            'model_id': model_id
        }
        endpoint=f"/api-key/task"
        _, data, message = self.make_request(endpoint, Const.POST_METHOD_NAME, data)
        return data, message
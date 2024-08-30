from .api import WowcherApi


class WowcherPaymentFrame(WowcherApi):
    GET_FRAME_LINK = '/ext/frame/link'

    def get_frame_url(
            self,
            client_id: str,
            merchant_id: str,
            activation_callback_url: str,
            language: str = "en",
            countries: list = None,
            without_auth: bool = False,
            auth_email: str = None,
            amount: float = 0
    ):
        url = f'{self.api_url}{self.GET_FRAME_LINK}'
        headers = {
            "X-ApiKey": self.api_key
        }

        request_body = {
            "client_id": client_id,
            "merchant_id": merchant_id,
            "activation_callback_url": activation_callback_url,
            "language": language,
            "amount": amount
        }

        if countries is not None:
            request_body["countries"] = countries

        if without_auth:
            if auth_email is None:
                raise Exception("Auth email is required for without_auth")

            request_body["additional_data"] = {
                "without_auth": True,
                "auth_email": auth_email
            }

        response = self.api_request(url, request_body, headers=headers)

        return response["data"]["link"]

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard python imports

"""
Two factor auth class to manage sending the SMS with OTP.
"""

import random

# Third party imports

import plivo
from plivo import exceptions


class TwoFactorAuth:

    """
    two_factor_auth provides two factor authentication
    mechanism for applications using Plivo APIs
    """

    def __init__(self, credentials, app_number, phlo_id):
        """
        Constructor method
        :param: credentials
        :param: app_number
        :return: None
        """

        self.client = plivo.RestClient(credentials["auth_id"], credentials["auth_token"])
        self.client_phlo = plivo.phlo.RestClient(credentials["auth_id"], credentials["auth_token"])
        self.app_number = app_number
        self.phlo_id = phlo_id

    def generate_code(self):
        code = random.choice(range(100000, 999999))  # generating 6 digit random code
        return code

    def send_verification_code_sms(self, dst_number: str, message):
        """
        `send_verification_code` accepts destination number
        to which the message that has to be sent.

        The message text should contain a `__code__` construct
        in the message text which will be
        replaced by the code generated before sending the SMS.

        :param: dst_number
        :param: message
        :return: verification code
        """
        try:
            response = self.client.messages.create(
                src=self.app_number, dst=dst_number, text=message
            )
            print(response)
            return response
        except exceptions as e:
            print(e)
            return "Error encountered", 400

    def send_verification_code_voice(self, dst_number, code):
        try:
            response = self.client.calls.create(
                from_=self.app_number,
                to_=dst_number,
                answer_url=f"https://twofa-answerurl.herokuapp.com/answer_url/{code}",
                answer_method="GET",
            )
            return response
        except exceptions as e:
            print(e)
            return "Error encountered", 400

    # Trigger PHLO
    def send_verification_code_phlo(
        self,
        dst_number,
        code,
        mode,
    ):
        payload = {
            "from": self.app_number,
            "to": dst_number,
            "otp": code,
            "mode": mode,
        }
        try:
            phlo = self.client_phlo.phlo.get(self.phlo_id)
            response = phlo.run(**payload)
            return response
        except exceptions as e:
            print(e)
            return ("Error encountered", 400)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# local import

"""
Render HTML, Send & Validate Verification Code.
"""

from plivo import exceptions
from plivo.resources import numbers
from app import app

# Third party imports

from flask import render_template, jsonify, current_app
from plivo import plivoxml, exceptions


# Application landing page


@app.route("/")
def index():
    """
    index() renders the landing page of the application.
    """

    return render_template("index.html")


# Number verification initiation


@app.route("/verify/<number>")
def verify(number):
    """
    verify(number) accepts a number and initiates verification for it.
    """
    try:
        code = current_app.p2fa.generate_code()
        if app.config["PHLO_ID"] == "":
            {
                current_app.p2fa.send_verification_code_sms(
                    number,
                    f'Your verification code is "{code}". Code will expire in 1 minute. ',
                )  # String should be less than 160 chars
            }
        else:
            {current_app.p2fa.send_verification_code_phlo(number, code, "sms")}
        current_app.redis.setex(
            "number:%s:code" % number, 60, code
        )  # Verification code is valid for 1 min
        return jsonify({"status": "success", "message": "verification initiated"})
    except:
        return ("Error encountered", 400)


# Code validation endpoint
@app.route("/verify_voice/<number>")
def verify_voice(number):
    """
    verify(number) accepts a number and initiates verification for it.
    """
    try:
        code = current_app.p2fa.generate_code()

        if app.config["PHLO_ID"] == "":
            {current_app.p2fa.send_verification_code_voice(number,code)}
        else:
            {current_app.p2fa.send_verification_code_phlo(number, code, "call")}
        current_app.redis.setex("number:%s:code" % number, 60, code)  # Verification code is valid for 1 min
        return (jsonify({"status": "success", "message": "verification initiated"}),200,)
    except:
        return ("Error encountered", 400)


@app.route("/checkcode/<number>/<code>")
def check_code(number, code):
    """
    check_code(number, code) accepts a number and the code entered by the user and
    tells if the code entered for that number is correct or not.
    """

    original_code = current_app.redis.get("number:%s:code" % number)
    if original_code == code:  # verification successful, delete the code
        current_app.redis.delete("number:%s:code" % number)
        return (jsonify({"status": "success", "message": "codes match! number verified"}),200,)
    elif original_code != code:
        return (
            jsonify(
                {
                    "status": "rejected",
                    "message": "codes do not match! number not verified",
                }
            ),
            404,
        )
    else:
        return (jsonify({"status": "failed", "message": "number not found!"}), 500)
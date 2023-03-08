import requests
from database import Database
from constants import PACKET_ENCODER_URL


class Encoder():


    @staticmethod
    def packet_type(PHYPayload:str) -> str:
        post_json = {}
        post_json["PHYPayload"] = PHYPayload
        response = requests.post(PACKET_ENCODER_URL+"MessageType", json=post_json)
        # To be sure that everything is ok
        while response.status_code != 200:
            response = requests.post(PACKET_ENCODER_URL+"MessageType", json=post_json)
        return response.json()["MessageType"]


    @staticmethod
    def join_request(device:dict) -> dict:
        post_json = {}
        post_json["DevEUI"] = device["DevEUI"]
        post_json["AppEUI"] = device["AppEUI"]
        post_json["AppKey"] = device["AppKey"]
        post_json["DevNonce"] = hex(device["DevNonce"])[2:].zfill(4)
        response = requests.post(PACKET_ENCODER_URL+"JoinRequest", json=post_json)
        # To be sure that everything is ok
        while response.status_code != 200:
            response = requests.post(PACKET_ENCODER_URL+"JoinRequest", json=post_json)
        _db = Database()
        print(device)
        _db.open()
        _db.update_dev_nonce(device["DevEUI"], device["DevNonce"]+1)
        _db.close()
        return response.json()


    @staticmethod
    def join_accept(device:dict, PHYPayload:str) -> dict:
        """Update device after decoding Join Accept PHYPayload"""
        post_json = {}
        post_json["AppKey"] = device["AppKey"]
        post_json["DevNonce"] = hex(device["DevNonce"]-1)[2:].zfill(4)
        post_json["PHYPayload"] = PHYPayload
        response = requests.post(PACKET_ENCODER_URL+"JoinAccept", json=post_json)
        # To be sure that everything is ok
        while response.status_code != 200:
            response = requests.post(PACKET_ENCODER_URL+"JoinAccept", json=post_json)
        # Update device infos with session keys
        response = response.json()
        device["DevAddr"] = response["DevAddr"]
        device["NwkSKey"] = response["NwkSKey"]
        device["AppSKey"] = response["AppSKey"]
        _db = Database()
        _db.open()
        _db.update_session_keys(device["DevEUI"], device["DevAddr"], device["NwkSKey"], device["AppSKey"])
        _db.update_f_cnt(device["DevEUI"])
        _db.close()
        return device


    @staticmethod
    def unconfirmed_data_up(device:dict, payload:str) -> dict:
        post_json = {}
        post_json["DevAddr"] = device["DevAddr"]
        post_json["NwkSKey"] = device["NwkSKey"]
        post_json["AppSKey"] = device["AppSKey"]
        post_json["FPort"]   = device["FPort"]
        post_json["FCnt"]    = device["FCnt"]
        post_json["payload"] = payload
        response = requests.post(PACKET_ENCODER_URL+"UnConfirmedDataUp", json=post_json)
        # To be sure that everything is ok
        while response.status_code != 200:
            response = requests.post(PACKET_ENCODER_URL+"UnConfirmedDataUp", json=post_json)
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response.json()



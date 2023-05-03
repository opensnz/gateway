import requests
from database import Database
from lorawan_wrapper import LoRaWAN

class Encoder():


    @staticmethod
    def packet_type(PHYPayload:str) -> str:
        return LoRaWAN.message_type(PHYPayload)


    @staticmethod
    def join_request(device:dict) -> dict:
        response = LoRaWAN.join_request(device["DevEUI"], device["AppEUI"], device["AppKey"], device["DevNonce"])
        _db = Database()
        _db.open()
        _db.update_dev_nonce(device["DevEUI"], device["DevNonce"]+1)
        _db.close()
        return response


    @staticmethod
    def join_accept(device:dict, PHYPayload:str) -> dict:
        """Update device after decoding Join Accept PHYPayload"""
        response = LoRaWAN.join_accept(PHYPayload, device["AppKey"], device["DevNonce"]-1)
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

        response =  LoRaWAN.unconfirmed_data_up(device["DevAddr"], device["FCnt"], device["FPort"], payload, 
                                                device["NwkSKey"], device["AppSKey"])
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response


    @staticmethod
    def confirmed_data_up(device:dict, payload:str) -> dict:

        response =  LoRaWAN.confirmed_data_up(device["DevAddr"], device["FCnt"], device["FPort"], payload, 
                                                device["NwkSKey"], device["AppSKey"])
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response
    

    @staticmethod
    def data_down(device:dict, PHYPayload:str) -> dict:
        response = {}
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response
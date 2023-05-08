import base64
from database import Database
from lorawan_wrapper import WrapperLoRaWAN

class LoRaWAN():


    @staticmethod
    def packet_type(PHYPayload:str) -> str:
        return WrapperLoRaWAN.message_type(PHYPayload)


    @staticmethod
    def join_request(device:dict) -> dict:
        response = WrapperLoRaWAN.join_request(device["DevEUI"], device["AppEUI"], device["AppKey"], device["DevNonce"])
        _db = Database()
        _db.open()
        _db.update_dev_nonce(device["DevEUI"], device["DevNonce"]+1)
        _db.close()
        return response


    @staticmethod
    def join_accept(device:dict, PHYPayload:str) -> dict|None:
        """Update device after decoding Join Accept PHYPayload"""
        response = WrapperLoRaWAN.join_accept(PHYPayload, device["AppKey"], device["DevNonce"]-1)
        if response is None:
            print("JoinAccept Failed")
            return None
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

        response =  WrapperLoRaWAN.unconfirmed_data_up(device["DevAddr"], device["FCnt"], device["FPort"], payload, 
                                                device["NwkSKey"], device["AppSKey"])
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response


    @staticmethod
    def confirmed_data_up(device:dict, payload:str) -> dict:

        response =  WrapperLoRaWAN.confirmed_data_up(device["DevAddr"], device["FCnt"], device["FPort"], payload, 
                                                device["NwkSKey"], device["AppSKey"])
        _db = Database()
        _db.open()
        _db.update_f_cnt(device["DevEUI"], device["FCnt"]+1)
        _db.close()
        return response
    

    @staticmethod
    def data_down(PHYPayload:str) -> dict|None:
        # Get DevAddr from PHYPayload
        # devAddr = bytes from index 1 to 4 of PHYPayload (little endian)
        PHYPayloadBytes = base64.b64decode(PHYPayload)
        devAddr = bytearray(PHYPayloadBytes[1:5])
        devAddr.reverse() # to big endian
        DevAddr = devAddr.hex().zfill(8)

        _db = Database()
        _db.open() 
        devices = _db.get_devices_by_devaddr(DevAddr=DevAddr)
        _db.close()

        response = None

        for device in devices:
            response = WrapperLoRaWAN.data_down(PHYPayload, device["DevAddr"],
                                                device["NwkSKey"], device["AppSKey"])
            if response is not None:
                device["payload"]=response["payload"]
                device["FPort"]=response["FPort"]
                device["ack"]=response["ack"]
                return device
        
        return None

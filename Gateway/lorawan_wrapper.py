from lorawan_functions import messageType, joinRequest,joinAccept, unconfirmedDataUp, confirmedDataUp, dataDown
from lorawan_types import *
import ctypes
import base64


class WrapperLoRaWAN :
    """LoRaWAN Wrapper Class to C Shared Library"""

    LORAWAN_MAX_FOPTS_LEN = 15
    LORAWAN_BUFFER_SIZE_MAX = 224
    MESSAGE_TYPE = ["JoinRequest", "JoinAccept", "UnconfirmedDataUp", "UnconfirmedDataDown",
                    "ConfirmedDataUp", "ConfirmedDataDown", "ConfirmedDataUp", "ReJoinRequest", "Proprietary"]

    @staticmethod
    def message_type(PHYPayload:str) -> str :

        phyPayload = base64.b64decode(PHYPayload)

        bufferSize = len(phyPayload)
        buffer = (ctypes.c_uint8 * bufferSize)()
        ctypes.memmove(ctypes.addressof(buffer), phyPayload, bufferSize)

        msg_type : MHDR_MType_t = messageType(buffer, bufferSize)

        return WrapperLoRaWAN.MESSAGE_TYPE[msg_type.value]


    @staticmethod
    def join_request(DevEUI:str, AppEUI:str, AppKey:str, DevNonce:int) -> dict :

        devEUI = tuple(bytes.fromhex(DevEUI))
        appEUI = tuple(bytes.fromhex(AppEUI))
        appKey = tuple(bytes.fromhex(AppKey))

        join = JoinRequest_t(devEUI, appEUI, appKey, DevNonce)
        buffer = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = joinRequest(ctypes.byref(join), buffer, bufferSize)

        output = {}
        PHYPayload = []
        for i in range(length):
            PHYPayload.append(buffer[i])
        output["PHYPayload"] = base64.b64encode(bytes(PHYPayload)).decode()
        output["size"] = int(length)

        return output
    
    
    @staticmethod
    def join_accept(PHYPayload:str, AppKey:str, DevNonce:int) -> dict|None :

        phyPayload = base64.b64decode(PHYPayload)
        appKey = tuple(bytes.fromhex(AppKey))

        DLsettings_data = DLsettings_t(0, 0, False)
        FreqCH4 = (ctypes.c_uint8 * 3)()
        FreqCH5 = (ctypes.c_uint8 * 3)()
        FreqCH6 = (ctypes.c_uint8 * 3)()
        FreqCH7 = (ctypes.c_uint8 * 3)()
        FreqCH8 = (ctypes.c_uint8 * 3)()
        CFlist_data = CFlist_t(FreqCH4, FreqCH5, FreqCH6, FreqCH7, FreqCH8)
        AppNonce = 0
        NetID = 0
        DevAddr = 0
        RxDelay = 0
        hasCFlist = False
        NwkSKey = (ctypes.c_uint8 * 16)()
        AppSKey = (ctypes.c_uint8 * 16)()
        join = JoinAccept_t(AppNonce, NetID, DevAddr, DLsettings_data, RxDelay, CFlist_data, hasCFlist, DevNonce, appKey, NwkSKey, AppSKey)

        bufferSize = len(phyPayload)
        buffer = (ctypes.c_uint8 * bufferSize)()
        ctypes.memmove(ctypes.addressof(buffer), phyPayload, bufferSize)

        status = joinAccept(ctypes.byref(join), buffer, bufferSize)

        if status == False:
            return None

        output = {}
        output["DevAddr"] = hex(join.DevAddr)[2:].zfill(8)
        NwkSKey = []
        AppSKey = []
        for i in range(16):
            NwkSKey.append(join.NwkSKey[i])
            AppSKey.append(join.AppSKey[i])

        output["NwkSKey"] = bytes(NwkSKey).hex()
        output["AppSKey"] = bytes(AppSKey).hex()

        return output
    

    @staticmethod
    def unconfirmed_data_up(DevAddr:str, FCnt:int, FPort:int, Payload:str, NwkSKey:str, AppSKey:str) -> dict:

        payload = tuple(bytes.fromhex(Payload))
        nwkSKey = tuple(bytes.fromhex(NwkSKey))
        appSKey = tuple(bytes.fromhex(AppSKey))

        FHDR_FCtrl_uplink_data = FHDR_FCtrl_uplink_t(False, False, True, False, 0)
        FHDR_FCtrl_data = FHDR_FCtrl_t((),FHDR_FCtrl_uplink_data)
        FOpts = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_MAX_FOPTS_LEN)()

        FHDR_data = FHDR_t(int(DevAddr, 16), FHDR_FCtrl_data, FCnt, FOpts)

        mac = MACPayload_t(FHDR_data, nwkSKey, appSKey, FPort, len(payload), payload)
        buffer = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = unconfirmedDataUp(ctypes.byref(mac), buffer, bufferSize)
    
        output = {}
        PHYPayload = []
        for i in range(length):
            PHYPayload.append(buffer[i])
        output["PHYPayload"] = base64.b64encode(bytes(PHYPayload)).decode()
        output["size"] = int(length)

        return output

    @staticmethod
    def confirmed_data_up(DevAddr:str, FCnt:int, FPort:int, Payload:str, NwkSKey:str, AppSKey:str) -> dict:
        
        payload = tuple(bytes.fromhex(Payload))
        nwkSKey = tuple(bytes.fromhex(NwkSKey))
        appSKey = tuple(bytes.fromhex(AppSKey))

        FHDR_FCtrl_uplink_data = FHDR_FCtrl_uplink_t(False, False, True, False, 0)
        FHDR_FCtrl_data = FHDR_FCtrl_t((),FHDR_FCtrl_uplink_data)
        FOpts = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_MAX_FOPTS_LEN)()

        FHDR_data = FHDR_t(int(DevAddr, 16), FHDR_FCtrl_data, FCnt, FOpts)

        mac = MACPayload_t(FHDR_data, nwkSKey, appSKey, FPort, len(payload), payload)
        buffer = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = confirmedDataUp(ctypes.byref(mac), buffer, bufferSize)

        output = {}
        PHYPayload = []
        for i in range(length):
            PHYPayload.append(buffer[i])
        output["PHYPayload"] = base64.b64encode(bytes(PHYPayload)).decode()
        output["size"] = int(length)

        return output

    @staticmethod
    def data_down(PHYPayload:str, DevAddr:str, NwkSKey:str, AppSKey:str) -> dict|None:
        
        phyPayload = base64.b64decode(PHYPayload)
        nwkSKey = tuple(bytes.fromhex(NwkSKey))
        appSKey = tuple(bytes.fromhex(AppSKey))

        FHDR_FCtrl_downlink_data = FHDR_FCtrl_downlink_t(False, False, False, False, 0)
        FHDR_FCtrl_data = FHDR_FCtrl_t(FHDR_FCtrl_downlink_data, ())
        FOpts = (ctypes.c_uint8 * WrapperLoRaWAN.LORAWAN_MAX_FOPTS_LEN)()
        
        FHDR_data = FHDR_t(int(DevAddr, 16), FHDR_FCtrl_data, 0, FOpts)

        payloadSize = WrapperLoRaWAN.LORAWAN_BUFFER_SIZE_MAX
        payload = (ctypes.c_uint8 * payloadSize)()

        mac = MACPayload_t(FHDR_data, nwkSKey, appSKey, 0, payloadSize, payload)
        
        bufferSize = len(phyPayload)
        buffer = (ctypes.c_uint8 * bufferSize)()

        ctypes.memmove(ctypes.addressof(buffer), phyPayload, bufferSize)

        status = dataDown(ctypes.byref(mac), buffer, bufferSize)

        if status == False:
            return None
        
        output = {}
        payload = ""
        for i in range(mac.payloadSize):
            payload = payload + hex(mac.payload[i])[2:].zfill(2)
        output["payload"]=payload
        output["adr"]=bool(mac.FHDR.FCtrl.downlink.ADR)
        output["rfu"]=bool(mac.FHDR.FCtrl.downlink.RFU)
        output["ack"]=bool(mac.FHDR.FCtrl.downlink.ACK)
        output["FCntDown"]=int(mac.FHDR.FCnt16)
        output["FPort"]=int(mac.FPort)

        return output




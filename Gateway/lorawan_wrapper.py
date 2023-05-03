from lorawan_functions import messageType, joinRequest,joinAccept, unconfirmedDataUp, confirmedDataUp, dataDown
from lorawan_types import *
import ctypes
import base64


class LoRaWAN :
    """LoRaWAN Wrapper Class to C Shared Library"""

    LORAWAN_MAX_FOPTS_LEN = 15
    LORAWAN_BUFFER_SIZE_MAX = 254
    MESSAGE_TYPE = ["JoinRequest", "JoinAccept", "UnconfirmedDataUp", "UnconfirmedDataDown",
                    "ConfirmedDataUp", "ConfirmedDataDown", "ConfirmedDataUp", "ReJoinRequest", "Proprietary"]

    @staticmethod
    def message_type(PHYPayload:str) -> str :

        phyPayload = base64.b64decode(PHYPayload)

        bufferSize = len(phyPayload)
        buffer = (ctypes.c_uint8 * bufferSize)()
        ctypes.memmove(ctypes.addressof(buffer), phyPayload, bufferSize)

        msg_type : MHDR_MType_t = messageType(buffer, bufferSize)

        return LoRaWAN.MESSAGE_TYPE[msg_type.value]


    @staticmethod
    def join_request(DevEUI:str, AppEUI:str, AppKey:str, DevNonce:int) -> dict :

        devEUI = tuple(bytes.fromhex(DevEUI))
        appEUI = tuple(bytes.fromhex(AppEUI))
        appKey = tuple(bytes.fromhex(AppKey))

        joinRequestData = JoinRequest_t(devEUI, appEUI, appKey, DevNonce)
        buffer = (ctypes.c_uint8 * LoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = LoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = joinRequest(ctypes.byref(joinRequestData), buffer, bufferSize)

        output = {}
        PHYPayload = []
        for i in range(length):
            PHYPayload.append(buffer[i])
        output["PHYPayload"] = base64.b64encode(bytes(PHYPayload)).decode()
        output["size"] = int(length)

        return output
    
    
    @staticmethod
    def join_accept(PHYPayload:str, AppKey:str, DevNonce:int) -> dict :

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
        JoinAccept_data = JoinAccept_t(AppNonce, NetID, DevAddr, DLsettings_data, RxDelay, CFlist_data, hasCFlist, DevNonce, appKey, NwkSKey, AppSKey)

        bufferSize = len(phyPayload)
        buffer = (ctypes.c_uint8 * bufferSize)()
        ctypes.memmove(ctypes.addressof(buffer), phyPayload, bufferSize)

        length = joinAccept(ctypes.byref(JoinAccept_data), buffer, bufferSize)

        output = {}
        output["DevAddr"] = hex(JoinAccept_data.DevAddr)[2:].zfill(8)
        NwkSKey = []
        AppSKey = []
        for i in range(16):
            NwkSKey.append(JoinAccept_data.NwkSKey[i])
            AppSKey.append(JoinAccept_data.AppSKey[i])

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
        FOpts = (ctypes.c_uint8 * LoRaWAN.LORAWAN_MAX_FOPTS_LEN)()

        FHDR_data = FHDR_t(int(DevAddr, 16), FHDR_FCtrl_data, FCnt, FOpts)

        unconfirmedDataUpData = MACPayload_t(FHDR_data, nwkSKey, appSKey, FPort, len(payload), payload)
        buffer = (ctypes.c_uint8 * LoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = LoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = unconfirmedDataUp(ctypes.byref(unconfirmedDataUpData), buffer, bufferSize)
    
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
        FOpts = (ctypes.c_uint8 * LoRaWAN.LORAWAN_MAX_FOPTS_LEN)()

        FHDR_data = FHDR_t(int(DevAddr, 16), FHDR_FCtrl_data, FCnt, FOpts)

        confirmedDataUpData = MACPayload_t(FHDR_data, nwkSKey, appSKey, FPort, len(payload), payload)
        buffer = (ctypes.c_uint8 * LoRaWAN.LORAWAN_BUFFER_SIZE_MAX)()
        bufferSize = LoRaWAN.LORAWAN_BUFFER_SIZE_MAX

        length = confirmedDataUp(ctypes.byref(confirmedDataUpData), buffer, bufferSize)

        output = {}
        PHYPayload = []
        for i in range(length):
            PHYPayload.append(buffer[i])
        output["PHYPayload"] = base64.b64encode(bytes(PHYPayload)).decode()
        output["size"] = int(length)

        return output

    @staticmethod
    def data_down(DevAddr:str, FCnt:int, FPort:int, FRMPayload:str, NwkSKey:str, AppSKey:str, DevNonce:int) -> dict:

        output = {}

        return output




import ctypes
from lorawan_types import *
from sys import platform

if platform == "win32" : 
    libLoRaWAN = ctypes.CDLL("./lorawan.dll")
elif platform == "linux":
    libLoRaWAN = ctypes.CDLL("./lorawan.so")


messageType = libLoRaWAN.LoRaWAN_MessageType
messageType.argtypes = [ctypes.POINTER(ctypes.c_uint8), 
                        ctypes.c_uint8]
messageType.restype = MHDR_MType_t


joinRequest = libLoRaWAN.LoRaWAN_JoinRequest
joinRequest.argtypes = [ctypes.POINTER(JoinRequest_t), 
                        ctypes.POINTER(ctypes.c_uint8), 
                        ctypes.c_uint8]
joinRequest.restype = ctypes.c_uint8


joinAccept = libLoRaWAN.LoRaWAN_JoinAccept
#bool LoRaWAN_JoinAccept(JoinAccept_t * packet, uint8_t* buffer, uint8_t bufferSize);
joinAccept.argtypes = [ctypes.POINTER(JoinAccept_t), 
                        ctypes.POINTER(ctypes.c_uint8), 
                        ctypes.c_uint8]
joinAccept.restype = ctypes.c_bool


unconfirmedDataUp = libLoRaWAN.LoRaWAN_UnconfirmedDataUp
unconfirmedDataUp.argtypes  =  [ctypes.POINTER(MACPayload_t), 
                                ctypes.POINTER(ctypes.c_uint8), 
                                ctypes.c_uint8]
unconfirmedDataUp.restype = ctypes.c_uint8


confirmedDataUp = libLoRaWAN.LoRaWAN_ConfirmedDataUp
confirmedDataUp.argtypes  =  [ctypes.POINTER(MACPayload_t), 
                                ctypes.POINTER(ctypes.c_uint8), 
                                ctypes.c_uint8]
confirmedDataUp.restype = ctypes.c_uint8


dataDown = libLoRaWAN.LoRaWAN_DataDown
dataDown.argtypes = [ctypes.POINTER(MACPayload_t), 
                    ctypes.POINTER(ctypes.c_uint8), 
                    ctypes.c_uint8]
dataDown.restype = ctypes.c_bool




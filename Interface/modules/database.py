import sqlite3
from modules.constants import SQLITE_DATABASE_PATH

TABLE_DEVICE_QUERY = """
CREATE TABLE IF NOT EXISTS DEVICE (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DevEUI VARCHAR(16) NOT NULL UNIQUE,
    AppEUI VARCHAR(16) NOT NULL,
    AppKey VARCHAR(32) NOT NULL,
    DevNonce INTEGER DEFAULT 1,
    DevAddr VARCHAR(8),
    NwkSKey VARCHAR(32),
    AppSKey VARCHAR(32),
    FCnt INTEGER DEFAULT 1,
    FPort INTEGER DEFAULT 2,
    Created_at TIMESTAMP DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now', 'utc'))
);
"""
TABLE_DATA_QUERY = """
CREATE TABLE IF NOT EXISTS DATA (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DevEUI VARCHAR(16) NOT NULL,
    Packet TEXT,
    Created_at TIMESTAMP DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now', 'utc'))
);
"""


SELECT_DEVICES_QUERY = "SELECT * FROM DEVICE "
SELECT_DEVICE_QUERY  = "SELECT * FROM DEVICE WHERE DevEUI = ? "
INSERT_DEVICE_QUERY  = "INSERT INTO DEVICE(DevEUI, AppEUI, AppKey) VALUES(?, ?, ?) "
UPDATE_DEVICE_QUERY  = "UPDATE DEVICE SET "
DELETE_DEVICE_QUERY  = "DELETE FROM DEVICE WHERE DevEUI = ? "

SELECT_ALL_DATA_QUERY= "SELECT * FROM DATA "
SELECT_DATA_QUERY    = "SELECT * FROM DATA WHERE DevEUI = ? "
INSERT_DATA_QUERY    = "INSERT INTO DATA(DevEUI, Packet) VALUES(?, ?) "
DELETE_DATA_QUERY    = "DELETE FROM DATA WHERE DevEUI = ? "
DELETE_ALL_DATA_QUERY= "DELETE FROM DATA"

DEFAULT_GATEWAYEUI   = "0000000000000000"
DEFAULT_APPEUI       = "0000000000000000"

class COLOR:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

class Database():

    def __init__(self, database_name : str = SQLITE_DATABASE_PATH):
        self.__name = database_name
        self.__connection : sqlite3.Connection = None
        self.__cursor : sqlite3.Cursor = None

    def open(self):
        self.__connection = sqlite3.connect(self.__name)
        self.__cursor = self.__connection.cursor()

    def close(self):
        if self.__connection != None:
            self.__connection.close()
            self.__connection = None
            self.__cursor = None

    def __connected__(self):
        if self.__connection == None :
            print(COLOR.FAIL+"No connection"+COLOR.END)
            return False
        return True

    def create_tables(self) -> bool:
        if self.__connected__() is not True:
            return False
        self.__cursor.execute(TABLE_DEVICE_QUERY)
        self.__cursor.execute(TABLE_DATA_QUERY)
        self.__connection.commit()
        return True



    ######################## Table DEVICE CRUD methods #############################

    def __get_device__(self, item:tuple=None) -> dict:
        if item is None or len(item) != 11:
            return None
        device = {}
        device["DevEUI"]   = item[1]
        device["AppEUI"]   = item[2]
        device["AppKey"]   = item[3]
        device["DevNonce"] = item[4]
        device["DevAddr"]  = item[5]
        device["NwkSKey"]  = item[6]
        device["AppSKey"]  = item[7]
        device["FCnt"]     = item[8]
        device["FPort"]    = item[9]
        device["Created_at"]  = item[10]
        return device
    
    def get_device(self, DevEUI:str=None) -> dict:
        if self.__connected__() is not True:
            return None
        if DevEUI == None:
            print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
            return False
        self.__cursor.execute(SELECT_DEVICE_QUERY, (DevEUI,))
        item = self.__cursor.fetchone()
        return self.__get_device__(item)
    
    def get_devices(self) -> list:
        devices = []
        if self.__connected__() is not True:
            return devices
        self.__cursor.execute(SELECT_DEVICES_QUERY)
        items = self.__cursor.fetchall()
        for item in items:
            device = self.__get_device__(item)
            if device is not None:
                devices.append(device)
        return devices

    def insert_device(self, DevEUI:str=None, AppEUI:str=DEFAULT_APPEUI, AppKey:str=None) -> bool:
        try:
            if self.__connected__() is not True:
                return False
            if DevEUI == None or AppKey == None:
                print(COLOR.FAIL+"DevEUI or AppEUI can't be none"+COLOR.END)
                return False
            self.__cursor.execute(INSERT_DEVICE_QUERY, (DevEUI, AppEUI, AppKey,))
            self.__cursor.connection.commit()
            return self.__insert_data__(DevEUI=DevEUI)
        except:
            return False
    
    def update_dev_nonce(self, DevEUI:str=None, DevNonce:int=1) -> bool:
        try:
            if self.__connected__() is not True:
                return False
            if DevEUI == None:
                print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
                return False
            if DevNonce <= 0 or DevNonce >= 65536:
                print(COLOR.FAIL+"DevNonce must be between 1 and 65535"+COLOR.END)
                return False
            query = UPDATE_DEVICE_QUERY + "DevNonce = ? " \
                                        + "WHERE DevEUI = ?"
            self.__cursor.execute(query, (DevNonce, DevEUI,))
            self.__connection.commit()
            return True
        except:
            return False

    def update_f_cnt(self, DevEUI:str=None, FCnt:int=1) -> bool:
        try:
            if self.__connected__() is not True:
                return False
            if DevEUI == None:
                print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
                return False
            if FCnt <= 0 or FCnt >= 65536:
                print(COLOR.FAIL+"FCnt must be between 1 and 65535"+COLOR.END)
                return False
            query = UPDATE_DEVICE_QUERY + "FCnt = ? " \
                                        + "WHERE DevEUI = ?"
            self.__cursor.execute(query, (FCnt, DevEUI,))
            self.__connection.commit()
            return True
        except:
            return False

    def update_session_keys(self, DevEUI:str=None, DevAddr:str=None, NwkSKey:str=None, AppSKey:str=None) -> bool:
        try:
            if self.__connected__() is not True:
                return False
            if DevEUI == None or DevAddr == None or NwkSKey == None or AppSKey == None:
                print(COLOR.FAIL+"DevEUI or DevAddr or NwkSKey or AppSKey can't be none"+COLOR.END)
                return False
            query = UPDATE_DEVICE_QUERY + "DevAddr = ?, " \
                                        + "NwkSKey = ?, " \
                                        + "AppSKey = ? " \
                                        + "WHERE DevEUI = ?"
            self.__cursor.execute(query, (DevAddr, NwkSKey, AppSKey, DevEUI,))
            self.__connection.commit()
            return True
        except:
            return False
    
    def delete_device(self, DevEUI:str=None) -> bool:
        try:
            if self.__connected__() is not True:
                return False
            if DevEUI == None:
                print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
                return False
            self.__cursor.execute(DELETE_DEVICE_QUERY, (DevEUI,))
            self.__connection.commit()
            return self.__delete_device_data__(DevEUI=DevEUI)
        except:
            return False

    ######################## Table DATA CRUD methods #############################

    def __get_device_data__(self, item:tuple=None) -> dict:
        if item is None or len(item) != 4:
            return None
        data = {}
        data["DevEUI"] = item[1]
        data["Packet"] = item[2]
        data["Created_at"] = item[3]
        return data
    
    def get_device_data(self, DevEUI:str=None) -> dict:
        device_data = []
        if self.__connected__() is not True:
            return None
        if DevEUI == None:
            print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
            return False
        self.__cursor.execute(SELECT_DATA_QUERY, (DevEUI,))
        items = self.__cursor.fetchall()
        for item in items:
            data = self.__get_device_data__(item)
            if data is not None:
                device_data.append(data)
        return device_data
    
    def get_all_data(self) -> list:
        all_data = []
        if self.__connected__() is not True:
            return all_data
        self.__cursor.execute(SELECT_ALL_DATA_QUERY)
        items = self.__cursor.fetchall()
        for item in items:
            data = self.__get_device_data__(item)
            if data is not None:
                all_data.append(data)
        return all_data

    def insert_device_data(self, DevEUI:str=None, Packet:str=None) -> bool:
        if self.__connected__() is not True:
            return False
        if DevEUI == None:
            print(COLOR.FAIL+"DevEUI or Data can't be none"+COLOR.END)
            return False
        self.__cursor.execute(INSERT_DATA_QUERY, (DevEUI, Packet))
        self.__connection.commit()
        return True

    def __delete_device_data__(self, DevEUI:str=None) -> bool:
        if self.__connected__() is not True:
            return False
        if DevEUI == None:
            print(COLOR.FAIL+"DevEUI can't be none"+COLOR.END)
            return False
        self.__cursor.execute(DELETE_DATA_QUERY, (DevEUI,))
        self.__connection.commit()
        return True

    def delete_device_data(self, DevEUI:str=None) -> bool:
        return self.__delete_device_data__(DevEUI)


    def delete_all_data(self) -> bool:
        if self.__connected__() is not True:
            return False
        self.__cursor.execute(DELETE_ALL_DATA_QUERY)
        self.__connection.commit()
        return True

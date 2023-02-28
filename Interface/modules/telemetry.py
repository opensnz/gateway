import json, psutil, platform, socket

class CPU:

    # constructor
    def __init__(self):
        frequency = psutil.cpu_freq()
        #self.temperatures : float = psutil.sensors_temperatures()
        self.frequency_current : float = frequency.current
        self.frequency_min : float = frequency.min
        self.frequency_max : float = frequency.max
        self.cores : int = psutil.cpu_count()
        self.percent : float = round(psutil.cpu_percent(), ndigits=2)
        

class RAM:

    # constructor
    def __init__(self):
        ram = psutil.virtual_memory()
        self.total : float = round(ram.total / (1024**3), ndigits=2)
        self.available : float = round(ram.available / (1024**3), ndigits=2)
        self.percent : float = round(ram.percent, ndigits=2)
        self.used : float = round(ram.used / (1024**3), ndigits=2)
        if platform.system()=='Linux':
            self.active : float = round(ram.active / (1024**3), ndigits=2)
            self.shared : float = round(ram.shared / (1024**3), ndigits=2)
            self.cached : float = round(ram.cached / (1024**3), ndigits=2)
            self.slab : float = round(ram.slab / (1024**3), ndigits=2)


class DISK:

    # constructor
    def __init__(self):
        disk = psutil.disk_usage('/')
        self.total : float = round(disk.total / (1024**3), ndigits=2)
        self.free : float = round(disk.free / (1024**3), ndigits=2)
        self.used : float = round(disk.used / (1024**3), ndigits=2)
        self.percent : float = round(disk.percent, ndigits=2)


class PLATFORM:

    # constructor
    def __init__(self):
        self.system : str = platform.system()
        self.system_release : str = platform.release()
        self.system_version : str = platform.version()
        self.architecture : str = platform.machine()
        self.processor : str = platform.processor()


class NETWORK:

    # constructor
    def __init__(self):
        self.interfaces = list()
        for interface in psutil.net_if_addrs().items():
            name = interface[0]
            mac = ""
            ipv4 = ""
            mask = ""
            ipv6 = ""
            for snic in interface[1]:
                if(snic.family == socket.AddressFamily.AF_INET):
                    ipv4 = snic.address
                    mask = snic.netmask
                elif(snic.family == socket.AddressFamily.AF_INET6):
                    ipv6 = snic.address
                elif (snic.family == psutil.AF_LINK) :
                    mac = snic.address
            self.interfaces.append(INTERFACE(name, mac, ipv4, mask, ipv6))


class INTERFACE:

    # constructor
    def __init__(self, name, mac, ipv4, mask, ipv6):
        self.name = name
        self.mac  = mac
        self.ipv4 = ipv4
        self.mask = mask
        self.ipv6 = ipv6
    


class Telemetry:
    
    # constructor
    def __init__(self):
        self.cpu = CPU()
        self.memory = RAM()
        self.disk = DISK()
        self.platform = PLATFORM()
        self.network = NETWORK()
    
    # static method (return json format)
    @staticmethod
    def to_json():
        telemetry = Telemetry()
        return json.dumps(telemetry, default=lambda o:o.__dict__, sort_keys=True)

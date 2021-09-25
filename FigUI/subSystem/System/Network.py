import parse
import argparse
import platform 
# import os, sys
import subprocess

# trying to make a more "proper" class
class LinuxNetInfo:
    '''
    Information about a given network (for Linux)
    '''
    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs:
            setattr(self, "_"+attr_name, attr_value)

    @property
    def name(self):
        '''name (ESSID) of network'''
        return self._name

    @name.setter
    def name(self, val):
        val = str(val)
        self._name = val

    @name.deleter
    def name(self):
        del self._name

    @property
    def bit_rate(self):
        '''Bit rate of the network (e.g. 65 Mb/s)'''
        return self._bit_rate

    @property
    def power(self):
        '''Tx-Power in dBm'''
        return self._power

    @property
    def frequency(self):
        '''Frequency in GHz e.g. frequency: 2.462GHz'''
        return self._frequency

    @property
    def standard(self):
        '''IEEE standard'''
        return self._standard

    @property
    def access_point(self):
        '''Access point, e.g.: BA:DD:71:A0:36:EC'''
        return self._access_point

    @property
    def retry_limit(self):
        '''Retry short limit'''
        return self._retry_limit

    @property
    def rts_thresh(self):
        '''RTS threshold'''
        return self._rts_thresh

    @property
    def power_management(self):
        '''Bool flag whether power management is on/off'''
        return self._power_management

    @property
    def link_quality(self):
        pass    


class LinuxNetInfo(argparse.Namespace):
    def __init__(self, *args, **kwargs):
        super(LinuxNetInfo, self).__init__(*args, **kwargs)
        self.templates = [
            ('''{} IEEE {} ESSID:"{}"''', 
            ["type", "ieee_std", "name"]),
            ('''Mode:{} Frequency:{} Access Point: {}''',
            ["mode", "frequency", "access_point"]),
            ('''Bit Rate={} Tx-Power={}''',
            ["bit_rate", "power"]),
            ('''Retry short limit:{} RTS thr:{} Fragment thr:{}''',
            ["retry_limit", "rts_thresh", "frag_thresh"]),
            ('''Power Management:{}''',
            ["power_management"]),
            ('''Link Quality={} Signal level={}''',
            ["link_quality", "signal_level"]),
            ('''Rx invalid nwid:{} Rx invalid crypt:{}  Rx invalid frag:{}''',
            ["invalid_nwid", "invalid_crypt", "invalid_frag"]),
            ('''Tx excessive retries:{} Invalid misc:{} Missed beacon:{}''',
            ["excess_retries", "invalid_misc", "missed_beacon"]),
            # ('',[]),
        ]

    def parse(self, raw_str):
        raw_str = raw_str.strip("\n")
        for i, line in enumerate(raw_str.split("\n")):
            line = line.strip()
            template = self.templates[i][0]
            attr_values = parse.parse(template, line)
            # set attribute values from parsed output.
            for j, attr_name in enumerate(self.templates[i][1]):
                setattr(self, 
                        attr_name, 
                        attr_values[j].strip())

    def serialize(self, prefix: str, attr: str) -> str:
        attr_val = getattr(self, attr)
        return prefix + ": " + attr_val + "\n"

    def __str__(self):
        op = "# Network Details:\n\n"
        op += "## Metadata:\n"
        op += self.serialize('Name', 'name')
        op += self.serialize('IEEE', 'ieee_std')
        op += self.serialize('Type', 'type')
        op += self.serialize('Mode', 'mode')
        op += self.serialize('Access Point', 'access_point')
        op += "\n"
        # physical metrics.
        op += "## Metrics:\n"
        op += self.serialize('Frequency', 'frequency')
        op += self.serialize('Bit Rate', 'bit_rate')
        op += self.serialize('Power', 'power')
        op += self.serialize('Power Management', 'power_management')
        op += self.serialize('Signal Level', 'signal_level')
        op += "\n"
        # limits and thresholds
        op += "## Limits and Thresholds:\n"
        op += self.serialize('Retry Short Limit', 'retry_limit')
        op += self.serialize('Tx Excess Retries', 'excess_retries')
        op += self.serialize('RTS Threshold', 'rts_thresh')
        op += self.serialize('Fragment Threshold', 'frag_thresh')
        op += self.serialize('Link Quality', 'link_quality')
        op += "\n"
        # all invalid flags.
        op += "## Invalid Flags:\n"
        op += self.serialize('Rx Invalid NWID', 'invalid_nwid')
        op += self.serialize('Rx Invalid Crypt', 'invalid_crypt')
        op += self.serialize('Rx Invalid Fragment', 'invalid_frag')
        op += self.serialize('Invalid Misc', 'invalid_misc')
        op += self.serialize('Missed Beacon', 'missed_beacon')

        return op.strip("\n")

class IWConfig:
    '''
    Python subprocess.getoutput wrapper around iwconfig
    '''
    def __init__(self):
        self.net_info = self.probe()

    def probe(self):
        result = subprocess.Popen('iwconfig', stdout=subprocess.PIPE)
        raw_str = result.communicate()[0].decode('utf-8')
        ret_code = result.returncode
        # create LinuxNetInfo
        net_info = LinuxNetInfo(isvalid=True if ret_code == 0 else False)
        net_info.parse(raw_str)

        return net_info
        # net_names = []

class NetworkHandler:
    def __init__(self):
        self.os = platform.system()
        if self.os == "Linux":
            self.manager = IWConfig()
        else:
            self.manager = None

    def probe(self):
        if self.manager:
            self.manager.probe()


if __name__ == "__main__":
    net_handler = NetworkHandler()
    print(net_handler.manager.net_info)
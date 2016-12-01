"""Network testing script"""
import random

#Difficulty settings.
CHALLENGE = {0: 'ee',  #very easy
             1: 'e',   #easy
             2: 'n',   #normal
             3: 'h',   #hard
             4: 'hh'}  #very hard

#The lowest and highest IPs in each network class.
IP_RANGE = {'A_LOW':  0x01000000,
            'A_HIGH': 0x7F000000,
            'B_LOW':  0x80000000,
            'B_HIGH': 0xBF000000,
            'C_LOW':  0xC0000000,
            'C_HIGH': 0xCF000000}

#Default masks for each IP address class.
DEFAULT_MASK = {'A': 0xFF000000,
                'B': 0xFFFF0000,
                'C': 0xFFFFFF00}


def tobytes(address):
    """Return a 32 bit integer address as an array of 4 bytes."""
    dbytes = []
    dbytes.append((address & 0x000000FF))
    dbytes.append((address & 0x0000FF00) >> 8)
    dbytes.append((address & 0x00FF0000) >> 16)
    dbytes.append((address & 0xFF000000) >> 24)
    return dbytes


class IpAddr(object):
    """An object that contains an IP address and all of the possible answers
    of that IP for a subnetting question (#hosts, class, mask, etc.). The
    answers are generated when an IPAddr object is created.
    """
    ip_bytes = {3: None, 2: None, 1: None, 0: None}
    net_bytes = {3: None, 2: None, 1: None, 0: None}
    host_addr = None
    net_class = None
    net_mask = None
    num_subnets = None
    num_hosts = None
    broadcast_ip = None
    def_gateway = None


    def __init__(self, answer):
        """
        Generate an IP when answer is None, or use the supplied answer to
        to create the object
        """
        if answer is None:
            self.__generate_answer()
        else:
            self.__init_answer(answer)


    def __generate_answer(self):
        """
        Generates a random IP, equally weighted among class A, B, and C.
        """
        self.__setclass(None)
        self.__setmask()
        self.__setip()
        self.__setnetwork()


    def __setclass(self, nclass):
        """Set the network class of the object.
        params: nclass = None, randomly generate the class for making a new IP.
                nclass = 1-3, the class is set to A-C respectively.
        """
        #The network class was not supplied as an argument -- generate it.
        if nclass == None:
            rand = random.randint(1, 3)
            if rand == 0:
                self.net_class = 'A'
            elif rand == 1:
                self.net_class = 'B'
            else:
                self.net_class = 'C'
        #The network is already generated and we only want to set the variable
        elif nclass == 1:
            self.net_class = 'A'
        elif nclass == 2:
            self.net_class = 'B'
        elif nclass == 3:
            self.net_class = 'C'


    def __setmask(self):
        """Set the network mask bits."""
        self.net_mask = DEFAULT_MASK[self.net_class]


    def __setip(self):
        """
        Create an IP within the network class of the object, then convert
        address into bytes and set the ip_bytes variable as would appear in
        dotted decimal format.
        """
        #Generate an IP within the appropriate range for the given net class.
        if self.net_class == 'A':
            ip_addr = random.randint(IP_RANGE['A_LOW'],
                                     IP_RANGE['A_HIGH'])
        elif self.net_class == 'B':
            ip_addr = random.randint(IP_RANGE['B_LOW'],
                                     IP_RANGE['B_HIGH'])
        else:
            ip_addr = random.randint(IP_RANGE['C_LOW'],
                                     IP_RANGE['C_HIGH'])

        #Convert the integer address into dotted decimal bytes.
        self.ip_bytes = tobytes(ip_addr)


    def __setnetwork(self):
        """Find the network address and set the net_bytes variable."""
        #Convert the 4 bytes into a 32 bit integer.
        ip_addr = ((self.ip_bytes[3] << 24) +
                   (self.ip_bytes[2] << 16) +
                   (self.ip_bytes[1] << 8) +
                   (self.ip_bytes[0]))

        #Perform bitwise AND with the network mask to find the network.
        net_addr = (ip_addr & self.net_mask)
        self.net_bytes = tobytes(net_addr)


# *** Wrapper around socket and sys modules to connect to IP
# **  Pinging ip
# *   Handle subnet addresses (borrowed bits)
# *   More defined error messages (point to segment with error)
# *   Wrapper for viewing bytes and hex (conversions)


class IPRangeException(Exception):

    def __init__(self, message):

        super().__init__(message)


class IPSegmentException(Exception):

    def __init__(self, message):

        super().__init__(message)


class IPAddress:

    def __init__(self, ip, name='IP address'):

        self.name = name
        self.segments = None

        if type(ip) is str:
            self.set(ip)
        elif type(ip) is list:
            self.segments = ip
            self.validate_segments()

    def set(self, ip):

        self.segments = ip.split('.')
        # Convert segments to int. Map returns map object so cast to list
        self.segments = list(map(int, self.segments))
        self.validate_segments()

    def set_segment(self, seg_num, num):

        if seg_num >= 0 and seg_num < len(self.segments):
            self.segments[seg_num] = num
            self.validate_segments()

    def validate_segments(self):

        if len(self.segments) != 4:
            raise IPSegmentException('IP does not have 4 segments (x.x.x.x)')

        for seg in self.segments:
            if not(seg >= 0 and seg <= 255):
                raise IPRangeException('IP segment out of range (0-255)')

    def copy(self):

        return IPAddress(self.segments)

    def __and__(self, ip):

        new_ip_str = ''
        for i in range(len(self.segments)):
            new_ip_str += str(self.segments[i] & ip.segments[i]) + '.'
        # Remove trailing '.' from IP assemble process
        return IPAddress(new_ip_str[0:len(new_ip_str)-1])

    def __str__(self):

        # Convert segments back to strings so that they can be joined
        temp = list(map(str, self.segments))
        return '.'.join(temp)

    def print(self):

        print(self.name + ':', self)

    @staticmethod
    def empty():

        return IPAddress([0, 0, 0, 0])


class SubnetAddress(IPAddress):

    def __init__(self, ip, name='Subnet address'):

        IPAddress.__init__(self, ip, name=name)


if __name__ == '__main__':

    userIn = input('IP address >>> ')
    ip = IPAddress(userIn)

    userIn = input('Subnet address >>> ')
    subnet = SubnetAddress(userIn, name='Subnet Address')

    net_add = ip & subnet
    net_add.name = 'Network address'

    broadcast_add = ip.copy()
    broadcast_add.set_segment(3, 255)
    broadcast_add.name = 'Broadcast address'

    print('\nResults\n-----------------------')
    ip.print()
    subnet.print()
    net_add.print()
    broadcast_add.print()

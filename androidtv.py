from socket import *
import shlex
import readline
from adb_shell.adb_device import *
def connectv():
    for i in range(0,250):
        so = socket(AF_INET, SOCK_DGRAM)
        s = socket(AF_INET, SOCK_STREAM)
        so.connect(("10.255.255.255", 1))
        sg = s.getsockname()[0]
        ra = sg.split(".")[3]
        target = "192.168."+ ra +"."+str(i)
        s.settimeout(0.15)
        conn = s.connect_ex((target,5555))
        print('testing: ',target,end="\r")
        if (conn == 0 ):
            return target


def tvshell():
    target = connectv()
    device = AdbDeviceTcp(target, 5555, default_transport_timeout_s=9.)
    device.connect(auth_timeout_s=0.1)
    def inc(vol):
        try:
            for i in range(1,int(vol)):
                device.shell('input keyevent 24')
        except ValueError:
            print('give a valid number.')

    def dec(vol):
        try:
            for i in range(1,int(vol)):
                device.shell('input keyevent 25')
        except ValueError:
            print('give a valid number.')
    print('you are connected to ',target)
    print('type help for instructions.')
    while True:
        cmd, *args = shlex.split(input('> '))
        if cmd=='exit':
            quit()
        elif cmd=='help':
            print('type mute to toggle mute.\ntype shutdown to shutdown.\ntype inc to increase volume.\ntype dec to decrease volume.\n')
        elif cmd=='mute':
            device.shell('input keyevent 164' )
        elif cmd =='shutdown':
            device.shell('input keyevent 26')
        elif cmd=='inc':
            vol=input('increase by how much: ')
            inc(vol)
        elif cmd=='dec':
            vol=input('decrease by how much: ')
            dec(vol)
        else:
            print('Unknow command')

tvshell()

import socket
import struct


################################################################################
# @file    UDP_XPlane.py
# @author  Luan Carlos Florencio Henriques
# @version 0.0.0.1
# @date    08.05.2021
# @brief   Master File of Graduation Thesis in Electrical Engineering, UFPB 2020
################################################################################

#XpConnect(IP where XP is running(String), XP UDP Port where is listening legacy (int), XP Main UDP PORT (int))
def xpConnect (ipXplane, listenPortXplane, udpMainPort):
    
    udpIp = [(s.connect((ipXplane, listenPortXplane)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udpIp, udpMainPort))

    return sock

def xpRead(sock):
    data, addr = sock.recvfrom(1024)
    lenData    = len(data)
    dataFormat = str(lenData)+'b'
    dataStruct = struct.unpack_from(dataFormat,data)
    
    return dataStruct

def DataProcessing(data):

    DataProcessed = data
    #data reference to be compared in control system
    header           = DataProcessed[0:5]
    #
    #label 4
    currentVertSpeed = bytesToFloat([DataProcessed[17],DataProcessed[18],DataProcessed[19],DataProcessed[20]])
    #label 17
    currentPitch     = bytesToFloat([DataProcessed[45],DataProcessed[46],DataProcessed[47],DataProcessed[48]])
    currentRoll      = bytesToFloat([DataProcessed[49],DataProcessed[50],DataProcessed[51],DataProcessed[52]])
    #
    
    currentElevator  = bytesToFloat([DataProcessed[157],DataProcessed[158],DataProcessed[159],DataProcessed[160]])
    currentAileronL  = bytesToFloat([DataProcessed[189],DataProcessed[190],DataProcessed[191],DataProcessed[192]])
    currentAileronR  = bytesToFloat([DataProcessed[193],DataProcessed[194],DataProcessed[195],DataProcessed[196]])
    #
    currentHeading   = bytesToFloat([DataProcessed[59],DataProcessed[60],DataProcessed[61],DataProcessed[62]])
    currentAltitude  = bytesToFloat([DataProcessed[89],DataProcessed[90],DataProcessed[91],DataProcessed[92]])
    currentThrottle  = bytesToFloat([DataProcessed[117],DataProcessed[118],DataProcessed[119],DataProcessed[120]])  
        
##    #Module Check
    
##    print '\nHeader:', header
    print('\n-------------- FLIGHT DATA --------------')
    print( 'Vertical Speed (feet.minute): ', currentVertSpeed)
    print('Pitch              (degrees): ', currentPitch)
    print('Roll               (degrees): ', currentRoll)
    print('Elevator           (degrees): ', currentElevator)
    print('Left Aileron       (degrees): ', currentAileronL)
    print('Right Aileron      (degrees): ', currentAileronR)
    print('Magnetic Heading   (degrees): ', currentHeading)
    print('Altitude              (feet): ', currentAltitude)
    print('Throttle           (percent): ', currentThrottle*100)
    print('-----------------------------------------')

    return currentVertSpeed, currentPitch, currentRoll, currentElevator, currentAileronL, currentAileronR, currentHeading, currentAltitude, currentThrottle


# here you will develop your control & stability system as an Autopilot,
# controlling the primary control surfaces (aileron - in the case of heading
# and roll control - and elevator -in the case of altitude and pitch control
def Control():   
    pass
    # return aileron, elevator


#XpSend (float elevator [-1,1], float ailerom [-1,1], IP where XP is running(String), XP UDP Port where the XP will receive (int))
def xpSend(elevator, aileron, rudder, ipXplane, receivePortXplane):   

    header      = struct.pack('5s', b'DATA\0')
    data_buf    = bytearray(struct.pack('iffffffff', 11, elevator, aileron, rudder, 0, 0, 0, 0, 0))
    dataToSend  = header + data_buf
    socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(dataToSend, (ipXplane, receivePortXplane))


#convert the bytearray to integer
def bytesToFloat(dataBytes):
    x = dataBytes
    return round(struct.unpack('<f', struct.pack('4b', *x))[0],4)


#XpConnect(IP where XP is running(String), XP UDP Port where is listening legacy (int), XP Main UDP PORT (int))
sock = xpConnect('192.168.0.0', 49004, 49000)

while True:
    rxData = xpRead(sock)
    DataProcessing(rxData)
    xpSend(0.5, 0.5, 0, '192.168.0.0', 49010)

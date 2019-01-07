# 07-23-18 - ESAU's DingPi Script (no this isn't chinese food, this turns your raspberry pi 3 into a midi usb host/router/midi processor by way of MidiDings!)

# Prerequisites:
# Raspberry Pi 3/3+ (other models untested but might work)
# Installed Raspbian Stretch Lite (https://www.raspberrypi.org/downloads/raspbian/)
# Installed alsa utilities (sudo apt-get install alsa-utils if connected to internet)
# Installed mididings (sudo apt-get install mididings if connected to internet)
# mididings documentation: http://dsacre.github.io/mididings/doc/start.html

# Reccomended:
# Wifi enabled for quick installation of prerequisites
# If you don't use linux much like me, enabling ssh on your pi so you can remote from another computer on your home network is pretty slick.
# Use linux utility crontab or equivalent to run this script on startup so you don't need a keyboard/monitorself. tutorial here: https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/

from mididings import *

# config is mididings' setup function
config(
    # specify alsa as backend vs Jack which we're not using
    backend='alsa',

    # in_ports and out_ports will define and set up what I consider a virtual patchbay in that we set up all the backend connections with referenced names but don't interconnect them yet.
    # in_ports is all devices sending midi out via usb cable into raspberry pi for routing.
    # the first item in each set of parenthesis is arbitrary and can be named whatever you want. Second item is like an address and is specific to what [client]:[port] values are listed when you plug your gear into Pi and run aplaymidi -l command.
    in_ports = [
        ('keystep','Arturia KeyStep 32:0'),
        ('beatstep', 'Arturia BeatStep Pro:0'),
        #('mpk', 'MPK261:0'),
    ],
    # out_ports is all devices receiving midi data via usb cable outputted from raspberry pi.
    out_ports = [
        ('CH345', 'CH345:0'),
        ('beatstep2', 'Arturia BeatStep Pro:0')
    ]
)

def add_velocity(ev):
    if ev.type == NOTEON:
        ev.velocity = 128 - ev.velocity
    return ev

# I consider this section the equivalent of virtual patch cables making connections on the virtual patchbay we declared above.
run(
    # routing channels individually from Xkey 25 key keyboard => mpc1000/mio => blofeld to enable multi-timbral playing, recording, playback,
    # also individually routing blofeld back to mpc100/mio for recording cc knob movements
    # PortSplit allows us to route individual input and output ports
    PortSplit({
        # here we duplicate keyboard midi 8 times, then filter each one to a specific channel and send to respective mio midi interface channel for multi-timbral capture into MPC1000 sequencer.
        'beatstep': [
            ChannelFilter(1) >> Output('CH345',1),
            ChannelFilter(2) >> Output('CH345',2),
            ChannelFilter(3) >> Output('CH345',3),
            ChannelFilter(4) >> Output('CH345',4),
            ChannelFilter(5) >> Output('CH345',5),
            ChannelFilter(6) >> Output('CH345',6),
            ChannelFilter(7) >> Output('CH345',7),
            ChannelFilter(8) >> Output('CH345',8),
            ChannelFilter(9) >> Output('CH345',8),
            ChannelFilter(10) >> Output('CH345',10),
            ChannelFilter(11) >> Output('CH345',11),
            ChannelFilter(12) >> Output('CH345',12),
            #Volca Fm needs a midi cc 41 msg for velocity. So we'll read the velocity from note on and generate a midi cc 41 value
            ChannelFilter(13) >> [Filter(NOTEON) % Ctrl(41, EVENT_VELOCITY) >> Output('CH345',13),Output('CH345',13)],
            ChannelFilter(14) >> Output('CH345',14),
            ChannelFilter(15) >> Output('CH345',15),
            ChannelFilter(16) >> [Filter(NOTEON) % Ctrl(41, EVENT_VELOCITY) >> Output('CH345',16),Output('CH345',16)],
            #Volca Fm needs a midi cc 41 msg for velocity
        ],
        # with mpc correctly configured for multi-timbral, incoming midi passes thru to mpc midi out which we duplicate eight times here and filter/send out via mio midi interface to the blofeld midi in
        'keystep': [
            ChannelFilter(1) >> Output('CH345',1),
            ChannelFilter(2) >> Output('CH345',2),
            ChannelFilter(3) >> Output('CH345',3),
            ChannelFilter(4) >> Output('CH345',4),
            ChannelFilter(5) >> Output('CH345',5),
            ChannelFilter(6) >> Output('CH345',6),
            ChannelFilter(7) >> Output('CH345',7),
            ChannelFilter(8) >> Output('CH345',8),
            ChannelFilter(9) >> Output('CH345',8),
            ChannelFilter(10) >> Output('CH345',10),
            ChannelFilter(11) >> Output('CH345',11),
            ChannelFilter(12) >> Output('CH345',12),
            #Volca Fm needs a midi cc 41 msg for velocity. So we'll read the velocity from note on and generate a midi cc 41 value
            ChannelFilter(13) >> [Filter(NOTEON) % Ctrl(41, EVENT_VELOCITY) >> Output('CH345',13),Output('CH345',13)],
            ChannelFilter(14) >> Output('CH345',14),
            ChannelFilter(15) >> Output('CH345',15),
            #Volca Fm needs a midi cc 41 msg for velocity. So we'll read the velocity from note on and generate a midi cc 41 value
            ChannelFilter(16) >> [Filter(NOTEON) % Ctrl(41, EVENT_VELOCITY) >> Output('CH345',16),Output('CH345',16)],
        ]
    })
)
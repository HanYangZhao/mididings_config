#!/bin/bash
sudo pkill -f python
sleep 1 
sudo python /home/pi/mididings_config/midi.py &

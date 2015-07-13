#!/bin/bash
# This script is made by Kendemu
#https://github.com/demulab/move_arm_mini/tree/603b20622aba2e2b1734e659a84f6710987e240c

do_version_check() {

   [ "$1" == "$2" ] && return 10

   ver1front=`echo $1 | cut -d "." -f -1`
   ver1back=`echo $1 | cut -d "." -f 2-`

   ver2front=`echo $2 | cut -d "." -f -1`
   ver2back=`echo $2 | cut -d "." -f 2-`

   if [ "$ver1front" != "$1" ] || [ "$ver2front" != "$2" ]; then
       [ "$ver1front" -gt "$ver2front" ] && return 11
       [ "$ver1front" -lt "$ver2front" ] && return 9

       [ "$ver1front" == "$1" ] || [ -z "$ver1back" ] && ver1back=0
       [ "$ver2front" == "$2" ] || [ -z "$ver2back" ] && ver2back=0
       do_version_check "$ver1back" "$ver2back"
       return $?
   else
           [ "$1" -gt "$2" ] && return 11 || return 9
   fi
}    

val = `do_version_check $(uname -r| sed 's/[[:alpha:]|(|[:space:]]//g' | awk -F- '{print $1}') 3.11.0`
if [$val -eq 11]; then
    echo "loading module ftdi_sio"
    sudo modprobe ftdi_sio vendor=0x1115 product=0x0008
    echo "writing device information in linux configuration file"
    sudo chmod 666 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
    sudo echo "1115 0008" >> /sys/bus/usb-serial/drivers/ftdi_sio/new_id
    echo "show if ttyUSB is recognized"
    ls -al /dev/ttyUSB*
    echo "adding current user to dialout group"
    sudo adduser $(whoami) dialout
    echo "changing permission of ttyUSB0 device"
    sudo chmod 666 /dev/ttyUSB0
    echo "ftdi_sio" >> /etc/modules
    sudo sed -e "$i echo '0411 00b3' > /sys/bus/usb-serial/drivers/ftdi_sio/new_id" /etc/rc.local
else
    echo "no need to change kernel module configuration. Your kernel version is lower than 3.12."
fi
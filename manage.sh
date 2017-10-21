#!/usr/bin/env bash
# this is a test script to ping a network and check if the server is online

filenamepre443="$1_443"
filenamepre80="$1_80"

dt=$(date +"%d_%m_%Y_%H:%M:%S")

filename443+="$dt-$filenamepre443"
filename80+="$dt-$filenamepre80"

csv443="$filename443.csv"
csv80="$filename80.csv"

tshark -i virbr0 -w $filename443.pcap -f "tcp port 443" -a duration:60 -T fields -e frame.number -e frame.time -e ip.src -e ip.dst -e tcp.port -e frame.len  -E header=y -E separator=, -E quote=d -E occurrence=f> $csv443 |
tshark -i virbr0 -w $filename80.pcap -f "tcp port 80" -a duration:60 -T fields -e frame.number -e frame.time -e ip.src -e ip.dst -e tcp.port -e frame.len  -E header=y -E separator=, -E quote=d -E occurrence=f> $csv80


#./delete.sh


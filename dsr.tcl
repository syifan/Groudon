#=============================================================================
#     FileName: dsr.tcl
#         Desc: Simulate the GroundWave propagation
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-04-02 11:16:14
#      History:
#=============================================================================
# wrls1.tcl
# A 3-node example for ad-hoc simulation with DSDV

# Define options
set val(chan)           Channel/WirelessChannel    ;# channel type
# set propagation model
set opt(prop) 			Propagation/Shadowing2	   ;
set val(netif)          Phy/WirelessPhy            ;# network interface type
set val(mac)            Mac/802_11                 ;# MAC type
#set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
set val(ifq)            CMUPriQueue    ;# interface queue type
set val(ll)             LL                         ;# link layer type
set val(ant)            Antenna/OmniAntenna        ;# antenna model
set val(ifqlen)         50                         ;# max packet in ifq
set val(nn)             2                          ;# number of mobilenodes
set val(rp)             DSDV                        ;# routing protocol
set val(x)              [lindex $argv 3]   			   ;# X dimension of topography
set val(y)              400   			   ;# Y dimension of topography  
set val(stop)		    150			   ;# time of simulation end
#set testscript [open testscript.sh r]

# parameters for GRWAVE
set HTT "HTT 679 \n" ;# Effective height of the transmitter (m)
set HRR "HRR 1491\n" ;#Effective height of the Receiver (m)
set IPOLRN "IPOLRN 1\n" ;# Polarization (1 for vertical and 2 for horizontal)
set FREQ "FREQ 6\n" ;#Frequency in MHz
set SIGMA "SIGMA 0.01\n" ;#Condutivity (S/m) of the terrain
set EPSLON "EPSLON 30\n" ;#Permitivity of the terrain
set dmin "dmin 1\n" ;#Distance (km) where the field needs to be calculated
set dmax "dmax 200\n" 
set dstep "dstep 5\n"
set GO "GO"
# create some data
# pick a filename - if you don't include a path,
#  it will be saved in the current directory
 #set filename "inp"
# open the filename for writing
# set fileId [open $filename "w"]
# send the data to the file -
#  failure to add '-nonewline' will result in an extra newline
# at the end of the file
#puts $fileId \
${HTT}${HRR}${IPOLRN}${FREQ}${SIGMA}${EPSLON}${dmin}${dmax}${dstep}${GO}
# close the file, ensuring the data is written out before you continue
#  with processing.
#close $fileId
# running grwave and grab the output

# runing script to get the output result
#set result [exec grabinfo.sh ]


# parameters for shadowing2
# Path loss exponent
Propagation/Shadowing2 set pathlossExp_ [lindex $argv 0]
# shadowing deviation
Propagation/Shadowing2 set std_db_ 3 	
# reference distance
Propagation/Shadowing2 set dist0_ 1.0	 
Propagation/Shadowing2 set validity_ 0.9
Propagation/Shadowing2 set seed_ 1		
# rx threshold
Phy/WirelessPhy set RXThresh_ 1.69063e-96
Phy/WirelessPhy set CSThresh_ 3e-9
# frequency
Phy/WirelessPhy set freq_ [lindex $argv 2]
Phy/WirelessPhy set Pt_ 100W
Phy/WirelessPhy set bandwidth_ [lindex $argv 1]
#Mac/802_11 set dataRate_ [lindex $argv 1]
#Mac/802_11 set bandwidth_ [lindex $argv 1]

# transmit antenna gain
Antenna/OmniAntenna set Gt_ 3.0
# receive antenna gain
Antenna/OmniAntenna set Gr_ 3.0
# system loss
Phy/WirelessPhy set L_ 1.0




set ns		  [new Simulator]
set tracefd       [open simple.tr w]
set windowVsTime2 [open win.tr w] 
set namtrace      [open simwrls.nam w]    

$ns trace-all $tracefd
$ns namtrace-all-wireless $namtrace $val(x) $val(y)

# set up topography object
set topo       [new Topography]

$topo load_flatgrid $val(x) $val(y)

create-god $val(nn)

#
#  Create nn mobilenodes [$val(nn)] and attach them to the channel. 
#

# configure the nodes
        $ns node-config -adhocRouting $val(rp) \
			 -llType $val(ll) \
			 -macType $val(mac) \
			 -ifqType $val(ifq) \
			 -ifqLen $val(ifqlen) \
			 -antType $val(ant) \
			 -propType $opt(prop) \
			 -phyType $val(netif) \
			 -channelType $val(chan) \
			 -topoInstance $topo \
			 -agentTrace ON \
			 -routerTrace ON \
			 -macTrace OFF \
			 -movementTrace ON
			 
	for {set i 0} {$i < $val(nn) } { incr i } {
		set node_($i) [$ns node]	
	}

# Provide initial location of mobilenodes
$node_(0) set X_ 0.0
$node_(0) set Y_ 0.0
$node_(0) set Z_ 0.0

#$node_(1) set X_ 490.0
$node_(1) set X_ [lindex $argv 3]
$node_(1) set Y_ 0.0
#$node_(1) set Y_ 285.0
$node_(1) set Z_ 0.0
#$node_(1) set Z_ 0.0

#$node_(2) set X_ 150.0
#$node_(2) set Y_ 240.0
#$node_(2) set Z_ 0.0

# Generation of movements
#$ns at 10.0 "$node_(0) setdest 250.0 250.0 3.0"
#$ns at 15.0 "$node_(1) setdest 45.0 285.0 5.0"
#$ns at 110.0 "$node_(0) setdest 480.0 300.0 5.0" 

# Set a TCP connection between node_(0) and node_(1)
set tcp [new Agent/TCP/Newreno]
$tcp set class_ 2
set sink [new Agent/TCPSink]
$ns attach-agent $node_(0) $tcp
$ns attach-agent $node_(1) $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 0.0 "$ftp start" 

# Printing the window size
proc plotWindow {tcpSource file} {
global ns
set time 0.01
set now [$ns now]
set cwnd [$tcpSource set cwnd_]
puts $file "$now $cwnd"
$ns at [expr $now+$time] "plotWindow $tcpSource $file" }
$ns at 10.1 "plotWindow $tcp $windowVsTime2"  

# Define node initial position in nam
for {set i 0} {$i < $val(nn)} { incr i } {
# 30 defines the node size for nam
$ns initial_node_pos $node_($i) 30
}

# Telling nodes when the simulation ends
for {set i 0} {$i < $val(nn) } { incr i } {
    $ns at $val(stop) "$node_($i) reset";
}

#set result [exec testscript.sh ]
#puts $result
# ending nam and the simulation 
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"
$ns at 150.01 "puts \"end simulation\" ; $ns halt"
    

proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    close $tracefd
    close $namtrace
}

$ns run


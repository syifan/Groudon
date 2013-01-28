#=============================================================================
#     FileName: mea.pl
#         Desc: Compute throughput
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-03-19 15:33:06
#      History:
#=============================================================================
#!/usr/bin/perl

#trace file name
$infile = $ARGV[0];
#time interval(s)
$granularity = 10;

#save the first time
$init=0;
$start = 0;

#hashtable to store send packet number
%pre_send_packet;

#hashtable to store delay info
%throughput_hash_table;

#defin type to consider
$type_to_consider = "tcp";
$layer_to_consider = "AGT";
$send = "s";
$rec = "r";

open(DATA, "<$infile")
    || die "cannot open $infile $!";

while(<DATA>){
    @x = split(' ');
    $time = $x[1];
    $target = $x[2];
    $packet_layer = $x[3];
    $send_or_rec = $x[0];
    $packet_num = $x[5];
    $packet_type = $x[6];
    $packet_size = $x[7];
    if(($packet_type =~/^$type_to_consider$/i) 
        && ($send_or_rec =~/^$send$/i) 
        && ($packet_layer =~/^$layer_to_consider$/i)){
        $send_packet = $target.":".$time;
        $pre_send_packet{$packet_num}= $send_packet;
    }


    if(($packet_type =~/^$type_to_consider$/i) 
        && ($send_or_rec =~/^$rec$/i)
        && ($packet_layer eq $layer_to_consider)){
        while(($key,$value) = each(%pre_send_packet)){

            #ignore node send packet to itself
            if($key == $packet_num && ($pre_target ne $target)){
                ($pre_target,$pre_time) = split(":",$value);
                if($init == 0){
                    $start = $pre_time;
                    $init = 1
                }
                #change it from byte to bits
                $throughput = $packet_size * 8;
                $throughput_hash_table{$time} = $throughput;
                delete($pre_send_packet{$key});
            }
        }
    }
}

#save the end time
$endtime = $time;
$end = int($endtime /$granularity);

#create a array based on time interval
my @throughput_array = (0) x ($end+1);
my @throughput_array_time = ($start) x ($end+1);
while(($key,$value) = each(%throughput_hash_table)){
        $key_num = int($key/$granularity);
        $throughput_array[$key_num] += $value;
        $i = $end;
        while($i <= $end && $i >= $key_num){
            if($throughput_array_time[$i] < $key){
                $throughput_array_time[$i] = $key;
            }
            $i--;
        }
}

#cal the throughput based on time interval
$i=0;
print "[";
while($i<=$end){
    $j = $granularity * $i;
    $k = $j + $granularity;
    $total_throughput += $throughput_array[$i];
    if($throughput_array_time[$i] ne $start){
        $avg = $total_throughput / ($throughput_array_time[$i] - $start);
        $avg = $avg / 1024;
    }
    else{
        $avg = $total_throughput;
    }
    $avg=sprintf "%.4f",$avg;
    if ($i != $end){
    print "$avg,";
}else{
    print "$avg";
}
    $i++;
}
#print "$avg\n";
print "]";
#finished,...
close DATA;
exit(0)

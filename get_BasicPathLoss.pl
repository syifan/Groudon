#!/usr/bin/perl
#=============================================================================
#     FileName: ana.pl
#         Desc: 
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-02-13 09:32:59
#      History:
#=============================================================================

# gr output
$infile = $ARGV[0];
open(DATA,"<$infile") 
    || die "cannot open it";

while(<DATA>){
    @x = split(' ');
#    print $x[0];
#    print "\n";
#print $x[1];
#print "\n";
if (($x[0] =~ /^[0-9]/) || $x[0] =~/^[-]/){
    #  print $x[0];
    #print "\n";
}

if (($x[1] =~ /^[0-9]/) || $x[1] =~/^[-]/){
#    print $x[1];
#    print "\n";
}
if (($x[2] =~ /^[0-9]/) || $x[2] =~/^[-]/){
print $x[2];
print "\n";
}
#    print $x[2];
#    print "\n";
#    print $x[3];


}

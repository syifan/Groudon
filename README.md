Groudon
====
![Mou icon](http://www.animalhi.com/thumbnails/detail/20121026/pokemon%20black%20background%20groudon%201680x1050%20wallpaper_www.animalhi.com_60.jpg)


## Overview
**Groudon**, a ground wave online simulation system (multinodes version)


## How to deploy (Server)
###check out the code
Check out the code by using git command.[^1]

	git clone git@github.com:quake0day/Groudon.git

[^1]: The following instruction assume that you checkout this repo to your home directory (~/Groudon).

To deploy this online simulation system, we need compile serveral componements. Currently, there are two main componments that need to be compiled.

###Grwave
We are using International Telecommunication Union (ITU)-R GRWAVE.
* A MS-DOS based software (written in *Fortran 77*).
* Used by ITU to obtain the graphics showed at Rec. ITU-R P.368-9.
* Allows calculating the field over a path with one value for conductivity.

**GRWAVE** is publicly available online: [Official Website](http://www.itu.int/oth/R0A0400000F/en "Grwave")

####usage
Firstly, we need to compile grwave by using **GFortran** [Official Website](http://gcc.gnu.org/wiki/GFortran "GFortran")

	cd ~/Groudon/grwave/
	gfortran grwave.for -o gr
Then we need copy the binary file `gr` to Groudon's root directory, you can type something like

	cp ~/Groudon/grwave/gr ~/Groudon/gr

###NS2
Firstly, you need make sure that you have a environment that is able to compile original ns2 source code into executable program (it can generate `ns` after type `make`)

After that, you need copy [`Shadowing2.cc`][sw2c] and [`Shadowing2.h`][sw2h] into `*/ns-2.*/mobile/`

[sw2c]: https://github.com/quake0day/grns2/blob/master/aur-ns-allinone/src/ns-allinone-2.34/ns-2.34/mobile/Shadowing2.cc  "download"
[sw2h]: https://github.com/quake0day/grns2/blob/master/aur-ns-allinone/src/ns-allinone-2.34/ns-2.34/mobile/Shadowing2.h  "download"

Since we want to simulate groundwave propagation, the default max propagation delay defined in NS2 **cannot be directly used** and need to be changed. (Otherwise if the propagation delay is more than 2us, and sender do not receive ACK, it will re-send the packet and give us a false result)

We need to change `*/ns-2.x/mac/mac802_11.h`.

	#define DSSS_MaxPropagationDelay 0.000002 // 2us XXXX
to a bigger value. Like:
	
	#define DSSS_MaxPropagationDelay 0.02

Then we can recompiled the whole program and copy the generated `ns` to `~/Groudon/`

Like:

	cp */ns-2.*/ns ~/Groudon/ns


###Extra Python library
Note:The library name are based on archlinux (AUR) it may have a different name in Ubuntu and other linux distro

1. mysql-python
2. python2-simplejson
3. python2-imaging (PIL) 
4. python2-numpy
5. python2-scipy

###Perl
You need to install perl to process simulation result

## More..


## Team Member
Si Chen

Yifan Sun
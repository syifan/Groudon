Groudon
====
![Mou icon](http://www.animalhi.com/thumbnails/detail/20121026/pokemon%20black%20background%20groudon%201680x1050%20wallpaper_www.animalhi.com_60.jpg)


## Overview
**Groudon**, a ground wave online simulation system (multinodes version)


## How to deploy 
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

After that, you need copy `Shadowing2.cc` and `Shadowing2.h` into `*/ns-2.*/mobile/`

Then recompiled the whole program and copy the generated `ns` to `~/Groudon/`

Like:

	cp */ns-2.*/ns ~/Groudon/ns


## More..


## Team Member
Si Chen

Yifan Sun
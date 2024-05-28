
#
#
#

.phoney: all dbg

all:
	python printer.py "R:\\dev\\1060-EVKB\\boards\\evkbmimxrt1060\\demo_apps\\shell\\armgcc\\CMakeLists.txt"
	# python printer.py test.cmake

# python printer.py "R:\dev\1060-EVKB\boards\evkbmimxrt1060\demo_apps\shell\armgcc\CMakeLists.txt"
dbg:
	python printer.py "R:\\dev\\1060-EVKB\\boards\\evkbmimxrt1060\\demo_apps\\shell\\armgcc\\CMakeLists.txt"


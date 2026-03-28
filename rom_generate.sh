#!/bin/bash

mips-linux-gnu-objcopy -O binary --gap-fill=0x00 SLES_513.56 SLES_513.56.rom

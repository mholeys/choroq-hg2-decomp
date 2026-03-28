#! /usr/bin/env python3

# Start from https://github.com/ethteck/kh1/blob/main/configure.py as example

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Set, Union

import ninja_syntax
import splat
import splat.scripts.split as split
from splat.segtypes.linker_entry import LinkerEntry

ROOT = Path(__file__).parent.resolve()
TOOLS_DIR = ROOT / "tools"

VERSION = "eur"
BASENAME = "SLES_512.56"
YAML_FILE = f"config/hg2.{VERSION}.yaml"

LD_PATH = f"{BASENAME}.ld"
ELF_PATH = f"build/{VERSION}/{BASENAME}"
MAP_PATH = f"build/{VERSION}/{BASENAME}.map"
PRE_ELF_PATH = f"build/{VERSION}/{BASENAME}.elf"

COMMON_INCLUDES = "-Iinclude -isystem include/sdk/ee -isystem include/gcc"

# TODO: workout what gcc version game/libs use
GAME_CC_DIR = f"{TOOLS_DIR}/cc/ee-gcc-game"
LIB_CC_DIR = f"{TOOLS_DIR}/cc/ee-gcc-lib/bin"
# TODO: workout gcc flags to start with
COMMON_COMPILE_FLAGS = "-O2 -G0 $g"

GAME_GCC_CMD = f"{GAME_CC_DIR}/bin/ee-gcc -c -B {GAME_CC_DIR}/bin/ee- {COMMON_INCLUDES} {COMMON_COMPILE_FLAGS} $in"

# TODO: what does masps2 do?
GAME_COMPILE_CMD = f"{GAME_GCC_CMD} -S -o - | {TOOLS_DIR}/masps2.py | {GAME_CC_DIR}/ee/bin/as {COMMON_COMPILE_FLAGS} -EL -mabi=eabi"

# TODO: change 991111 to whatever is needed
LIB_COMPILE_CMD = f"{LIB_CC_DIR}/ee-gcc -c -isystem include/gcc-991111 {COMMON_INCLUDES} {COMMON_COMPILE_FLAGS}"

# TODO: what does this do
NO_G_FILES = [
    "xblade.c",
    "gumi.c",
]

def clean():
    if os.path.exists(".splache"):
        os.remove(".splache")
    shutil.rmtree("asm", ignore_errors=True)
    shutil.rmtree("assets", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)

# TODO: update gcc version as needed
def write_permuter_settings():
    with open("permuter_settings.toml", "w") as f:
        f.write(
            f"""compiler_command = "{GAME_COMPILE_CMD} -D__GNUC__"
assembler_command = "mips-linux-gnu-as -march=r5900 -mabi=eabi -Iinclude"
compiler_type = "gcc"

[preserve_macros]

[decompme.compilers]
"tools/build/cc/gcc/gcc" = "ee-gcc2.96"
"""
        )
        
        















if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure the project")
    parser.add_argument(
        "-v",
        "--version",
        help="Game version to configure for",
        choices=["jp", "usa", "eur", "kor"],
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="Clean extraction and build artifacts",
        action="store_true",
    )
    args = parser.parse_args()

    if args.version:
        VERSION = args.version
    else:
        VERSION = "eur"
        
    # TODO: populate
    BASENAME = {
        "jp": "",
        "usa": "",
        "eur": "SLES_513.56",
        "kor": "",
    }[VERSION]

    LD_PATH = f"{BASENAME}.ld"
    ELF_PATH = f"build/{VERSION}/{BASENAME}"
    MAP_PATH = f"build/{VERSION}/{BASENAME}.map"
    PRE_ELF_PATH = f"build/{VERSION}/{BASENAME}.elf"
    
     if args.clean:
        clean()

    EXTENDEDNAME = {
        "jp": "Choro Q HG 2 チョロQ HG 2",
        "usa": "Everywhere Road Trip",
        "eur": "Road trip Adventure",
        "kor": "쵸로Q HG 2",
    }[VERSION]
    
     print(
        f"Generating build configuration for {EXTENDEDNAME} edition ({BASENAME})"
    )
        
    YAML_FILE = f"config/hg2.{VERSION}.yaml"
    
    split.main([YAML_FILE], modes="all", verbose=False)
    
    linker_entries = split.linker_writer.entries

    build_stuff(linker_entries)

    write_permuter_settings()
    
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc/4.0/)

# Introduction
This material was originally developed as part of an assignment of the Operating systems for embedded systems course delivered at Politecnico di Torino by Prof. Stefano Di Carlo.

Basic repository aiming at testing both FreeRTOS and cache-timing attacks on AES, on Raspberry Pi Pico board.
Largely inspired from my [lab about cache-timing attacks on Raspberry Pi 4](https://github.com/marius-hel/aes-cache-timing-attack-pi4) which is entirely based on [*Cache-timing attacks on AES* by Daniel J. Bernstein](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf).

# Prerequisite
Hardware:
- Raspberry Pi Pico board
- Micro-USB cable

Software:
- Install CMake and the Pico SDK toolchain. Please follow the instructions of "Chapter 2. The SDK" from this document: [Getting started with Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)

# Setup
Execute *setup.sh* to: setup the project, pull the FreeRTOS kernel and make a first build.
`./setup.sh`

# Build
If changes are made to the code, go to *build* folder and type <br>
`make`<br>
or<br>
`make -j4`<br>
for faster build.

# Deploy
- Unplug the Micro-USB cable
- Press the *BOOTSEL* button on the Raspberry Pi Pico board
- Plug the Micro-USB cable
- Release the *BOOTSEL* button on the Raspberry Pi Pico board
- Copy *rp2040_freertos_aes.uf2* (in *build* folder) to the Raspberry Pi Pico board (actually behaving as a mass storage). <br>
On Ubuntu: `cp rp2040_freertos_aes.uf2 /media/*user*/RPI-RP2/`

# Cache-timing attack: lab procedure

## Step 1: study
In the root folder, run:<br>
`make study`<br>

## Step 2: attack
Comment out
```
#define ZERO_KEY_MODE
```
in *main.c*:
```
[...]
#define LED_PIN 25
#define ON 1
#define OFF 0
//#define ZERO_KEY_MODE
[...]
```
Go to *build* folder and run:<br>
`make`<br>

Deploy the compiled code on the Raspberry Pi Pico by following the procedure described in [deploy](#Deploy) part.

Then go back to the root folder and run:<br>
`make attack`<br>

## Step 3: analysis

You can eventually run the following sequence of commands:<br>
`make correlate`<br>
`make show_known_bits`<br>
`make show_private_key`<br>
You should now be able to compare what is found by the attack procedure to the real private key.

# Example of results

After getting samples for study and attack phase, taking ~1 hour (4096000 samples) each, I got the following results:
```
[...]
$ make show_private_key
00001111 00011110 00101101 00111100 01001011 01011010 01101001 01111000 10000111 10010110 10100101 10110100 11000011 11010010 11100001 11110000 
$ make show_known_bits 
[...]
11 bits are supposed known with a probability >= 1.0
From left to right: k[0] ... k[15] 
________ ________ 0_1_____ ________ ________ ________ 0_1_____ 01______ ________ ________ 1_______ 10______ ________ ________ 1_1_____ ________ 
```
We notice that all the "supposed known" bits seem right. This is quite satisfying for a total of two hours of attack. However, this is not enough at all if we want to brute force the key. All in all, this is a good start for a more advanced and longer cache-collision timing attack on Raspberry Pi Pico.
import argparse
import serial
from datetime import datetime
import os
import numpy as np

LOG_STEP = 200
SAVE_STEP = 100000

t = [[0 for _ in range(256)] for _ in range(16)]
tsq = [[0 for _ in range(256)] for _ in range(16)]
tnum = [[0 for _ in range(256)] for _ in range(16)]

def save():
    global t
    global tsq
    global tnum

    u = [[0 for _ in range(256)] for _ in range(16)]
    udev = [[0 for _ in range(256)] for _ in range(16)]

    for j in range(16):
        for b in range(256):
            u[j][b] = t[j][b] / tnum[j][b]
            udev[j][b] = tsq[j][b] / tnum[j][b]
            udev[j][b] -= u[j][b] * u[j][b]
            udev[j][b] = np.sqrt(udev[j][b])
    
    uavg = sum([sum(u[j]) for j in range(16)])/(16*256)

    with open(args.outputfile, "w") as file:
        for j in range(16):
            for b in range(256):
                file.write(f"{j:2} {b:3} {tnum[j][b]} {u[j][b]:.4f} {udev[j][b]:.4f} {u[j][b] - uavg:.4f} {udev[j][b] / np.sqrt(tnum[j][b]):.4f}\n")

def main(args):
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

    global t
    global tsq
    global tnum

    then = datetime.now()
    failure_counter=0

    print(f"Attack - {args.n} samples")

    for i_sample in range(args.n):
        #plaintext = np.random.randint(low=0, high=256, size=16, dtype=np.uint8)
        plaintext = os.urandom(16)
        ser.write(plaintext)
        
        read_buffer = ser.readline()
        try:
            [in_str, cycles_str] = read_buffer[:-2].decode().split(';')
        except:
            #print("Error:", read_buffer[:-2].decode())
            failure_counter += 1
            continue
        try:
            cycles_int = int(cycles_str)
        except:
            failure_counter += 1
            continue
        if (cycles_int > 0) and (len(in_str) == 32):
            for j in range(16):
                try:
                    b = int(in_str[2*j: 2*j + 2], 16)
                    t[j][b] += cycles_int
                    tsq[j][b] += cycles_int * cycles_int
                    tnum[j][b] += 1
                except:
                    print(f"Error: cannot convert {in_str[2*j: 2*j + 2]} to int")
                    failure_counter += 1
                    continue
        if i_sample % LOG_STEP == 0:
            now = datetime.now()
            eta = ((args.n - i_sample)/LOG_STEP)*(now - then)
            print(f"ETA:{eta} {i_sample/args.n*100:.4f}%", end='\r')
            then = now

        if ((i_sample+1) % SAVE_STEP == 0) and i_sample > 0:
            save()

    print("Done" + ' ' * 30)

    ser.close()

    print(f"Sample loss: {failure_counter/args.n*100:.4f}%")
    overall_min = min([min(tnum[j]) for j in range(16)])
    overall_max = max([max(tnum[j]) for j in range(16)])
    print(f"Overall min tnum: {overall_min}")
    print(f"Overall max tnum: {overall_max}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('n', type=int)
    parser.add_argument('outputfile')
    args = parser.parse_args()
    main(args)
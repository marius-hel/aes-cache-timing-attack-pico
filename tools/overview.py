""" Simple script to plot how bytes affect timings """
import argparse
import matplotlib.pyplot as plt

def main(arg):
    """ Main function """
    plaintextbyte = list(range(256))
    timings = [[0 for _ in range(256)] for _ in range(16)]

    with open(arg.file, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            splitted = line.split()
            timings[int(splitted[0])][int(splitted[1])] = float(splitted[5])

    fig, axes = plt.subplots(4, 4, figsize=(12, 8), sharex=True, sharey=True)
    fig.suptitle(f"Average cycles above global average", fontsize=15)

    for i in range(4):
        for j in range(4):
            k = 4*i + j
            axes[i,j].scatter(plaintextbyte, timings[k], marker='.')
            axes[i,j].set_title(f"abv_avg=f(n[{str(k)}])")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot average cycles above global average <file>')
    parser.add_argument('file')
    args = parser.parse_args()
    main(args)

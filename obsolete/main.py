from tools import *


def main():
    metadata, data = readGSF('data/data0.gsf')
    writeMAT(metadata, data, 'data0.mat')
    writeOBJ(metadata, data, 'data0_raw.obj')

    metadata, data = readGSF('data/data1.gsf')
    writeMAT(metadata, data, 'data1.mat')
    writeOBJ(metadata, data, 'data1_raw.obj')


if __name__ == '__main__':
    main()

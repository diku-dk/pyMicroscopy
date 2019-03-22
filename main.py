from tools import *


def main():
    metadata, data = readGSF('data/data0.gsf')
    writeOBJ(metadata, data, 'data0_raw.obj')
    writeMAT(metadata, data, 'data0.mat')

    metadata, data = readGSF('data/data1.gsf')
    writeOBJ(metadata, data, 'data1_raw.obj')
    writeMAT(metadata, data, 'data1.mat')


if __name__ == '__main__':
    main()

import sys
import getopt
import numpy as np


def read_gsf(file_name):
    '''Read a Gwyddion Simple Field 1.0 file format
    http://gwyddion.net/documentation/user-guide-en/gsf.html

    Args:
        file_name (string): the name of the output (any extension will be replaced)
    Returns:
        metadata (dict): additional metadata to be included in the file
        data (2darray): an arbitrary sized 2D array of arbitrary numeric type
    '''
    print('readGSF(', file_name, ')')

    if file_name.rpartition('.')[1] == '.':
        file_name = file_name[0:file_name.rfind('.')]

    gsfFile = open(file_name + '.gsf', 'rb')

    metadata = {}

    # check if header is OK
    if not (gsfFile.readline().decode('UTF-8') == 'Gwyddion Simple Field 1.0\n'):
        gsfFile.close()
        raise ValueError('File has wrong header')

    term = b'00'
    # read metadata header
    while term != b'\x00':
        line_string = gsfFile.readline().decode('UTF-8')
        metadata[line_string.rpartition(' = ')[0]] = line_string.rpartition('=')[2]
        term = gsfFile.read(1)
        gsfFile.seek(-1, 1)

    gsfFile.read(4 - gsfFile.tell() % 4)

    # fix known metadata types from .gsf file specs
    # first the mandatory ones...
    metadata['XRes'] = np.int(metadata['XRes'])
    metadata['YRes'] = np.int(metadata['YRes'])

    # now check for the optional ones
    if 'XReal' in metadata:
        metadata['XReal'] = np.float(metadata['XReal'])

    if 'YReal' in metadata:
        metadata['YReal'] = np.float(metadata['YReal'])

    if 'XOffset' in metadata:
        metadata['XOffset'] = np.float(metadata['XOffset'])

    if 'YOffset' in metadata:
        metadata['YOffset'] = np.float(metadata['YOffset'])

    data = np.frombuffer(gsfFile.read(), dtype='float32').reshape(metadata['YRes'], metadata['XRes'])

    gsfFile.close()
    return metadata, data


def write_mat(metadata, data, filename):
    import numpy as np
    import scipy.io
    print('write_mat:', metadata, data.shape)
    xdim = metadata['XRes']
    ydim = metadata['YRes']
    xsize = metadata['XReal']
    ysize = metadata['YReal']
    z_max = np.max(data)
    z_min = np.min(data)
    zsize = z_max - z_min
    scipy.io.savemat(filename, dict(xsize=xsize, ysize=ysize, zsize=zsize, height=data))


def main(argv):
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('gsf2mat.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('gsf2mat.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file)
    print('Output file is "', output_file)

    if input_file.split(".")[-1] != "gsf":
        print('Input file was not a gsf-file')
        sys.exit(2)

    if output_file.split(".")[-1] != "mat":
        print('Output file was not a mat-file')
        sys.exit(2)

    metadata, data = read_gsf(input_file)
    write_mat(metadata, data, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])


import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import REESMesh.factory as FACTORY
import REESMesh.mesh as MESH


def plotGSF(metadata, data):
    """
    Gwyddion Simple Field 1.0 file format data structures

    Args:
        metadata (dict): additional metadata to be included in the file
        data (2darray): an arbitrary sized 2D array of arbitrary numeric type
    """
    print(metadata)
    print(data.shape)
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    xdim = metadata['XRes']
    ydim = metadata['YRes']
    xsize = metadata['XReal']
    ysize = metadata['YReal']
    dx = xsize / (xdim-1)
    dy = ysize / (ydim-1)

    X = np.arange(xdim)*(dx*1000000)
    Y = np.arange(ydim)*(dy*1000000)
    X, Y = np.meshgrid(X, Y)
    Z = data*1000000
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_title(metadata['Title'])
    ax.set_xlabel('mu m')
    ax.set_ylabel('mu m')
    ax.set_zlabel('mu m')
    plt.show()


def writeGSF(data, file_name, metadata={}):
    '''Write a 2D array to a Gwyddion Simple Field 1.0 file format
    http://gwyddion.net/documentation/user-guide-en/gsf.html

    Args:
        file_name (string): the name of the output (any extension will be replaced)
        data (2darray): an arbitrary sized 2D array of arbitrary numeric type
        metadata (dict): additional metadata to be included in the file

    Returns:
        nothing
    '''

    XRes = data.shape[0]
    YRes = data.shape[1]

    data = data.astype('float32')

    if file_name.rpartition('.')[1] == '.':
        file_name = file_name[0:file_name.rfind('.')]

    gsfFile = open(file_name + '.gsf', 'wb')

    s = ''
    s += 'Gwyddion Simple Field 1.0' + '\n'
    s += 'XRes = {0:d}'.format(XRes) + '\n'
    s += 'YRes = {0:d}'.format(YRes) + '\n'

    for i in metadata.keys():
        try:
            s += i + ' = ' + '{0:G}'.format(metadata[i]) + '\n'
        except:
            s += i + ' = ' + str(metadata[i]) + '\n'

    gsfFile.write(bytes(s, 'UTF-8'))

    gsfFile.write(b'\x00' * (4 - len(s) % 4))

    gsfFile.write(data.tobytes(None))

    gsfFile.close()


def readGSF(file_name):
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


def writeMAT(metadata, data, filename):
    import numpy as np
    import scipy.io
    print('writeMAT:', metadata, data.shape)
    xdim = metadata['XRes']
    ydim = metadata['YRes']
    xsize = metadata['XReal']
    ysize = metadata['YReal']
    z_max = np.max(data)
    z_min = np.min(data)
    zsize = z_max - z_min
    scipy.io.savemat(filename, dict(xsize=xsize, ysize=ysize, zsize=zsize, height=data))


def writeOBJ(metadata, data, filename, xstep=1, ystep=1):
    """

    Args:
        metadata (dict): additional metadata to be included in the file
        data (2darray): an arbitrary sized 2D array of arbitrary numeric type
        filename: The filename of the that is to be written
    """
    print('writeOBJ:', metadata, data.shape)

    xdim = metadata['XRes']
    ydim = metadata['YRes']

    xsize = metadata['XReal']
    ysize = metadata['YReal']

    dx = xsize / (xdim-1)
    dy = ysize / (ydim-1)

    mesh = FACTORY.make_height_field(xdim, ydim, dx, dy, data, xstep, ystep)

    # Get all coordinates to be in units of micrometers
    MESH.scale(mesh, 1000000, 1000000, 1000000)

    MESH.save_obj(mesh, filename)



#!/usr/bin/env python

import os, subprocess, tempfile, sys

MATLAB_FOLDER = '%s/matlab' % os.path.realpath(os.path.dirname(__file__))

def exec_matlab_server(matlab_binary, port=4000):
    log_directory = tempfile.mkdtemp()
    matlab_args = [
        matlab_binary,
        '-nodesktop',  '-nosplash', '-nodisplay',
        '-r', 'cd {};webserver({});exit'.format(MATLAB_FOLDER, port),
        '-logfile', os.path.join(log_directory, 'log.txt')]
    print matlab_args
    os.execv(matlab_args[0], matlab_args)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run MATLAB server.')
    parser.add_argument('-p', '--port', type=int, default=4000)
    parser.add_argument('--binary', default=None)
    args = parser.parse_args()

    if args.binary is None:
        # Try to find MATLAB binary.
        import glob
        matches = sorted(glob.glob('/Applications/MATLAB*/bin/matlab'), reverse=True)
        if matches:
            args.binary = matches[0]
            print "Using", args.binary
        else:
            print >>sys.stderr, "Couldn't find MATLAB automatically; pass the matlab executable on the command line."
            args.print_help(sys.stderr)

    exec_matlab_server(args.binary, args.port)

#!/usr/bin/python

import os, re, logging

log_patt = re.compile(r'data\.(.+)\.([\d]{10,})')
logger = logging.getLogger('skypespy')

def listdirs(root_dir):
    for dirname, dirnames, filenames in os.walk(root_dir):
        for subdirname in dirnames:
            yield os.path.join(dirname, subdirname)

def aggregate(root_dir):
    if os.path.isdir(root_dir):
        # traverse through the all subdirectories inside the data directory
        for path in listdirs(root_dir):
            f_out = open(os.path.join(path, 'data.%s' % os.path.basename(path)), 'ab')
            # list all the files in a specific folder and append them to one big file
            for fname in os.listdir(path):
                m = log_patt.match(fname)
                if m:
                    logger.info('starting aggregation in %s' % path)
                    try:
                        path_to_file = os.path.join(path, fname)
                        f_in = open(path_to_file, 'rb')
                        f_out.write(f_in.read())
                        f_in.close()
                        # remove old file
                        os.remove(path_to_file)
                    except:
                        logging.warning('could not aggregate data in %s' % path)
                    logger.info('aggregation finished')
            f_out.close()

if __name__ == '__main__':
    aggregate()


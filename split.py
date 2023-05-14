import os, sys

kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                   # default: roughly a floppy

def split(fromfile, todir, parts): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    total_size=os.stat(fromfile).st_size
    chunksize=total_size//parts
    print(parts)
    print(total_size)
    print(chunksize)
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, todir+('%02d' % partnum)+'.txt')
        #filename = os.path.join(todir, ('part%04d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum
            

if len(sys.argv) == 2 and sys.argv[1] == '-help':
    print("Use: split.py [file-to-split target-dir [[parts]]")
else:
    if len(sys.argv) < 3:
        interactive = 1
        fromfile = raw_input('File to be split? ')       # input if clicked 
        todir    = raw_input('Directory to store part files? ')
    else:
        interactive = 0
        fromfile, todir = sys.argv[1:3]                  # args in cmdline
        if len(sys.argv) == 4: parts = int(sys.argv[3])
    absfrom, absto = map(os.path.abspath, [fromfile, todir])
    print('Splitting', absfrom, 'to', absto, 'in', parts, 'parts')

    try:
        parts = split(fromfile, todir, parts)
    except:
        print('Error during split:')
        #print(sys.exc_type, sys.exc_value)
    else:
        print('Split finished:', parts, 'parts are in', absto)
    if interactive: raw_input('Press Enter key') # pause if clicked

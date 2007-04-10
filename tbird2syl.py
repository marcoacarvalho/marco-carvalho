import os
import sys

__author__ = 'Rodrigo Senra <rsenra@acm.org>'
__date__ =  '2005-03-23'
__version__ =  '0.3'

__doc__ = r"""
This module integrates your Mozilla Thunderbird 1.0 tree to
your sylpheed MH mailbox tree.

The script receives two parameters from command-line:
 <Thunderbird folder path> <Sylpheed folder path>

Best way to use it is to go to inside yout Thunderbird
root mailfolder directory and invoke it as:

  <path>\python2.4 <path>\tbird2syl.py . <path to sylpheed>\Mail

This idiom will avoid the creation of the folder Thunderbird inside
your sylpheed folder tree.

If the names of your directories match in both trees, files should
be placed in the correct folder.

This is an alpha release, so it may be a little rough around the edges.
Nevertheless, I used it with great success to convert a very large and
deep folder tree.

Please, do backup your sylpheed (destination) folder tree before trying
this out. Live safe and die old!

This code is released in the public domain.
"""

def harvest_offsets(filepath):
    """Given the filepath, this runs through the file finding
    the number of the line where a message begins.
    
    The functions returns a list of integers corresponding to
    the begining of messages.
    """	
    offsets = []
    state = 'begin'
    for i,line in enumerate(open(filepath)):
        if line.startswith('From ') and state!='found_head':
	    state = 'found_head'
	    continue
        elif line.startswith('Return-Path') and state=='found_head':
	    state = 'found_offset'
	    offsets.append(i)
	    continue
    return offsets

def make_messages(outputdir, filepath, offsets, start):
    """Given a filepath holding several messages in Thunderbird format,
    extarct the messages and create individual files for them, inside
    outputdir with appropriate the appropriate naming scheme.
    """ 
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    if not os.path.exists(filepath):
        raise Exception('Cannot find message file  %s'%(filepath))
    lines = open(filepath).readlines()
    aux = offsets[:]
    msgoffs = zip(offsets[:-1], aux[1:])
    for i,j in msgoffs:
	fd  = open(os.path.join(outputdir,"%d"%start),"w")
	fd.write(''.join(lines[i:j-1])) #-1 to remove first from line
	fd.close()
	start +=1

def process_file(filepath, outputdir):
    """Integrates a Thunderbird message file into a sylpheed message diretory.
    """  
    offs = harvest_offsets(filepath)
    make_messages(outputdir, filepath, offs, 1)


def convert_tree(in_treepath, out_treepath):
    """Traverse your thunderbird tree, converting each message file found into
    a sylpheed message directory.
    """
    for path,subs,files in os.walk(in_treepath):
        if files:
            for f in [x for x in files if not x.endswith('.msf')]:
                if path.endswith('.sbd'):
                    outpath = path[:-4]
                else:
                    outpath = path
                print path,f
                process_file(os.path.join(path,f),
                             os.path.join(out_treepath,outpath,f))
    
if __name__=='__main__':
    if len(sys.argv)<3:
        print __doc__
    else:
        convert_tree(sys.argv[1], sys.argv[2])

 	  	 

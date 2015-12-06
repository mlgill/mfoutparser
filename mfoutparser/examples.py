import os
from sys import modules
from shutil import copytree

def copy_examples(dest_path='.'):
    """Copy mfoutparser example files to a specified directory.

       Input: destination path for mfoutparser example files,
              default directory is the current path.
              If the destination directory exists and is not
              empty, then a directory called "examples" will 
              be created for the files inside the destination
              directory.

       Output: directory with example files
    """

    # Setup examples path
    mfoutpath = modules['mfoutparser'].__path__[0]
    examplespath = os.sep.join([mfoutpath, 'examples'])

    # Setup destination path
    if dest_path is '.':
        dest_path = os.getcwd()
    elif dest_path[0] is not os.sep:
        dest_path = os.sep.join([os.getcwd(), dest_path])

    destination = dest_path

    # Create a new destination directory if current one is not empty
    if os.path.exists(destination):
        if os.listdir(destination) != []:
            destination = os.sep.join([destination, 'examples'])

    # Copy files
    try:
        copytree(examplespath, destination)
    except:
        print('Files could not be copied to {:s}'.format(destination))
    else:
        print('Example files copied to {:s}'.format(destination))

    return
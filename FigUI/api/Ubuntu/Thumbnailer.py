import os
from pathlib import Path
from typing import Tuple, Union
try:
    import magic
    magic = magic.Magic()
except: # import error/platform error.
    magic = None


def totem(input: Union[str, Path], output: Union[str, Path], format: str="png", show_progress: bool=False, verbose: bool=False, execute: bool=True) -> Tuple[str, int]:
    '''
    TODO: replace with C/C++ binding if possible!
    A function to create thumbnails for videos using the totem thumbnailer. Default behaviour is to build the command and invoke it and return the status code and constructed command, however you can just build the command and not execute it, if you want to!
    
    **Arguments** :
    input:
    output:
    format:
    show_progress:
    verbose:
    execute:

    **Returns** : 
    cmd: the built command.
    status: status code on execution of the command.
    '''
    # get asbolute input path.
    input = str(input)
    output = str(output)
    input = os.path.realpath(input)
    # print(input)
    # ascertain that the file is a video file.
    if magic and not magic.from_file(input).startswith("video"):
        return
    cmd = f"totem-video-thumbnailer {input} {output}"
    if format == "jpeg":
        cmd += " --jpeg"
    if verbose:
        cmd += " -v"
    if show_progress:
        cmd += " -p"
    if execute:
        status = os.system(cmd)

    return cmd, status
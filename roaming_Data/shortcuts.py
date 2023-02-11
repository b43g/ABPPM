import os, platform

def startup():

    python_data = "Python Version: {}, {} \n{}".format(platform.python_version(), platform.architecture(), platform.python_build())
    return python_data
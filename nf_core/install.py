#!/usr/bin/env python
""" Install software for nf-core pipelines """

from __future__ import print_function

import logging
import requests
import subprocess
import os
import tempfile


def install_tools(tools):
    """ Master function to install tools """
    if 'nextflow' in tools:
        if nextflow_is_installed():
            logging.error("Nextflow is already installed! Skipping..")
        else:
            nextflow_install()


def nextflow_is_installed():
    """ Check if nextflow is installed """
    logging.info("Checking if nextflow is already installed")
    try:
        subprocess.call(['nextflow', '-version'])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
        else:
            raise
    else:
        return True

def singularity_is_installed():
    """ Check if singularity is installed """
    logging.info("Checking if singularity is already installed")
    try:
        subprocess.call(['singularity', '--version'])
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
        else:
            raise
    else:
        return True

def nextflow_install():
    """ Install nextflow """
    logging.info("Installing nextflow")
    response = requests.get('http://get.nextflow.io')
    install_script = response.text
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    logging.debug("Installing nextflow to {}".format(tmpdir))
    nf_install_exit_code = subprocess.call(install_script, shell=True)
    logging.debug("Nextflow install exit code: {}".format(nf_install_exit_code))
    bin_paths = ['~/bin']
    for path in bin_paths:
        logging.debug("Attempting to move nextflow to {}".format(path))
        try:
            os.rename(os.path.join(tmpdir, 'nextflow'), os.path.expanduser(path))
        except OSError as e:
            pass
        else:
            logging.info("Installed nextflow to {}".format(path))
            break
    else:
        logging.error("Was not able to move nextflow binary to directory in PATH")

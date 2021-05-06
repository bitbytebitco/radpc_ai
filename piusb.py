#!/usr/bin/python

import os
import subprocess
import shutil

lock_file = "piusb.lck"

def is_piusb_loaded():
    """ Checks if `g_mass_storage` kernel module loaded. Ensure
        that a lock file is in place if kernel module is loaded.

    Returns:
        True or False 

    """

    try:
        p = subprocess.Popen('lsmod | grep g_mass_storage', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()

        # ensure that lock file in place
        create_piusb_lock()
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        
    if len(output)>0:
        return True
    else:
        return False

def create_piusb_lock():
    """ Create empty lock file. 

    """

    if not os.path.exists(lock_file):
        open(lock_file,"a").close()


def unload_piusb():
    """ Unload `g_mass_storage` module and remove associated lock file. 

    """

    try:
        print("Unmounting Raspberry Pi as USB from host machine")
        subprocess.call("sudo rmmod g_mass_storage", shell=True)
    except Exception as e:
        print(e)


def load_piusb():
    """ Load `g_mass_storage` kernel module and create associated lock file. 

    """
    try:
        p = subprocess.Popen('sudo modprobe g_mass_storage file=/memory.bin stall=0 ro=0', 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        output, err = p.communicate()

    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)

def reboot_pi():
    """ Reboot Raspberry Pi 

    """
    try:
        print("Rebooting Raspberry Pi")
        subprocess.call("sudo reboot", shell=True)
    except Exception as e:
        print(e)

def backup_memory_partition():
    fromDirectory = "/mnt/memory"
    toDirectory = "/mnt/backup"

    try:
        print("Backing up `/memory` to `/backup`")
        files = [f for f in os.listdir(fromDirectory)]
        print(files)
        for f in files:
            fp = os.path.join(fromDirectory, f)
            shutil.copy(fp, toDirectory)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Is RPI plugged into host?
    # IF HOST finished with RPI THEN "disconnect" RPI as USB 
        
    # DO functions unsafe to do while RPI acting as USB
        # backup /memory to /backup 
    

    g_mass_loaded = is_piusb_loaded()
    print("g_mass_loaded loaded: {}".format(g_mass_loaded))

    if g_mass_loaded:
        unload_piusb()

    backup_memory_partition()


from microIO import resolve_pin, pinmap_search

__I2C = None


def __init():
    global __I2C
    if __I2C is None:
        from machine import Pin, I2C
        __I2C = I2C(-1, Pin(resolve_pin('i2c_scl')), Pin(resolve_pin('i2c_sda')))
    return __I2C


def scan():
    """
    I2C scan function - experimental
    :return list: list of devices
    """
    # https://docs.micropython.org/en/latest/library/machine.I2C.html
    return __init().scan()


#######################
# LM helper functions #
#######################

def pinmap():
    """
    [i] micrOS LM naming convention
    Shows logical pins - pin number(s) used by this Load module
    - info which pins to use for this application
    :return dict: pin name (str) - pin value (int) pairs
    """
    return pinmap_search(['i2c_scl', 'i2c_sda'])


def help(widgets=False):
    """
    [BETA][i] micrOS LM naming convention - built-in help message
    :return tuple:
        (widgets=False) list of functions implemented by this application
        (widgets=True) list of widget json for UI generation
    """
    return 'scan', 'pinmap'

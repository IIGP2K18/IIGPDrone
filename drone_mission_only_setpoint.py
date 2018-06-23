import time
from functions import *

setpoint_local_position( 2, 2, 0, 0, tolerance=0.5, relative=True)
setpoint_local_position( 2,-2, 0, 0, tolerance=0.5, relative=True)
setpoint_local_position(-2,-2, 0, 0, tolerance=0.5, relative=True)
setpoint_local_position(-2, 2, 0, 0, tolerance=0.5, relative=True)

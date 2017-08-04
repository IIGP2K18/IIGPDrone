import rospy
from core_api.srv import *

def get_global_namespace():
    rospy.wait_for_service('/get_global_namespace')
    try:
        res = rospy.ServiceProxy('/get_global_namespace', ParamGetGlobalNamespace)
        op = res()
        return str(op.param_info.param_value)
    except rospy.ServiceException, e:
        rospy.logerr("global namespace service not available", e)
        return None

def access_request(enable_access):
    rospy.wait_for_service('/flytos/navigation/access_request')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/access_request', AccessRequest)
        resp = handle(enable_access=enable_access)
        return resp
    except rospy.ServiceException, e:
	rospy.logerr("service call failed %s", e)

def arm():
    rospy.wait_for_service('/flytos/navigation/arm')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/arm', Arm)
        resp = handle()
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)

def disarm():
    rospy.wait_for_service('/flytos/navigation/disarm')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/disarm', Disarm)
        resp = handle()
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)

def takeoff(height):
    rospy.wait_for_service('/flytos/navigation/take_off')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/take_off', TakeOff)
        resp = handle(takeoff_alt=height)
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)


def land(async= False):
    rospy.wait_for_service('/flytos/navigation/land')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/land', Land)
        resp = handle(async)
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)

def position_hold():
    rospy.wait_for_service('/flytos/navigation/position_hold')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/position_hold', PositionHold)
        resp = handle()
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)

def setpoint_local_position(lx, ly, lz, yaw, tolerance = 2.0, async = False, relative= False, yaw_valid= False, body_frame= False):
    rospy.wait_for_service('/flytos/navigation/position_set')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/position_set', PositionSet)

        # building message structure
        req_msg = PositionSetRequest(x=lx, y=ly, z=lz, yaw=yaw, tolerance=tolerance, async=async, relative=relative, yaw_valid=yaw_valid, body_frame=body_frame)
        resp = handle(req_msg)
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("pos set service call failed %s", e)

def setpoint_global_position(lat_x, long_y, rel_alt_z, yaw, tolerance= 0.0, async = False, yaw_valid= False):
    rospy.wait_for_service('/flytos/navigation/position_set_global')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/position_set_global', PositionSetGlobal)

        # build message structure
        req_msg = PositionSetGlobalRequest(lat_x=lat_x, long_y=long_y, rel_alt_z=rel_alt_z, yaw=yaw, tolerance=tolerance, async=async, yaw_valid=yaw_valid)
        resp = handle(req_msg)
        return resp

    except rospy.ServiceException, e:
        rospy.logerr("global pos set service call failed %s", e)

def setpoint_velocity(vx, vy, vz, yaw_rate, tolerance= 1.0, async = False, relative= False, yaw_rate_valid= False, body_frame= False):
    rospy.wait_for_service('/flytos/navigation/velocity_set')
    try:
        handle = rospy.ServiceProxy('/flytos/navigation/velocity_set', VelocitySet)
        # build message structure
        req_msg = VelocitySetRequest(vx=vx, vy=vy, vz=vz, yaw_rate=yaw_rate, tolerance=tolerance, async=async, relative=relative, yaw_rate_valid=yaw_rate_valid, body_frame=body_frame)
        resp = handle(req_msg)

        return resp
    except rospy.ServiceException, e:
        rospy.logerr("vel set service call failed %s", e)








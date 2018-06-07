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

def access_request(enable_access)
    rospy.wait_for_service('/<namespace>/navigation/access_request')
    try:
        handle = rospy.ServiceProxy('/<namespace>/navigation/access_request', AccessRequest)
        resp = handle(enable_access=enable_access)
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("service call failed %s", e)

print(get_global_namespace())

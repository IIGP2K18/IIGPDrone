echo "Pre start cleanup"
killall rosmaster
killall python

echo "Starting MAVROS"
roslaunch mavros px4.launch fcu_url:="///dev/ttyACM0:921600" gcs_url:=udp://@192.168.43.251:14550 &> /dev/null &
sleep 2

echo "Starting ping_ros"
python ping_ros.py &> /dev/null &
sleep 2

echo "Starting Main Control Code"
python offb_obst_simple.py

echo "Cleanup"
killall python
killall rosmaster

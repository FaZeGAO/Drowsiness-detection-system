from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import time
import os
from utilities import process_image, support_redis,process_image_data, get_data
import requests
import asyncio
import subprocess

COUNTER = 0
bostezo=0
alarm_status = False
alarm_status2 = False
alerta=False
count_alert=0
lack_alert=False
frameTime = 1

docker_compose_directory = '/home/sersch/docker_compose_detection'
querry="curl -X 'POST' 'http://localhost:8080/execute_command/?command=%22ALERTA%20DE%20SOMNOLENCIA%2C%20TE%20ESTAS%20QUEDANDO%20DORMIDO%22' -H 'accept: application/json' -d ''"
os.popen("sudo -S %s"%( "sudo sdptool add SP" ), 'w').write('1234')
subprocess.Popen(["docker", "compose", "up", "-d"], cwd=docker_compose_directory)
print("Levantando servicios")
time.sleep(12)
print("-> Loading the predictor and detector...")
rd=support_redis("172.16.0.4",6379)
print("-> Conecting redis")
print("-> Starting Video Stream")

#vs = cv2.VideoCapture('/home/sersch/Desktop/calibracion.mp4')  
#vs = VideoStream(src = '/home/sersch/Desktop/cal.mp4').start()
vs = VideoStream(src = 0).start()
#frame_delay = 1 / 30


while True:

    if lack_alert:
        count_alert=count_alert+1
    if count_alert>200:
        lack_alert=False
        count_alert=0
    
    print("count_alert: ",count_alert)
    
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image_data = process_image_data(gray)

    data_redis={"gray":image_data, 
                "COUNTER":COUNTER, 
                "bostezo":bostezo,  
                "alarm_status":alarm_status,
                "alarm_status2":alarm_status2, 
                "alerta":alerta
                 }
    
    rd.store_dict_in_redis(redis_key="variables", data=data_redis)
    response = requests.get("http://localhost/predictor")
    data=response.json()
    alerta, COUNTER, ear, lip, rightEyeHull, leftEyeHull, bostezo, distance, alarm_status, alarm_status2 = get_data(data)
    
    if count_alert>1:
        alerta=False
        
    rd.redis_client.set("alerta", int(alerta))
    
    if (type(leftEyeHull)!= type(np.NaN)) & (type(rightEyeHull) !=type(np.NaN)):
        leftEyeHull = np.array(leftEyeHull)
        rightEyeHull = np.array(rightEyeHull)
        
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

    print(alerta,bostezo)
    
    if type(lip) != type(np.NaN):
        lip = np.array(lip)
        cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)
    
    if alerta:
        lack_alert=True

        cv2.putText(frame, "ALERTA de somnolencia!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if count_alert==0:
            subprocess.Popen([querry], shell=True)

    cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.moveWindow("Frame",600,300)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    #time.sleep(frame_delay)    
    
    rd.redis_client.delete("variables") 


cv2.destroyAllWindows()
vs.stop()

    
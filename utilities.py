import numpy as np
import pickle
import redis
import cv2

def get_data(data):
    
    if data["leftEyeHull"] == 'nan':
        leftEyeHull = np.NaN
    else:
        leftEyeHull=eval(data["leftEyeHull"])
    
    if data["rightEyeHull"] == 'nan':
        rightEyeHull = np.NaN
    else:
        rightEyeHull=eval(data["rightEyeHull"])
    
    if data["lip"] == 'nan':
        lip = np.NaN
    else:
        lip=eval(data["lip"])
    
    ear=data['ear']

    COUNTER=data["COUNTER"]
    alerta=data['alerta']
    bostezo=data['bostezo']
    distance=data["distance"]
    alarm_status=data['alarm_status']  
    alarm_status2=data['alarm_status2']


    return alerta, COUNTER, ear, lip, rightEyeHull, leftEyeHull, bostezo, distance, alarm_status, alarm_status2

def process_image(image_path):
    image = cv2.imread(image_path)    
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

def process_image_data(image):    
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

def deserialize_dict(serialized_data):
    return pickle.loads(serialized_data)

def serialize_dict(data):
    return pickle.dumps(data)

def decode_image(image_data):
    # Convert image data (bytes) back to a numpy array
    image_np_array = np.frombuffer(image_data, dtype=np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)
    return image

class support_redis:
    def __init__ (self,hostname,port):
        self.hostname=hostname
        self.port=port
        self.redis_client = redis.StrictRedis(host=self.hostname, port=self.port, db=0)
    
    def store_dict_in_redis(self,redis_key, data):
        serialized_data = serialize_dict(data)
        self.redis_client.set(redis_key, serialized_data)

    def get_dict_from_redis(self,redis_key):
        serialized_data = self.redis_client.get(redis_key)
        if serialized_data:
            return deserialize_dict(serialized_data)
        return None
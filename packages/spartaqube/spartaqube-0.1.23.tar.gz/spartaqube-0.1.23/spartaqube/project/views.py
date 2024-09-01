import os,json,base64,json
def sparta_13c671eb4b():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def sparta_3b770b7aa3(b):return base64.b64decode(b).decode('utf-8')
def sparta_b3002852da(s):return base64.b64encode(s.encode('utf-8'))
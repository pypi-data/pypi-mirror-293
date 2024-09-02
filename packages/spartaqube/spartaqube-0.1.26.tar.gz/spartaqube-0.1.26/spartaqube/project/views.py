import os,json,base64,json
def sparta_b9c6ae7ccf():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def sparta_a15226cbe5(b):return base64.b64decode(b).decode('utf-8')
def sparta_f12c206714(s):return base64.b64encode(s.encode('utf-8'))
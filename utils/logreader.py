import os
import json
import numpy as np
import matplotlib.pyplot as plt

event_counter = 0
epoch = []
mAP = []
_ac=[]
_2c=[]
_3c=[]
_4c=[]
_5c=[]
_6c=[]
_7c=[]
_8c=[]
_9c=[]
_10c=[]
_jc=[]
_qc=[]
_kc=[]
_ah=[]
_2h=[]
_3h=[]
_4h=[]
_5h=[]
_6h=[]
_7h=[]
_8h=[]
_9h=[]
_10h=[]
_jh=[]
_qh=[]
_kh=[]
_as=[]
_2s=[]
_3s=[]
_4s=[]
_5s=[]
_6s=[]
_7s=[]
_8s=[]
_9s=[]
_10s=[]
_js=[]
_qs=[]
_ks=[]
_ad=[]
_2d=[]
_3d=[]
_4d=[]
_5d=[]
_6d=[]
_7d=[]
_8d=[]
_9d=[]
_10d=[]
_jd=[]
_qd=[]
_kd=[]

with open('log2.txt') as json_file:
    data = json.load(json_file)
    for e in data['events']:
        msg = e['message']
        if "INFO:root:[" in msg and "Validation:" in msg:
            epoch.append(msg[msg.index("Epoch")+6: msg.index("]")])
        if "mAP=" in msg:
            mAP.append(float(msg[msg.index("mAP=")+4:]))
        if msg.startswith("ac="):
            _ac.append(float(msg[msg.index("ac=")+3:]))
        if msg.startswith("2c="):
            _2c.append(msg[msg.index("2c=")+3:])
        if msg.startswith("3c="):
            _3c.append(msg[msg.index("3c=")+3:])
        if msg.startswith("4c="):
            _4c.append(msg[msg.index("4c=")+3:])
        if msg.startswith("5c="):
            _5c.append(msg[msg.index("5c=")+3:])
        if msg.startswith("6c="):
            _6c.append(msg[msg.index("6c=")+3:])
        if msg.startswith("7c="):
            _7c.append(msg[msg.index("7c=")+3:])
        if msg.startswith("8c="):
            _8c.append(msg[msg.index("8c=")+3:])
        if msg.startswith("9c="):
            _9c.append(msg[msg.index("9c=")+3:])
        if msg.startswith("10c="):
            _10c.append(msg[msg.index("10c=")+4:])
        if msg.startswith("jc="):
            _jc.append(msg[msg.index("jc=")+3:])
        if msg.startswith("qc="):
            _qc.append(msg[msg.index("qc=")+3:])
        if msg.startswith("kc="):
            _kc.append(msg[msg.index("kc=")+3:])
        if msg.startswith("ah="):
            _ah.append(msg[msg.index("ah=")+3:])
        if msg.startswith("2h="):
            _2h.append(msg[msg.index("2h=")+3:])
        if msg.startswith("3h="):
            _3h.append(msg[msg.index("3h=")+3:])
        if msg.startswith("4h="):
            _4h.append(msg[msg.index("4h=")+3:])
        if msg.startswith("5h="):
            _5h.append(msg[msg.index("5h=")+3:])
        if msg.startswith("6h="):
            _6h.append(msg[msg.index("6h=")+3:])
        if msg.startswith("7h="):
            _7h.append(msg[msg.index("7h=")+3:])
        if msg.startswith("8h="):
            _8h.append(msg[msg.index("8h=")+3:])
        if msg.startswith("9h="):
            _9h.append(msg[msg.index("9h=")+3:])
        if msg.startswith("10h="):
            _10h.append(msg[msg.index("10h=")+4:])
        if msg.startswith("jh="):
            _jh.append(msg[msg.index("jh=")+3:])
        if msg.startswith("qh="):
            _qh.append(msg[msg.index("qh=")+3:])
        if msg.startswith("kh="):
            _kh.append(msg[msg.index("kh=")+3:])
        if msg.startswith("ad="):
            _ad.append(msg[msg.index("ad=")+3:])
        if msg.startswith("2d="):
            _2d.append(msg[msg.index("2d=")+3:])
        if msg.startswith("3d="):
            _3d.append(msg[msg.index("3d=")+3:])
        if msg.startswith("4d="):
            _4d.append(msg[msg.index("4d=")+3:])
        if msg.startswith("5d="):
            _5d.append(msg[msg.index("5d=")+3:])
        if msg.startswith("6d="):
            _6d.append(msg[msg.index("6d=")+3:])
        if msg.startswith("7d="):
            _7d.append(msg[msg.index("7d=")+3:])
        if msg.startswith("8d="):
            _8d.append(msg[msg.index("8d=")+3:])
        if msg.startswith("9d="):
            _9d.append(msg[msg.index("9d=")+3:])
        if msg.startswith("10d="):
            _10d.append(msg[msg.index("10d=")+3:])
        if msg.startswith("jd="):
            _jd.append(msg[msg.index("jd=")+3:])
        if msg.startswith("qd="):
            _qd.append(msg[msg.index("qd=")+3:])
        if msg.startswith("kd="):
            _kd.append(msg[msg.index("kd=")+3:])
        if msg.startswith("2s="):
            _2s.append(msg[msg.index("2s=")+3:])
        if msg.startswith("3s="):
            _3s.append(msg[msg.index("3s=")+3:])
        if msg.startswith("4s="):
            _4s.append(msg[msg.index("4s=")+3:])
        if msg.startswith("5s="):
            _5s.append(msg[msg.index("5s=")+3:])
        if msg.startswith("6s="):
            _6s.append(msg[msg.index("6s=")+3:])
        if msg.startswith("7s="):
            _7s.append(msg[msg.index("7s=")+3:])
        if msg.startswith("8s="):
            _8s.append(msg[msg.index("8s=")+3:])
        if msg.startswith("9s="):
            _9s.append(msg[msg.index("9s=")+3:])
        if msg.startswith("10s="):
            _10s.append(msg[msg.index("10s=")+4:])
        if msg.startswith("js="):
            _js.append(msg[msg.index("js=")+3:])
        if msg.startswith("qs="):
            _qs.append(msg[msg.index("qs=")+3:])
        if msg.startswith("ks="):
            _ks.append(msg[msg.index("ks=")+3:])
#plt.axis([min(epoch), max(epoch),min(mAP), max(mAP)])
plt.xlabel("Epoch")
plt.ylabel("mAP")

#plt.annotate('mAP Collapse @ Epoch 30', xy=(30,max(mAP)),
#             xytext=(40, max(mAP)), arrowprops=dict(facecolor='black',
#                                              shrink=0.05),)

#plt.plot(epoch, mAP)
plt.plot(_ac, _2c, _3c, _4c, _5c, _6c, _7c, _8c, _9c, _10c, _jc, _qc, _kc)
#plt.axis([0.0, 184, 0.0, 0.5])
plt.axis('off')
plt.xlabel("Epoch")
plt.ylabel("mAP")
plt.legend()
plt.show()
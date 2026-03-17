import struct, time, random, hashlib
 
class SensorNode:
    def __init__(self, nid, battery=100):
        self.id=nid; self.battery=battery; self.readings=[]
    def sense(self):
        v=random.gauss(25.0,2.0)  # temperature
        self.readings.append(v); self.battery-=0.01; return v
    def aggregate(self, method='avg'):
        if not self.readings: return None
        if method=='avg': return sum(self.readings)/len(self.readings)
        if method=='min': return min(self.readings)
        if method=='max': return max(self.readings)
          class ClusterHead(SensorNode):
    def __init__(self, nid):
        super().__init__(nid,200); self.members=[]
    def collect(self):
        data=[m.aggregate() for m in self.members if m.aggregate() is not None]
        return sum(data)/len(data) if data else None
    def compress(self, data):
        packed=struct.pack(f'{len(data)}f', *data)
        return packed, hashlib.md5(packed).hexdigest()
 
nodes=[SensorNode(i) for i in range(10)]
ch=ClusterHead(99); ch.members=nodes
for _ in range(5):
    for n in nodes: n.sense()
agg=ch.collect()
print(f"Cluster head aggregate: {agg:.2f}°C, Battery: {ch.battery}")

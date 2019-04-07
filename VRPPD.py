import pandas as pd

'''
class MyClass(object):
    def __init__(self, number):
        self.number = number

my_objects = []

for i in range(100):
    my_objects.append(MyClass(i))

# later

for obj in my_objects:
    print obj.number
    
#Import xlsx
df = pd.ExcelFile(file_name, sheet_name=SheetName)
listdf = df.tolist() #Baris Pertama langsung diabaikan
'''
'''
Struktur data order = [ID, Titik Awal, Titik Tujuan, Jumlah Penumpang]
Struktur data kendaraan = [ID, Titik Sekarang, Rute, Jarak tempuh, Waktu tempuh]
Struktur data lokasi = [Nama, List Order dengan titik awal nama lokasi]
'''

file_name = "DataMasuk.xlsx"
	
class Kendaraan():
	def __init__(self, nomor, kapasitas, startnode):
		self.nomor 			= nomor
		self.kapasitas		= kapasitas
		self.currentnode	= startnode
		self.sequence		= 0
		self.jaraktempuh	= 0
		self.waktutempuh	= 0
		self.rute			= []
		self.cri			= 0 #current rute index
		self.nri			= 0
		self.currentnodeid	= 0
		self.nextnodeid		= 0
		self.currenttask	= [-1]
		self.aktif			= 1
		self.log			= []
	
	def plan(self):
		n = 0
		p = self.cekorder(self.cri)
		if(p == 0):
			n = self.cekdemand()
		if(p+n == 0):
			self.aktif = 0
			return 0
		self.jalan()
		self.droptask()
		return 1
		
	def jalan(self):		
		self.log.append(self.currenttask[:])
		self.waktutempuh 	+= self.currenttask[4]
		self.jaraktempuh 	+= self.currenttask[3]
		self.cri = self.nri
		self.currentnodeid	= self.nextnodeid
		
	def cekorder(self, ruteindex):
		nodeId = self.rute[ruteindex]
		if(ruteindex+1 == len(self.rute)): #Menentukan ID node selanjutnya
			nodeIdnext = 1 #EP
		else:
			nodeIdnext = self.rute[ruteindex+1]
		for p in daftar_nodes[nodeId-1].avorder: #mencari apakah ada order yang mau ke nodeId selanjutnya
			if(p[2] == nodeIdnext):
				if(p[1] == nodeId):
					self.currenttask = p
					p[6] -= 1
				return 1
		return 0
	
	def cekdemand(self):
		flag = 0
		for i in range(self.cri+1, len(self.rute)):
			flag = self.cekorder(i)
			if(flag==1):
				self.nri = self.cri
				taskid = str(self.currentnodeid)+"-"+str(self.rute[i])
				for p in daftar_order:
					if(taskid == p[0]):
						temp = p[:]
						temp[6] = -1
						self.currenttask = temp 
				return 1
		for i in range(0, self.cri):
			flag = cekorder(i)
			if(flag==1):
				self.nri = self.cri
				taskid = str(self.currentnodeid)+"-"+str(self.rute[i])
				for p in daftar_order:
					if(taskid == p[0]):
						temp = p[:]
						temp[6] = -1
						self.currenttask = temp 
				return 1
		return 0
		
	def droptask(self):
		self.currenttask	= [-1]
		
class Nodes():
	def __init__(self, id, nama):
		self.id				= id
		self.nama			= nama
		self.avorder		= []
		
	def cleanup(self):
		for i in range(len(self.avorder)-1, -1,-1):
			if(self.avorder[i][6]==0):
				del self.avorder[i]

def cavod(i):
	for p in i:
		print(p.nama)
		print(p.avorder)
		print("===========")
	
daftar_order		= []
daftar_kendaraan	= []
daftar_nodes		= []
daftar_rute 		= []

def main():	
	global daftar_kendaraan, daftar_nodes, daftar_order, daftar_rute
	
	# Load Data #
	#Order
	df = pd.read_excel(file_name, sheet_name = "Order")
	daftar_order = df.values.tolist()
	#Kendaraan
	df = pd.read_excel(file_name, sheet_name = "Kendaraan")
	temp = df.values.tolist()
	daftar_kendaraan = []
	for x in temp:
		daftar_kendaraan.append(Kendaraan(x[0],x[1],x[2]))
	#Rute
	daftar_rute = []
	df = pd.read_excel(file_name, sheet_name = "Rute")
	temp = df.values.tolist()
	for n in temp:
		daftar_rute.append([int(i) for i in n if str(i) != 'nan'])
	#Nodes
	df = pd.read_excel(file_name, sheet_name = "Nodes")
	temp = df.values.tolist()
	daftar_nodes = []
	for x in temp:
		daftar_nodes.append(Nodes(x[0],x[1]))
	'''	
	print(daftar_order)
	print(daftar_kendaraan)
	print(daftar_nodes)
	print(daftar_rute)
	'''
	# Assign order to node #
	for p in daftar_order:
		daftar_nodes[p[1]-1].avorder.append(p)
	for p in daftar_nodes:
		p.cleanup()
	
	cavod(daftar_nodes)
	
	# Assign Route for every vehicle #
	for p in range(0, len(daftar_rute)):
		daftar_kendaraan[p].rute = daftar_rute[p]
		#print(daftar_kendaraan[p].rute)
	
	# Running Simulation #
	'''
	print(daftar_nodes[1].avorder)
	daftar_kendaraan[4].cekorder(1)
	daftar_kendaraan[4].jalan()
	print(daftar_kendaraan[4].jaraktempuh)
	print(daftar_kendaraan[4].waktutempuh)
	print(daftar_nodes[1].avorder)
	'''
	flag = 1
	iterasi = 0
	while(flag):
		flag = 0
		for p in daftar_kendaraan:
			temp = p.plan()
			if(temp==1):
				flag = 1
			for c in daftar_nodes:
				c.cleanup()
		cavod(daftar_nodes)
		iterasi += 1
		print("===========> {}".format(iterasi))

	for p in daftar_kendaraan:
		print("{}\t{:.1f}\t{}".format(p.nomor, p.jaraktempuh, p.waktutempuh))
	#input()
	for q in daftar_kendaraan:
		for p in q.log:
			print(p)
		print("{}\t{:.1f}\t{}".format(q.nomor, q.jaraktempuh, q.waktutempuh))
if __name__ == '__main__':
	main()

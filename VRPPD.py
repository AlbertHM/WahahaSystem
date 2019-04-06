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
		self.currentindex	= 0
		self.currentnode	= 0
		self.nextnode		= 0
		self.currentorder	= []
	
	def plan(self):
		if((self.currentindex + 1) > (len(self.rute)-1)):
			self.nextnode = self.rute[0]
			self.currentindex = 0
		else:
			self.nextnode = self.rute(self.currentindex+1)
		
		if(self.nextnode != -1):
			return 1
		else:
			return 0
		
	def jalan(self):		
		temp 				= self.currentorder[3:5] #[Waktu, Jarak]
		self.waktutempuh 	+= temp[0]
		self.jaraktempuh 	+= temp[1]
		self.currentnode 	= self.nextnode
		
	def cekorder(self, nodeId):
		#for p in daftar_nodes[nodesId].avorder
		pass
	
	def cekdemand(self):
		pass
	
	def pickup(self):
		pass
		
	def drop(self):
		self.currentorder	= [0]
		
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
		daftar_rute.append([i for i in n if str(i) != 'nan'])
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
		print(daftar_kendaraan[p].rute)
	
	# Running Simulation #
	'''
	jalan = 1
	while(jalan):
		jalan = 0
		for p in daftar_kendaraan:
			if(p.currentorder):
				p.drop()
			if(p.plan):
				jalan = 1
				p.jalan()'''
	
	
if __name__ == '__main__':
	main()

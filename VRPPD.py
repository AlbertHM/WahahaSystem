import pandas as pd

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
		self.currentnodeid	= 1
		self.nextnodeid		= 0
		self.currenttask	= [-1]
		self.aktif			= 1
		self.log			= []
	
	def cetak(self):
		print(self.nomor)
		print(self.cri)
		print(self.nri)
	
	def plan(self):
		#Melakukan pengecekan order pada titik tersebut
		p = [1,0]
		#print("Mulai proses =============")
		#self.cetak()
		p = list(self.cekorder(self.cri))
		#Apabila ada, ambil tasknya p[0] status, p[1] available order
		if(p[0]):
		#	NRI = CRI + 1
			#print("Masuk Order")
			if(self.cri + 1 == len(self.rute)):
				self.nri = 0
			else:
				self.nri = self.cri + 1
			p[1][6] -=1
		#Jika tidak, lakukan cek demand
		else:
		#	Untuk setiap nodes pada rute
			#print("Masuk Demand")
			k=0
			for i in range(self.cri+1, len(self.rute)):
		#		Cek Order jika ada NRI = index node
				k = list(self.cekorder(i))[0]
				#print("Checking")
				#print(str(k) +"--"+ str(i))
				if(k==1):
					self.nri = i
					break
			if(k!=1):
				for i in range(0, self.cri):
					k = list(self.cekorder(i))[0]
					#print(str(k) +"--"+ str(i))
					if(k==1):
						self.nri = i
						break
			#print("End of checking")
			if(k!=1):
				print("STOPPING CONDITION")
				self.cetak()
				return 0
			taskId = str(self.rute[self.cri]) +"-"+ str(self.rute[self.nri])
			#print("TASK ID")
			#print(taskId)
			for u in daftar_order:
				#print("get here")
				if(taskId == u[0]):
					#print("gotcha")
					p[1] = u[:]
					p[1][6] = -1
					break
		#	Berjalan ke nodes yg di tunjuk NRI tersebut
		self.log.append(p[1][:])
		#print("Current task " +str(p[1][:]))
		self.waktutempuh += p[1][4]
		self.jaraktempuh += p[1][3]
		#print("CRI | NRI0 : " + str(self.cri) + "\t" +str(self.nri))
		self.cri = self.nri
		#self.cetak()
		#print("Akhir proses =============")
		return 1
		
	def cekorder(self, ruteindex):
		#print("===/CekOrder\===")
		a = self.rute[ruteindex]
		if(ruteindex+1 == len(self.rute)): #Menentukan ID node selanjutnya
			b = 1 #EP
		else:
			b = self.rute[ruteindex+1]
		for p in daftar_nodes[a-1].avorder:
			if(p[2] == b):
				#print("===\CekOrder/===")
				return 1,p #Ada order nih, nih ordernya
		#print("===\CekOrder/===")
		return 0,-1 #Ga ada order yg cocok di titik ini
				
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

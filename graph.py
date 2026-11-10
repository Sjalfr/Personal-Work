class graf_analyze:
    def __init__(self):
        self.hodnoty_grafu()

    def hodnoty_grafu(self):
        self.graf= [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        self.gVelikost= 4
    
    def vypis_grafu(self):
        vGraf= []
        for i in range(self.gVelikost):
            row= self.graf[i * self.gVelikost : (i + 1) * self.gVelikost]
            vGraf.append(row)
            print(row)  
        return vGraf

analyza= graf_analyze()
analyza.vypis_grafu()

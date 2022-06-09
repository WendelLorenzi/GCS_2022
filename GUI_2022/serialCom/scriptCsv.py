     with open('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/Counter.csv','w') as counter:
            lista = self.countPackage(self.getTam('/home/wendel/Área de trabalho/LtSat/GCS_2022/GUI_2022/datasets/csvTransicao/packageType.csv'))
            counter = self.unloadVet(counter, lista)
            
    def countPackage(self, tam):
        cont = 0
        packageCounter = []
        while(cont == tam):
            cont= cont + 1
            packageCounter.append(cont)
            if (count == (tam - 1)):
                return packageCounter
            
    
    def getTam(self, path): 
        results = pd.read_csv(str(path))   
        return results[results.columns[0].count()]
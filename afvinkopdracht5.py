#   Auteur: Sil van Appeldoorn
#   Jaar: december 2017
#   Code Neemt een DNA sequentie en kan vervolgens de volgende dingen teruggeven: de DNA sequentie, de lengte, het transcript en het GC%.

import re
import pickle

output = open('aa_dict.dat', 'rb')
aa_dict = pickle.load(output)
output.close()

class sequentie:
    def __init__(self,seq):
        self.setSeq(seq)

    def setSeq(self,seq):
        self.seq = seq

    def getSeq(self):
        return self.seq

    def getLength(self):
        return len(self.seq)
    

class DNA(sequentie):
    def __init__(self,seq):
        sequentie.__init__(self,seq)
        self.setDNA(seq)

    def setDNA(self,seq):
        try:
            self.seq = seq
            teldna = re.match('^[ATGCN]*$',self.seq.upper())
            if teldna == None:
                raise SystemError        
        except SystemError:
            print('Dit is geen DNA sequentie')

##    def getDNA(self):
##        return self.seq

    def getTranscript(self):
        RNA = ''
        for x in self.seq.upper():
            if x == 'A':
                RNA += 'U'
            if x == 'T':
                RNA += 'A'
            if x == 'G':
                RNA += 'C'
            if x == 'C':
                RNA += 'G'
        return RNA

##    def getLength(self):
##        return len(self.seq)

    def getGC(self):
        
        g = self.seq.count('C')
        c = self.seq.count('G')
        GC = (g + c)/len(self.seq)*100
        return GC     
        
class RNA(DNA):
    def __init__(self,seq):
        sequentie.__init__(self,seq)
        self.Translation = RNA
    
    def getTranslation(self):

        self.seq = self.seq.lower()

        protein = ''
        start = self.seq.find('atg')
        startseq = self.seq[start:]

        file = []
        doorgaan = True

        while doorgaan == True:
            if len(startseq) >= 3:
                file.append(startseq[0:3])
                startseq = startseq[3:]
            else:
                doorgaan = False

        for x in file:
            try:
                if x == 'taa' or x == 'tag' or x == 'tga':
                    raise TypeError
                else:
                    protein += aa_dict[x]

            except TypeError:
                return protein
        
        
#   Code neemt een bestand in, bekijkt hiervan of het DNA is of niet en vervolgens kijkt die welke sequentie van het bestand het hoogste GC% heeft.
#   Daarbij print die dan het bijbehorend transcript en lengte.

dnaLijst = []
headerLijst = []

def main():

    bestand = open('afvink5.txt','r')
    x = ''
    z = ''
    GClijst = []
    dna_sort = []

    for line in bestand:
        line = line.rstrip()
        if line.startswith('>'):
            z += line
            headerLijst.append(z)
        if not line.startswith('>'):
            x += line
            z = ''
        if line.startswith('>') and x is not '':
            dnaLijst.append(RNA(x))
            x = ''
    dnaLijst.append(RNA(x))

    for x in dnaLijst:
        GClijst.append(x.getGC())

    i = (GClijst.index(max(GClijst)))
    
    print('Header van de sequentie:','\n',headerLijst[i],'\n')
    print('Het hoogste GC% van het bestand:',max(GClijst))
    print('Het bijbehorende transcript:', dnaLijst[i].getTranscript())
    print('De lengte van het de sequentie:', dnaLijst[i].getLength())
    print('Het eiwit van de sequentie:', dnaLijst[i].getTranslation())
    #print(dnaLijst[i].getSeq())

    #print(dnaLijst)
    #print([x.getGC()for x in dnaLijst])
    #print(dnaLijst[0].getGC())
    
    
    
main()

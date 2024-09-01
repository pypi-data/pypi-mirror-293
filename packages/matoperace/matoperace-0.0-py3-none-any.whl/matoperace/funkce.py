from copy import deepcopy
from decimal import Decimal
import math
import fractions

def NaZlomky(a):
    for radek in a:
        for i in range(len(radek)):
            radek[i] = fractions.Fraction(Decimal(str(radek[i])))

def NaCisla(a):
    for i in range(len(a)):
        a[i] = list(map(float, a[i]))
def SkalS(u, v):
    x = 0
    for i in range(len(u)):
        x += u[i] * v[i]
    return x

def ZaokMat(a, přesnost):
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] = round(a[i][j], přesnost)
    return a

def SoucetMat(a, b):
    c = deepcopy(a)
    if type(a[0]) == list:
        for i in range(len(a)):
            for j in range(len(a[0])):
                c[i][j] += b[i][j]
    else:
        for i in range(len(a)):
            c[i] += b[i]
    return c

def NasMat(a, b):
    c = []
    for i in range(len(a)):
        c.append([])
        for j in range(len(b[0])):
            x = 0
            for k in range(len(b)):
                x += a[i][k] * b[k][j]
            c[i].append(x)
    return c

def NasSkal(t, a):
    b = deepcopy(a)
    if type(a[0]) == list:
        for i in range(len(a)):
            for j in range(len(a[0])):
                b[i][j] *= t
    else:
        for i in range(len(a)):
            b[i] *= t
    return b

def Transpozice(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def Determinant(vstup):
    danaMatice = deepcopy(vstup)
    NaZlomky(danaMatice)
    sign = 1
    for i in range(len(danaMatice)):
        if danaMatice[i][i] == 0:
            for j in range(i + 1, len(danaMatice)):
                if danaMatice[j][i] != 0:
                    danaMatice[i], danaMatice[j] = danaMatice[j], danaMatice[i]
                    sign *= -1
                    break
        if danaMatice[i][i] == 0:
            return 0
        for j in range(i + 1, len(danaMatice)):
            t = danaMatice[j][i] / danaMatice[i][i]
            for k in range(i, len(danaMatice)):
                danaMatice[j][k] -= (danaMatice[i][k] * t)
    det = 1
    for i in range(len(danaMatice)):
        det *= danaMatice[i][i]
    return round(float(det), 12)

def LURozklad(a):
    pMatice = [[0 if j != i else 1 for j in range(len(a))] for i in range(len(a))]
    lMatice = deepcopy(pMatice)
    uMatice = deepcopy(a)
    NaZlomky(uMatice)
    permutace = False
    for i in range(len(uMatice)):
        if uMatice[i][i] == 0:
            permutace = True
            for j in range(i + 1, len(uMatice)):
                if uMatice[j][i] != 0:
                    uMatice[i], uMatice[j] = uMatice[j], uMatice[i]
                    pMatice[i], pMatice[j] = pMatice[j], pMatice[i]
                    break
        if uMatice[i][i] == 0:
            print("Zadaná matice je singulární – LU rozklad neexistuje")
            return None
        for j in range(i + 1, len(uMatice)):
            t = uMatice[j][i] / uMatice[i][i]
            lMatice[j][i] = t
            for k in range(i, len(uMatice)):
                uMatice[j][k] -= (uMatice[i][k] * t)
    NaCisla(uMatice)
    NaCisla(lMatice)
    if permutace:
        return lMatice, uMatice, pMatice
    return lMatice, uMatice

def QRRozklad(vstup):
    danaMaticeTransp = Transpozice(vstup)
    rMatice = [[0 for _ in danaMaticeTransp] for _ in danaMaticeTransp]
    onBaze = []
    lzSloupcu = 0
    for i in (iterSeznam := [n for n in range(len(danaMaticeTransp))]):
        ogProjekce = [0 for _ in danaMaticeTransp[0]]
        for j in range(i):
            ogProjekce = SoucetMat(ogProjekce, NasSkal(SkalS(onBaze[j], danaMaticeTransp[i]), onBaze[j]))
            rMatice[j][i + lzSloupcu] = SkalS(onBaze[j], danaMaticeTransp[i])
        kolVektor = SoucetMat(danaMaticeTransp[i], NasSkal(-1, ogProjekce))
        if abs(SkalS(kolVektor, kolVektor)) < 1e-13:
            rMatice.pop(i)
            danaMaticeTransp.pop(i)
            for k in iterSeznam:
                iterSeznam[k] -= 1
            lzSloupcu += 1
            continue
        onBaze.append(NasSkal(1 / math.sqrt(SkalS(kolVektor, kolVektor)), kolVektor))
        rMatice[i][i + lzSloupcu] = math.sqrt(SkalS(kolVektor, kolVektor))
    qMatice = Transpozice(onBaze)
    return ZaokMat(qMatice, 12), ZaokMat(rMatice, 12)

def Cramer(vstup):
    matSoustavyTransp = Transpozice(vstup)
    vektorPS = matSoustavyTransp.pop()
    hlDet = Determinant(matSoustavyTransp)
    if hlDet == 0:
        print("Matice soustavy je singulární a tuto metodu nelze použít")
        return None
    reseni = []
    for i in range(len(matSoustavyTransp)):
        pomocnaMat = deepcopy(matSoustavyTransp)
        pomocnaMat[i] = vektorPS
        reseni.append(Determinant(pomocnaMat) / hlDet)
    return reseni

def GaussJorEliminace(vstup):
    danaMatice = deepcopy(vstup)
    NaZlomky(danaMatice)
    singularni = False
    lzSloupců = 0
    volnéP = []
    for i in range(len(danaMatice)):
        if danaMatice[i - lzSloupců][i] == 0:
            for j in range(i - lzSloupců + 1, len(danaMatice)):
                if danaMatice[j][i] != 0:
                    danaMatice[i - lzSloupců], danaMatice[j] = danaMatice[j], danaMatice[i - lzSloupců]
                    break
        if danaMatice[i][i] == 0:
            singularni = True
            lzSloupců += 1
            volnéP.append(i)
            continue
        for j in range(len(danaMatice)):
            if j != i - lzSloupců:
                danaMatice[j] = SoucetMat(danaMatice[j], NasSkal(-1 * (danaMatice[j][i] / danaMatice[i - lzSloupců][i]), danaMatice[i - lzSloupců]))
    reseni = []
    if not singularni:
        for i in range(len(danaMatice)):
            reseni.append(float(danaMatice[i][-1] / danaMatice[i][i]))
        for i in range(len(danaMatice), len(danaMatice[0]) - 1):
            reseni.append(0)
        return reseni
    for i in range(lzSloupců):
        if danaMatice[-(i + 1)][-1] != 0:
            print("Soustava nemá řešení.")
            return None
    j = 0
    for i in range(len(danaMatice)):
        if i in volnéP:
            reseni.append(0)
            j += 1
            continue
        reseni.append(float(danaMatice[i - j][-1] / danaMatice[i - j][i]))
    return reseni

def LinearniRegrese(vstup):
    puvMatice = []
    puvMatice.append([vstup[i][0] for i in range(len(vstup))])
    puvMatice.append([1 for _ in vstup])
    puvVektor = [vstup[i][1] for i in range(len(vstup))]
    vysMatice = NasMat(puvMatice, Transpozice(deepcopy(puvMatice)))
    vysVektor = NasMat(puvMatice, Transpozice([puvVektor]))
    vysVektor = Transpozice(vysVektor)
    vysMatice.append(vysVektor[0])
    return Cramer(Transpozice(vysMatice))
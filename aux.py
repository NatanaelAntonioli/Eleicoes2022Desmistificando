def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def modelo_urna(numero):

    numero = int(numero)
    
    if numero >= 999500 and numero <= 1220500:
        return 2009
    elif numero >= 1220501 and numero <= 1345500:
        return 2010
    elif numero >= 1368501 and numero <= 1370500:
        return 2011
    elif numero >= 1600000 and numero <= 1650000:
        return 2011
    elif numero >= 1650001 and numero <= 1701000:
        return 2013
    elif numero >= 1750000 and numero <= 1950000:
        return 2015
    elif numero >= 2000000 and numero <= 2250000:
        return 2020
    else:
        return 1000
 






from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

@csrf_exempt
def encryptPage(req):
    temp = loader.get_template('index.html')
    

    #Only choices that aren't divisible by 3 are in the array
    ar = []
    for i in range(1, 27):
        if i % 3 != 0:
            ar.append(i)
    return HttpResponse(temp.render({'request' : req, 'ar' : ar, 'result' : None}));

@csrf_exempt
def encrypt(req):
    temp = loader.get_template('index.html')
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "#This is the set of all characters that can be encrypted
    pt = req.POST.get('plainText')
    a = int(req.POST.get('a'))
    b = int(req.POST.get('b'))

    enc = ''#The encryption text will be saved into this variable

    for c in pt:
        ch = ((a * al.index(c)) + b) % len(al)# The equation is [y = ([a * x] + b) MOD m]
        enc += al[ch]#After encrypting the character it's added to the string
    
    #Just making the choices array again
    ar = []
    for i in range(1, 27):
        if i % 3 != 0:
            ar.append(i)

    return HttpResponse(temp.render({'request' : req, 'ar' : ar, 'result' : 'Encrypted: ' + enc + ', A key: ' + str(a) + ', B key: ' + str(b)}));

@csrf_exempt
def decrypt(req):
    temp = loader.get_template('index.html')
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "#This is the set of all characters that can be decrypted
    et = req.POST.get('encText')
    a = int(req.POST.get('a'))
    b = int(req.POST.get('b'))
    dec = ''#Decrypted text will be stored here

    inv_a_mod_m = modular_inverse(a, len(al))#Using the function modular_inverse we get inverse(a) MOD m
    for c in et:
        ch = (inv_a_mod_m * (al.index(c) - b)) % len(al)# The equation is [x = (inverse(a) * [y - b]) MOD m] 
        dec += al[ch]

    #Just making the choices array again
    ar = []
    for i in range(1, 27):
        if i % 3 != 0:
            ar.append(i)
            
    return HttpResponse(temp.render({'request' : req, 'ar' : ar, 'result' : 'Decrypted: ' + dec + ', A key: ' + str(a) + ', B key: ' + str(b)}));

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    return x % m


        
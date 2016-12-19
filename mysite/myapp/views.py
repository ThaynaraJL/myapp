# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request,'myapp/index.html')

def geocoding(request):
    return render(request,'myapp/geocoding-reverse.html')

    
def processar(request):
    if request.method == 'POST':
        pontos = request.POST.get('pontos')
        n_ponto = request.POST.get('n_ponto')
        
        pontos = pontos.replace(","," ")
        pontos = pontos.split(")")
        import psycopg2
        global cur

        conn = psycopg2.connect("\
            dbname='Detrans_dw'\
            user='postgres'\
            host='localhost'\
            password='root'\
        ")
        cur = conn.cursor()
        criar_poligono=""
        i=0
        p_ponto=""
        for p in pontos:
            if i==0:
                p_ponto = p_ponto + p
            if len(pontos)-1==i:
                criar_poligono=criar_poligono+p+p_ponto
            else:
                criar_poligono=criar_poligono+p+","

            i += 1
            
        criar_poligono = criar_poligono.replace("(","")

        cur.execute("INSERT INTO consulta(nome,local) VALUES('%s',st_geometryfromtext('POLYGON((%s))',4326))"%(n_ponto,criar_poligono))
        conn.commit()
        return render(request,'myapp/processa.html', {'criar_poligono': criar_poligono, 'pontos':pontos })
		#return criar_poligono
    
    else:
        return render(request,'myapp/index.html')

def compara(request):

    import psycopg2
    global cur

    conn = psycopg2.connect("\
        dbname='Detrans_dw'\
        user='postgres'\
        host='localhost'\
        password='root'\
    ")
    cur = conn.cursor()
    cur.execute("SELECT  MAX(chave_tec) FROM infracao")
    res = cur.fetchone()
    n_infracao = res[0]

    l=[]
    while n_infracao > 0:
        cur.execute("SELECT ST_INTERSECTS((SELECT ST_ASTEXT(local) FROM consulta ORDER BY id_consulta DESC LIMIT(1)),(SELECT  ST_ASTEXT(localizacao) FROM infracao WHERE chave_tec = %d))"%n_infracao)
        res_1 = cur.fetchone()
        intersects = res_1[0]
        if intersects == True:
            cur.execute("SELECT ST_ASTEXT(localizacao) FROM infracao WHERE chave_tec = %d" %n_infracao)
            res_2 = cur.fetchone()
            local_infracao = res_2[0]
            l.append(local_infracao)
            
        n_infracao -=1

    l_coord=[]
    for i in l:
        pontos = i[6:-1]
        l_coord.append(pontos)

    #print(l_coord)
    return render(request,'myapp/recebepontos.html', {'l_coord': l_coord})


def style(request):
    return render(request,'myapp/style.css')
    
def jquery(request):
    return render(request,'myapp/jquery-1.4.2.min.js')
    
def poligono(request):
    return render(request,'myapp/poligono.min.js')

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
        dt_inicio= request.POST.get('data_inicio')
        dt_fim = request.POST.get('data_fim')
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

        #dd/mm/aaaa
        #YYYY/MM/DD

        cur.execute("INSERT INTO consulta(nome,local,data_inicial,data_final) VALUES('%s',st_geometryfromtext('POLYGON((%s))',4326),'%s','%s')"%(n_ponto,criar_poligono,dt_inicio,dt_fim))
        conn.commit()
        return render(request,'myapp/processa.html', {'criar_poligono': criar_poligono, 'pontos':pontos, 'dt_ini':dt_inicio,'dt_fim':dt_fim })
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
    cur.execute("SELECT incao.chave_tec FROM infracao incao, dataperiodo dt where incao.dataperiodo_id = dt.chave_data and dt.datacomp between '31/05/2015' and '01/12/2015'")
    resul_consulta_data = cur.fetchall()
    

    l={}
    for resultado in resul_consulta_data:
        n_infracao = resultado[0]
        cur.execute("SELECT ST_INTERSECTS((SELECT ST_ASTEXT(local) FROM consulta ORDER BY id_consulta DESC LIMIT(1)),(SELECT  ST_ASTEXT(localizacao) FROM infracao WHERE chave_tec = %d))"%n_infracao)
        res_1 = cur.fetchone()
        intersects = res_1[0]
        if intersects == True:
            cur.execute("SELECT ST_ASTEXT(localizacao),chave_tec FROM infracao WHERE chave_tec = %d" %n_infracao)
            res_2 = cur.fetchone()
            local_infracao = res_2[0]
            id_infracao = res_2[1]
            l[id_infracao]= local_infracao
            
    if l:
        coordenadas=[]
        d_coord={}
        for i in l:
            pos= l[i]
            #POINT(0 70)
            d_coord[i] = pos[6:-1] #obtem os valores que estão entre parênteses
            coordenadas.append(d_coord[i])

        return render(request,'myapp/recebepontos.html', {'d_coord': d_coord, 'l_coord':coordenadas})
    else:
        return render(request,'myapp/mensagem.html')

def exibeinfracoes(request):

    import psycopg2
    global cur

    conn = psycopg2.connect("\
        dbname='Detrans_dw'\
        user='postgres'\
        host='localhost'\
        password='root'\
    ")
    cur = conn.cursor()
    cur.execute("SELECT incao.chave_tec FROM infracao incao")
    resul = cur.fetchall()
    

    l={}
    for resultado in resul:
        n_infracao = resultado[0]
        
        cur.execute("SELECT ST_ASTEXT(localizacao) FROM infracao WHERE chave_tec = %d group by(localizacao)" %n_infracao)
        res_2 = cur.fetchone()
        local_infracao = res_2[0]
        id_infracao = n_infracao
        l[id_infracao]= local_infracao
            

    coordenadas=[]
    d_coord={}
    for i in l:
        pos= l[i]
        #POINT(0 70)
        d_coord[i] = pos[6:-1] #obtem os valores que estão entre parênteses
        coordenadas.append(d_coord[i])

    return render(request,'myapp/exibetodos.html', {'d_coord': d_coord, 'l_coord':coordenadas})



def style(request):
    return render(request,'myapp/style.css')
    
def jquery(request):
    return render(request,'myapp/jquery-1.4.2.min.js')
    
def poligono(request):
    return render(request,'myapp/poligono.min.js')

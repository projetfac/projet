#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json
from flask import Flask,request,redirect

app = Flask(__name__)
app._static_folder = os.path.abspath("./")

@app.route('/') # Pour renvoyer la page HTML
def index():
    print('/')
    if os.path.isfile("client_ol.html") :
        print("client_ol.html accessible")
        return app.send_static_file("client_ol.html")
    return "client_ol.html non accessible"

@app.route('/css') # Pour renvoyer la page HTML
def css():
    print('/css')
    return app.send_static_file("aaa.css")


@app.route('/<fichier>') # Pour renvoyer les codes JavaScript...
def fichier(fichier):
    print('/'+fichier)
    if os.path.isfile(fichier) :
        print(fichier, "accessible")
        return app.send_static_file(fichier)
    return fichier+" non accessible"

@app.route('/handle_datar')
def handle_datar():
    args = request.args
    print(args,args.get('theme'),args.get('categorie'))
    return redirect("/handle_datar/theme/"+args.get('theme')+"/categorie/"+args.get('categorie'), code=302)

@app.route('/handle_datar/theme/<value1>/categorie/<value2>')
def handle_datar_jolie_url(value1,value2):
    return app.send_static_file("client_ol.html")


@app.route("/json/handle_datar/theme/<value1>/categorie/<value2>") #le parametre theme est par exemple "Ecoles" ou "Restauration"...,le parametre categorie est par exemple "ecoles primaires" ou "bar"
def renvoie_marqueurs(value1,value2):
    
    listePI = [] # la liste qui sera renvoyee au navigateur
    if os.path.isdir("PI/"+value1) :
        nameoffile = os.listdir("PI/"+value1)
        with open("PI/"+value1+"/"+nameoffile[0],encoding ="utf-8") as json_file:
            data = json.load(json_file)

        

        for element in data["features"]:
            #Puisque les fichiers .json ou .geojson ne sont pas similaires en en tout point il faux au préalable savoir ou chercher ce qu'on veux chercher dans quel fichiers par exemple
            #le nom d'une ecole sera dans element["properties"]["libel"] mais le nom d'un bar/restaurant... sera element["properties"]["name"]
            nomvariable=""
            if value1=="Affichage_Panneaux":
                #on enleve les espaces de part et d'autre, puis on remplace les espaces a l'interieur par _ car une url ne dois pas comporter d'espace.
                nomvariable=element["properties"]["support"].strip()
                nomvariable=nomvariable.replace(" ", "_")
                name=""
            elif value1=="Ecoles":
                nomvariable=element["properties"]["delta_ssca"].strip()
                nomvariable=nomvariable.replace(" ", "_")
                name=element["properties"]["libel"]
            elif value1=="Restauration":
                nomvariable=element["properties"]["amenity"].strip()
                nomvariable=nomvariable.replace(" ", "_")
                name=element["properties"]["name"]

            latitude=element["geometry"]["coordinates"][1]
            longitude=element["geometry"]["coordinates"][0]

            if value2!="":
                if value2==nomvariable:
                    if name!="":               
                        listePI.append([name,latitude,longitude]) 
                    #redondant mais pas grave, ceci sera tjrs vrai en bas
                    elif nomvariable!="":
                        listePI.append([nomvariable,latitude,longitude])


    
    print(listePI,"debug1")
    #en dessous ce sont des tests pour debugger
    #listePI=[[elo,1.43,3.87 marche aussi],[]]
    #dataa =[{0: "lelo",1:43.612275 ,2:3.873584},{0: "ilu",1:43.618286 ,2:3.881923}]
    return json.dumps(listePI)





@app.route("/jsonn/PI/<theme>") #le parametre theme est par exemple "Ecoles" ou "Restauration"
def renvoie_categories(theme):
    listePI = [] # la liste qui sera renvoyee au navigateur
    if os.path.isdir("PI/"+theme) :
        nameoffile = os.listdir("PI/"+theme)

        with open("PI/"+theme+"/"+nameoffile[0],encoding ="utf-8") as json_file:
            data = json.load(json_file)

        
        for element in data["features"]:
            #Puisque les fichiers .json ou .geojson ne sont pas similaires en en tout point il faux au préalable savoir ou chercher ce qu'on veux chercher dans quel fichiers par exemple
            #le nom d'une ecole sera dans element["properties"]["libel"] mais le nom d'un bar/restaurant... sera element["properties"]["name"]
            nomvariable=""
            if theme=="Affichage_Panneaux":
                nomvariable=element["properties"]["support"].strip()
                nomvariable=nomvariable.replace(" ", "_")
            elif theme=="Ecoles":
                nomvariable=element["properties"]["delta_ssca"].strip()
                nomvariable=nomvariable.replace(" ", "_")
            elif theme=="Restauration":
                nomvariable=element["properties"]["amenity"].strip()
                nomvariable=nomvariable.replace(" ", "_")

            if nomvariable!="":
                if nomvariable not in listePI:
                    listePI.append(nomvariable) 
    dataa =[]
    print(listePI,"folk")
    for i,elt in enumerate(listePI):
        #print(i,elt,"debug2")
        #Attention il peux y avoir des comportement bizarres avec les dicts, si tu copies un dict dans une liste prend en compte le fait que c'est une reference a l'objet(le dict).
        #tu peux sois faire une copie profonde ou superficielle
        dicooo={}
        dicooo[0]=elt
        #print(dicooo,"debug3")
        dataa.append(dicooo)
        #print(dataa)
    print("debug4",dataa,listePI)
    return json.dumps(dataa)    




@app.route("/delete",methods = ['POST']) 
def delete():
    theme=request.form['theme']
    latitudeuser=request.form['latitude']
    longitudeuser=request.form['longitude']

    if os.path.isdir("PI/"+theme) :#pense a ajouter un msg si ce n'est pas un dir,on aurait pu utiliser le message flashing mais il faux utiliser render_template. Tant pis.
        nameoffile = os.listdir("PI/"+theme)

        print(nameoffile[0],"debug5")
        with open("PI/"+theme+"/"+nameoffile[0],encoding ="utf-8") as f:
            data = json.load(f)

        
        for (i,dicoelement) in enumerate(data["features"]):
            latitude=dicoelement["geometry"]["coordinates"][1]
            longitude=dicoelement["geometry"]["coordinates"][0]
            print("debug6",type(latitude),type(latitudeuser),type(longitude),type(longitudeuser))
            #Il faux appliquer la fonction str()  car dans le json le type est float, donc on convertit dans le meme type que ce que le html form envoie
            if(str(latitude)==latitudeuser and str(longitude)==longitudeuser):
                print("debug7",data["features"][i])

                data["features"].pop(i)

        print(data["features"])

        with open("PI/"+theme+"/"+nameoffile[0], 'w',encoding ="utf-8") as f:
            #difference entre dump et dumps: dumps = dump string, utilise dump quand tu ecris dans un fichier.
            json.dump(data, f)




    
    return app.send_static_file("client_ol.html")

@app.route("/add",methods = ['POST']) 
def add():
    theme=request.form['theme']
    categorie=request.form['categorie']
    name=request.form['name']
    latitude=request.form['latitude']
    longitude=request.form['longitude']

    if os.path.isdir("PI/"+theme) :#pense a ajouter un msg si ce n'est pas un dir,on aurait pu utiliser le message flashing mais il faux utiliser render_template. Tant pis.
        nameoffile = os.listdir("PI/"+theme)
        #Puisque les fichiers .json ou .geojson ne sont pas similaires en en tout point il faux au préalable savoir ou chercher, ces dictionnaires indiquent ces informations.
        dicoresspondancestheme={"Restauration":"amenity","Ecoles":"delta_ssca","Affichage_Panneaux":"support"}
        dicoresspondancesname={"Restauration":"name","Ecoles":"libel","Affichage_Panneaux":"name"}




        try:
            float(longitude)
            float(latitude)
        except ValueError:
            #ne pas faire confiance aux donnees que l'utilisateur input
            print("longitude et/ou latitude ne peuvent pas etre converties en float, l'utilisateur n'a pas ecrit des nombres")
            return app.send_static_file("client_ol.html")


        entrynormalise= { "type": "Feature", "properties": { dicoresspondancesname[theme]:name, dicoresspondancestheme[theme]:categorie}, "geometry": { "type": "Point", "coordinates": [ longitude, latitude ] } }

        print(nameoffile[0],"debug8")
        with open("PI/"+theme+"/"+nameoffile[0],encoding ="utf-8") as f:
            data = json.load(f)

        data["features"].append(entrynormalise)

        with open("PI/"+theme+"/"+nameoffile[0], 'w',encoding ="utf-8") as f:
            #difference entre dump et dumps: dumps = dump string, utilise dump quand tu ecris dans un fichier.
            json.dump(data, f)


    return app.send_static_file("client_ol.html")

@app.route("/modify",methods = ['POST']) 
def modify():
    theme=request.form['theme']
    ancienlatitude=request.form['ancienlatitude']
    ancienlongitude=request.form['ancienlongitude']

    name=request.form['name']
    latitudeuser=request.form['latitude']
    longitudeuser=request.form['longitude']



    if os.path.isdir("PI/"+theme) :#pense a ajouter un msg si ce n'est pas un dir,on aurait pu utiliser le message flashing mais il faux utiliser render_template. Tant pis.
        nameoffile = os.listdir("PI/"+theme)

        dicoresspondancesname={"Restauration":"name","Ecoles":"libel","Affichage_Panneaux":"name"}
        print(nameoffile[0],"debug9")


        try:
            float(longitudeuser)
            float(latitudeuser)
        except ValueError:
            #ne pas faire confiance aux donnees que l'utilisateur input
            print("longitude et/ou latitude ne peuvent pas etre converties en float, l'utilisateur n'a pas ecrit des nombres")
            return app.send_static_file("client_ol.html")



        with open("PI/"+theme+"/"+nameoffile[0],encoding ="utf-8") as f:
            data = json.load(f)

        print("debug10")
        for (i,dicoelement) in enumerate(data["features"]):
            latitude=dicoelement["geometry"]["coordinates"][1]
            longitude=dicoelement["geometry"]["coordinates"][0]
            #print("debug11",type(latitude),type(ancienlatitude),type(longitude),type(ancienlongitude))
            #Il faux appliquer la fonction str()  car dans le json le type est float, donc on convertit dans le meme type que ce que le html form envoie
            if(str(latitude)==ancienlatitude and str(longitude)==ancienlongitude):
                print("debug12",data["features"][i])
                
                relevantkey=dicoresspondancesname[theme]
                print("debug13",relevantkey)
                data["features"][i]["properties"][relevantkey]=name
                data["features"][i]["geometry"]["coordinates"][1]=latitudeuser
                data["features"][i]["geometry"]["coordinates"][0]=longitudeuser
                print(data["features"][i])



        with open("PI/"+theme+"/"+nameoffile[0], 'w',encoding ="utf-8") as f:
            #difference entre dump et dumps: dumps = dump string, utilise dump quand tu ecris dans un fichier.
            json.dump(data, f)

    return app.send_static_file("client_ol.html")



app.run()

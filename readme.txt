 'flashbot_scrapy.py' :
 
Bot se connectant à une URL puis executant une requête par élément dans le 'thesaurus'. Enregistre les résultats dans une DB MongoDB.
Variables de configuration dans le code source:
    start_urls : URL à laquelle se connecte le bot
    allowed_domains : Domaine auquel se connecte le bot
    thesaurus : Liste de mo-clés recherchés.
    client = MongoClient('localhost', 27017) : Adresse et port de l'instance MongoDB
    db = client['flashbot'] : Nom de la DB utilisée dans MongoDB
    collection = db['jobsearch'] : Nom de la collection utilisée dans MongoDB

Le bot se lance avec la commande : 
    scrapy runspider flashbot_scrapy.py
  
  
'flashbot_flask.py'

Serveur Web autorisant des requêtes sur la DB MongoDB depuis une page Web et affichant les résultats sur une deuxième page.
Variables de configuration dans le code source:
    client = MongoClient('localhost', 27017) : Adresse et port de l'instance MongoDB
    db = client['flashbot'] : Nom de la DB utilisée dans MongoDB
    collec = db['jobsearch'] : Nom de la collection utilisée dans MongoDB
    
Le serveur se lance avec les commandes suivantes :
    export FLASK_APP=flashbot_flask.py
    flak run
(NOTE : l'export n'est à executer qu'une seule fois)

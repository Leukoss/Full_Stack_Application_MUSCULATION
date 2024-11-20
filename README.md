# Coach est là - Application full stack data

Ce readme a pour objectif de présenter le sujet choisi, ainsi que les 
difficultés rencontrées. On retrouvera aussi un court guide afin de
faciliter l'installation et le lancement de l'application

## Sujet - Application d'enregistrement des performances de musculation

Cette application a pour objectif d'enregistrer la progression des 
personnes pratiquant la musculation. Lors de sa séance, l'utilisateur 
peut donc saisir ses performances dans l'application afin de pouvoir 
les consulter par la suite. Les données récoltées permettent d'établir
un graphique retraçant l'évolution des performances sur un 
exercice spécifique.

L'application possède deux volets principaux:
* Profil : informations globales sur l'utilisateur et ensemble des données relatives aux exercices
* Exercice : ajout de nouvelles performances et ajout de nouveaux exercices

Pour accéder aux données concernant un certain utilisateur, il faut d'abord se créer un compte dans la page prévue à cet effet. Une fois le compte crée, l'utilisateur est libre de se connecter et de se déconnecter.

### Profil

La page profil est composé d'une section regroupant l'ensemble des exercices et des informations sur l'utilisateur.

![image](/static/images/capture_1.PNG "Capture d'écran profil")

Lorsque l'utilisateur sélectionne un des exercice, ses performances les plus récentes vont être représentées sous forme de tableau.

![image](/static/images/capture_2.PNG "Capture d'écran profil")

L'utilisateur peut également analyser ses performances à l'aide d'un graphique en cliquant sur *voir plus*.

### Exercice

Cette section contient deux sections. Une section qui liste l'ensemble des exercices. L'autre section permet de rajouter des exercices dans la liste des exercices et d'enregister des performances liées à des exercices.

![image](/static/images/capture_3.PNG "Capture d'écran profil")

Ajout de nouveaux exercices pour enregistrer des nouvelles performances.

![image](/static/images/capture_4.PNG "Capture d'écran profil")

Ajout de nouvelles performances qui pourront être comparées à celle enregistrées précedemment.

## Difficultés Rencontrées

La première grosse difficulté a été d'adopter Django. Il s'agit d'un framework complet mais complexe doté de plusieurs fichiers qui peuvent parraître difficile d'accès. Cependant après une brève période d'adaptation, ce framework est parfaitement adapté à l'application que l'on a développée.

Les principaux obstacles dans ce projet ont été les problèmes liés à la base de données, aux modèles, aux back-end de manière générale. La récupération des données dans un format json pour les séries et les répétitions était également compliqué.

Enfin, l'affichage du graphique représentait une difficulté supplémentaire surtout pour représenter l'ensemble des sets à la fois sur un même graphique.

## Guide d'Installation et de Lancement de l'Application

Il faut se rendre sur : https://github.com/Leukoss/Full_Stack_Application_MUSCULATION/tree/apo

1. Récupérer/cloner le projet dans un répertoire donné

2. Ouvrir Docker

3. Ouvrir deux terminals dans le répertoire du projet
-dans le premier terminal  : **docker-compose up --build**
-dans le second : **docker-compose exec web python manage.py migrates**

4. Se rendre sur : http://localhost:8080/

5. Profitez des fonctionalités de Coachella, créer un compte, ajouter des exercices et des performances pour visualiser les graphiques.

END
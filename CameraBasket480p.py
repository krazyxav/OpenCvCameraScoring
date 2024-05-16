# import the opencv library: pip install opencv-python
# import the numpy library: pip install numpy
# import the math library: pip install math

import cv2
import numpy as np
#import math
import time
import threading

# 0 : première camera dans celles trouvées par la librairie
# Pb connu sous windows 11: exécuter d'abord le code sous Thonny pour faire
#   reconnaitre l'utilisation de la caméra par les systèmes de sécurité windows
# Ce n'est plus vrai au 19/09/2023

#préparation de la lecture de la vidéo
#récupération du stream de la caméra du raspberry, personnaliser l'adresse IP
vid = cv2.VideoCapture("rtmp://192.168.160.67:1935/live")

#camera 0: première caméra dispo.
#problème rencontré au début: faire tourner le programme avec thonny pour faire reconnaître la camera.
#Après paramétrage python de VS code, OK directment sous VS code.
#exemples d'utilisation de la camera embarquée d'un pc portable,
#ou d'un fichier vidéo

#vid = cv2.VideoCapture(0)
#vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#vid = cv2.VideoCapture("D:/Xavier/Vidéos/videos voiture téléguidée/20141228_113354.mp4",cv2.CAP_FFMPEG)
#vid = cv2.VideoCapture("D:/Xavier/Vidéos/videos voiture téléguidée/20141228_113354.mp4")
#print(cv2.getBuildInformation())

#formatvidéo
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)

#préaparation de l'enregistrement de la vidéo en mjpeg
out = cv2.VideoWriter('outVid.avi', cv2.VideoWriter_fourcc('M','J','P','G'),10, (720,576))

#global temps_arrete
temps_arrete = True
arret_programme = False

#initialisation du chrono
timer='chrono'

#réglage de la durée de la fraction de match
time_secs =600


def chrono():
    global temps_arrete
    global time_secs
    global vid
    global timer
    global arret_programme
    
    #boucle sans fin
    while(True):
        #déorulement du chrono ou non suivant les appuis de la touche t
        #dans video_globale()
        #affifchage du chrono mm:ss
        if temps_arrete == False :
            if time_secs > 60 :
                mins,secs = divmod(time_secs,60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                time_secs -= 1
                time.sleep(1)
            else :
                if time_secs > 0 :
                    timer = '{:.1f}'.format(time_secs)
                    time_secs -= 0.1
                    time.sleep(0.1)
                else : 
                    timer = '0.0'
        #détection de l'arrêt du programme par appui de la touche q
        #dans video_globale()
        if arret_programme == True:
            break


def video_globale():
    
    global time_secs
    global timer
    global temps_arrete
    global arret_programme

    x=10
    y=10
    w=50
    h=50

    black = (0,0,0)
    white = (255,255,255)

    score_local = 0
    score_visiteur = 0
    equipe_local = "LBA"
    equipe_local = "BCL"

    taille_police = 0.5
    while(True):

        # Capture the video frame
        # by frame

        ret, frame = vid.read()

        cv2.namedWindow('frame') #,cv2.WINDOW_NORMAL)

        #cv2.resizeWindow('frame',(600,600))
    
        #text=str(frame.shape[0])
                
        #ajout de rectangles, a mettre avant les textes pour ne pas les recouvrir
        #cv2.rectangle(frame, (50,150), (100,160), white,-1)
        
        #textes
        #cv2.putText(frame, text,(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, white,1)
        #exemples d'insertion de texte
        cv2.putText(frame,'taille police 12345 '+str(taille_police),(50,50),cv2.FONT_HERSHEY_PLAIN, taille_police,white,1)
        cv2.putText(frame,time.asctime(), (50,70),cv2.FONT_HERSHEY_PLAIN, 2,white,1)
        #pour test valeur arrêt ou non du chrono
        #cv2.putText(frame,str(temps_arrete), (50,90),cv2.FONT_HERSHEY_PLAIN, 2,white,1)

        #insertion du chrono
        cv2.putText(frame,timer,(250,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)

        #ajout des scores
        cv2.putText(frame,str(score_local),(200,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)
        cv2.putText(frame,str(score_visiteur),(400,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)


        #ajout du frame au fichier vidéo
        out.write(frame)
        #mise a jour
        cv2.imshow('frame', frame)
        
        #surveillance des touches de clavier
        touche_frappee = cv2.waitKey(1) & 0xFF

        if touche_frappee == ord('q'):
            arret_programme = True
            break

        #variation des tailles de polices par les touches + et -
        if touche_frappee == ord('+'):
            taille_police += 0.5
            
        if touche_frappee == ord('-'):
            taille_police -= 0.5

        if taille_police <= 0:
            taille_police = 0.5

        #gestion des scores
        if touche_frappee == ord('l'):
            score_local +=1
        if touche_frappee == ord('L'):
            score_local -=1
        if touche_frappee == ord('v'):
            score_visiteur +=1
        if touche_frappee == ord('V'):
            score_visiteur -=1

        #arrêt ou mise en route du chrono par appui touche t
        if touche_frappee == ord('t'):
            temps_arrete = not temps_arrete
 
#déroulement simultané du chrono et de la capture de la vidéo
th1=threading.Thread(target=chrono)
th2=threading.Thread(target=video_globale)

th1.start()
th2.start()

th1.join()
th2.join()

print("Arrêt programme")
# Sortie du programme
vid.release()
out.release()
# Destroy all the windows
cv2.destroyAllWindows()

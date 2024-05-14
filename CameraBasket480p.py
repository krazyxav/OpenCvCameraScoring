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
#récupération du stream de la caméra du raspberry
vid = cv2.VideoCapture("rtmp://192.168.160.67:1935/live")

#vid = cv2.VideoCapture(0)
#vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#vid = cv2.VideoCapture("D:/Xavier/Vidéos/videos voiture téléguidée/20141228_113354.mp4",cv2.CAP_FFMPEG)
#vid = cv2.VideoCapture("D:/Xavier/Vidéos/videos voiture téléguidée/20141228_113354.mp4")
#print(cv2.getBuildInformation())

#formatvidéo
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)

#préaparation de l'enregistrement de la vidéo
out = cv2.VideoWriter('outVid.avi', cv2.VideoWriter_fourcc('M','J','P','G'),10, (720,576))

#global temps_arrete
temps_arrete = True
arret_programme = False

timer='chrono'

#global time_secs
time_secs =600
#mins,secs = divmod(time_secs,60)
#timer = '{:02d}:{:02d}'.format(mins, secs)

def chrono():
    global temps_arrete
    global time_secs
    global vid
    global timer
    global arret_programme
    
    #boucle sans fin
    while(True):

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



        #ajouter gestion de la dernière minute
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
        
        #texte
        #cv2.putText(frame, text,(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, white,1)
        cv2.putText(frame,'taille police 12345 '+str(taille_police),(50,50),cv2.FONT_HERSHEY_PLAIN, taille_police,white,1)
        cv2.putText(frame,time.asctime(), (50,70),cv2.FONT_HERSHEY_PLAIN, 2,white,1)
        cv2.putText(frame,str(temps_arrete), (50,90),cv2.FONT_HERSHEY_PLAIN, 2,white,1)

        cv2.putText(frame,timer,(250,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)
    
        cv2.putText(frame,str(score_local),(200,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)
        cv2.putText(frame,str(score_visiteur),(400,400),cv2.FONT_HERSHEY_PLAIN, 2,white,2)
        
        #rectangles
        #cv2.rectangle(frame, (50,150), (100,160), white,-1)

        #ajout du frame au fichier vidéo
        out.write(frame)
        #mise a jour
        cv2.imshow('frame', frame)
        
        #surveillance des touches de clavier
        touche_frappee = cv2.waitKey(1) & 0xFF

        if touche_frappee == ord('q'):
            arret_programme = True
            break


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

        if touche_frappee == ord('t'):
            temps_arrete = not temps_arrete
 


th1=threading.Thread(target=chrono)
th2=threading.Thread(target=video_globale)

th1.start()
th2.start()

th1.join()
th2.join()

print("Arrêt programme")
# After the loop release the cap object
vid.release()
out.release()
# Destroy all the windows
cv2.destroyAllWindows()
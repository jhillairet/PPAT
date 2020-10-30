# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 16:19:04 2019

@author: PD124182
"""

def smoothlocal(x,window_len=10,window='hanning'):
 import numpy as N
 import pylab as plt
#ne pas dependre d'une toolbox....    
 if N.ndim(x) != 1:
#raise ValueError, "smooth only accepts 1 dimension arrays."
  plt.disp("smooth only accepts 1 dimension arrays.")
 if N.size(x) < window_len:
#raise ValueError, "Input vector needs to be larger than window size."
  plt.disp("Input vector needs to be larger than window size.")

 if window_len<3:
  return x
  
 if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
#raise ValueError, "Window must be 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
  plt.disp("Window must be 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

 s=N.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]

 if window == 'flat': #moving average
  w=N.ones(window_len,'d')
 else:
  w=eval('N.'+window+'(window_len)')
        
 y=N.convolve(w/w.sum(),s,mode='same')
 return y[window_len-1:-window_len+1]
#*********************************************************************
def filterdata(x):
 #import numpy as N
 #import pylab as plt
 import scipy
 from scipy import signal 
#designing a butterworth filter and filtering
 b, a = signal.butter(20, 0.2,btype='low', analog=False)
 sig=signal.lfilter(b,a,x)
 return sig 
#*********************************************************************
def pradwest1(shot,fi=1):
 """%version initiale  29/03/2017
 %function [Prad,Pbulk,Pdiv,Pchan,trad]=pradwest1(shot,fi)
 %on reecrit le programme de calcul de la puissance rayonnée  pour WEST
 %la fonction permet de calculer la puissance rayonnée dans WEST ou Tore
 %Supra, indifferamment.
 %
 %version du 16/11/2017
 %Les tirs  50000 < numchoc <51785 sont corrigés du defaut de
 % numérisation 
 %
 % version du 23/11/2017
 %on rajoute une donnée en sortie, Pchan la puissance rayonnée  sur chaque
 %cone de visée, intégrée toroidalement.
 %
 %version du 28/11/2017
 %on definit une fonction de lissage à l'interieur du programme
 %qui est identique à celle utilisée par JET, fenetre 'hanning', longueur 8
 %car la fonction smooth toolbox matlab standard ecrase trop le signal.
 %le lissage est maintenant identique en matlab et python et les deux
 %programmes donnent exactement le meme resultat.
 %
 %version du 16/01/2018
 %on tient compte de l'inclinaison toroidale des 2 caméras lors du 
 %remontage pour les tirs >50000. le facteur multiplicatif de correction
 %correspondant à 17.5°est 0.954. 
 %
 %version du 23/01/2018
 % on ne sort plus la figure représentant les puissances rayonnées, 
 %ainsi que celle représentant la puissance par voie de mesure.
 %peut etre rétabli si forte demande
 %
  %version du 30/01/2018
 %la représentation des figures devient optionnelle,
 %la syntaxe d'appel de la fonction change
 %              [Prad,Pbulk,Pdiv,Pchan,trad]=pradwest(shot,fi)
 % une valeur de fi=0 annulera la representation des figures.
 %toute autre valeur de fi produira des figures. si aucune valeur n'est
 %rentrée pour fi, il y aura production de figure.
 % le temps passe en relatif.
 %
 %version du 30/08/2018
 %dans cette version, on corrige la puissance rayonnée divertor bas quand
 %on detecte du rayonnement prés du divertor haut. Ceci amène à fournir une
 %donnée supplémentaire, la puissance divertor haut Pdivh, la puissance
 %divertor bas est renommée Pdivb.
 %la syntaxe de la fonction devient:
            [Prad,Pbulk,Pdivb,Pdivh,Pchan,trad]=pradwest(shot,fi)
%
%modif du 14/11/2018
%le calcul de la répartition Pdivh et Pdivb est amélioré
%on change le nom du programme pour la phase de test, la syntaxe devient:
%               [Prad,Pbulk,Pdivb,Pdivh,Pchan,trad]=pradwest1(shot,fi)
% 
%modif du 28/11/2018
on calcule la puissance tombant directement sur le bolometre pour
la base de données IMAs. la syntaxe devient:
           [Prad,Pbulk,Pdivb,Pdivh,Pchan,bolofmas,tbolo,trad]=pradwest1(shot,fi)
% """
 
 
 import pylab as plt
 import numpy as N
 import pywed
 
 
 #plt.close('all')
 
 #declaration des variables
 cg=[];gain=[];therm=[];tcold=[];deltab=[];deltah=[];deltahm=[];bolof=[]
 boloi1=[];Prad=[];A1=[];Si=[];B1=[];A2=[];B2=[]
 Pdivb=[];Pbulk=[];Prad=[];Pchan=[];Pdivh=[]


 #shot=N.int(input('Shot: '))
 #chargement des signaux de bolometrie
 [bolo1,tbolo1]=pywed.tsmat(shot,'DBOLO-GBOLOC1')
 [bolo1,tboloa]=pywed.tsmat(shot,'DBOLO-GBOLOC1','+')
 torigin=N.mean(tboloa[:,0]-tbolo1[:,0])
#chargement des gains
 [gainp1,gaina1]=pywed.tsmat(shot,'DBOLO;Params;BGAINP1','DBOLO;Params;BGAINA1')
#chargement des angles solides
 [omega1,omega2]=pywed.tsmat(shot,'DBOLO;CONFIG_CAM1;SOLIDE','DBOLO;CONFIG_CAM2;SOLIDE')
#chargement etalonnage des bolometres, 1ere colonne, nombre de W/Volts
#2eme colonne constante de refroidissment
 [etal1,etal2]=pywed.tsmat(shot,'DBOLO;CONFIG_CAM1;ETAL','DBOLO;CONFIG_CAM2;ETAL')
#chargement des gains supplementaires (tous a 1)
 [cg1,cg2]=pywed.tsmat(shot,'DBOLO;CONFIG_CAM1;COGAIN','DBOLO;CONFIG_CAM2;COGAIN')
 cg=N.append(cg1,cg2)
#chargement etat des bolometres
 [et1,et2]=pywed.tsmat(shot,'DBOLO;CONFIG_CAM1;ETAT','DBOLO;CONFIG_CAM2;ETAT')

 if shot>50000:
     west=2 #config WEST
     plt.disp('WEST!')
 else:
     if shot<100:
         west=2
         plt.disp('Test Info!')
     else:
         west=1 #cas Tore Supra
         plt.disp('Tore Supra!')

#calcul des gains finaux pour chaque voie, 16 au total
 for ll in range(16):
     a=gainp1[ll]*gaina1[ll]*cg[ll]*64
     gain=N.append(gain,a)
       
 
 #angles solides pour les 16 voies  
 sol=omega1
 for ll in range(8):
     sol=N.append(sol,omega2[ll])
#etat des voies (on=1/off=0) 
 etat=et1   
 for ll in range(8):
    etat=N.append(etat,et2[ll])
#suite à la detection probleme voie 9 (8 EN PYTHON)? cette voie est mise inopérante
 #etat[8]=0
    
#constante thermique en V/Watts
 for ll in range(8):
     a=etal1[ll,0]
     therm=N.append(therm,a) 
 for ll in range(8):
     a=etal2[ll,0]
     therm=N.append(therm,a)
#temps de refroidissement en s
 for ll in range(8):
     a=etal1[ll,1]
     tcold=N.append(tcold,a) 
 for ll in range(8):
     a=etal2[ll,1]
     tcold=N.append(tcold,a)
 #le signal bolo des 16 voies avec le temps associé 
 bolo=bolo1
 nt=len(bolo) 
 tbolo=tbolo1[:,0] 
 
 ss=N.where(tbolo<-6) [0]
#offset  debut du plasma 
 valbase=N.zeros(16)
 for kk in range(16):
   [a,b]=N.histogram(bolo[ss,kk],1000)
   #jj=plt.find(a==max(a))
   jj=N.where(a==N.max(a)) [0]
   jj=N.max(jj)
   if b[jj]<-5.1:
    valbase[kk]=-4.9
   else: 
    valbase[kk]=b[jj] 

#correction du signal du bit defectueux pour les tirs<51785
#il faut rajouter dans ce cas:1.2563  
    if west==2:
#données avant le 20/11/2017
        if shot<51785:
            for kk in range(16):
              #ssw=plt.find(bolo[:,kk]<-5.3)
              ssw=N.where(bolo[:,kk]<-5.3) [0]
              bolo[ssw,kk]=bolo[ssw,kk]+1.2563
           
 tmax=N.max(tbolo)
 ss1=N.where(tbolo>tmax-1) [0]
 #offset fin du plasma 
 valbase1=N.zeros(16) 
 for kk in range(16):
   [a,b]=N.histogram(bolo[ss1,kk],1000)
   #jj=plt.find(a==max(a))
   jj=N.where(a==N.max(a)) [0]
   jj=N.max(jj)
   if b[jj]<-5.1:
    valbase1[kk]=-4.9
   else: 
    valbase1[kk]=b[jj]
       
 #enlevement de la derive      
 for ll in range(16):
     boloi=bolo[:,ll]
     derive=valbase1[ll]-valbase[ll]
     bolo[:,ll]=boloi[:]-N.arange(nt)*derive/nt 
         
 #détection par seuil
 for ll in range(16):
   boloi=bolo[:,ll]
   #kk1=plt.find(boloi<valbase[ll]-0.2)
   kk1=N.where(boloi<valbase[ll]-0.2) [0]
   boloi[kk1]=valbase[ll]
   if len(kk1)>5:
       lvu=ll+1
       plt.disp('noise on channel {}' .format(lvu))

   kk2=N.where(boloi<valbase[ll])[0]
   boloi[kk2]=valbase[ll];
   bolo[:,ll]=boloi;
    
    #enlevement offset initial
 for ll in range(16):
     bolo[:,ll]=bolo[:,ll]-valbase[ll]

#fin de chargement parametres et donnees BOLO*************

#correction gain, etendue de la ligne de visee...  
 calb=20.24#inverse surface detecteur
 bolomas=bolo[:,0:16]-bolo[:,0:16]
 for ll in range(16):
     boloi=bolo[:,ll]
     boloi=boloi*calb/gain[ll]#gain et correction surface detecteur
     
     bolomas[:,ll]=bolo[:,ll]/gain[ll] #pour base de donnees IMAS signal brut
     
     boloi=4000*N.pi*boloi/sol[ll]#normalisation angle solide
     bolo[:,ll]=boloi[:]
     
  #on applique la fonction de transfert pour IMAS pour avoir le signal brut en WATTs
 bolofmas=bolo[:,0:16]-bolo[:,0:16]
 for ll in range(16):     
    bolofmas[:,ll]=((N.gradient(bolomas[:,ll])/N.gradient(tbolo))*tcold[ll]+bolomas[:,ll])/therm[ll] 
    
 #resampling a 1ms
 to=N.arange(N.min(tbolo),N.max(tbolo),1e-3)
 for ll in range(16):
     boloi=bolo[:,ll]
     boloi1=N.interp(to,tbolo,boloi)
     boloi1=smoothlocal(boloi1,8) #lissage défini localement
     bolof=N.append(bolof,boloi1)
     
#signal final traité/normalisé, lissé 
#à multiplier par la pondération de chaque voie 
#pour puissance le long de la ligne de visée (MW)
 bolof=N.reshape(bolof,(N.size(to),16),order='f')

#definition rayon plasma
 if west==2:
     Ro=2.5 #en m   WEST!
 else:
     Ro=2.38 # en m Tore Supra!

#calcul de la fonction de reponse du bolometre
 for ll in range(16):
     bolof[:,ll]=((N.gradient(bolof[:,ll])/N.gradient(to))*tcold[ll]+bolof[:,ll])/therm[ll]
    
#interpolation des voies manquantes
 eta1=etat*1
 if eta1[0]==0:
     bolof[:,0]=bolof[:,1]
     eta1[0]=1
     
 if eta1[15]==0:
     bolof[:,15]=bolof[:,14]
     eta1[15]=1
     
 b=sum(eta1)
 if b!=16:
     for ll in range(1,15):
         if eta1[ll]==0:
             bolof[:,ll]=(bolof[:,ll-1]+bolof[:,ll+1])/2
             lvu=ll+1
             plt.disp('channel {} is interpolated' .format(lvu))


#coeff de ponderation des voies bolometrie déterminés  à partir des programmes 
# 1) largeurtrapezebas.m
# 2) largeur trapezehaut.m

 if west==1:
#largeurtrapezebas, ponderation voies basses
#option grand coté trapeze à la paroi interne (TS)
     deltab =[0.0883,0.0940,0.0949,0.0966,0.0960,0.0952,0.0946,0.0942] 
 else:
#option grand coté trapeze près de la DSMF (WEST)
     deltab=[0.0881,0.0939,0.0934,0.0925,0.0916,0.0916,0.0910,0.0907]
    
#largeurtapezehaut, ponderation voies hautes sans correction recouvrement
 if west==1:
#option grand coté trapeze à la paroi interne (TS)
     deltah =[0.0943,0.0947,0.0952,0.0959,0.0959,0.0954,0.0948,0.0925]
 else:
#option grand coté trapeze près de la DSMF (WEST)     
     deltah=[0.0908,0.0913,0.0915,0.0919,0.0922,0.0951,0.0944,0.0924]
    
#largeurtrapezehaut ponderation voies hautes avec correction recouvrement
 if west==1:
#option grand coté trapeze à la paroi interne (TS)
     deltahm =[0.0352,0.0523,0.0706,0.0842,0.0959,0.0954,0.0948,0.0925]
 else:
#option grand coté trapeze près de la DSMF (WEST)      
     deltahm=[0.0156,0.0435,0.0635,0.0785,0.0922,0.0951,0.0944,0.0924]
    

   
#debut du programme de calcul des  puissances rayonnees
 delta1=N.append(deltab,deltahm)
 delta2=N.append(deltab,deltah)
 
 #facteur de correction angle toroidal cameras 
 if shot>50000:
     cort=0.954 #facteur de correction toroidale
 else:
     cort=1.0 #pas de correction
 
 Prad=bolof[:,0]*delta1[0]
 for ll in range(1,16):
      Si=delta1[ll]*bolof[:,ll]
      Prad=Prad+Si 
 Prad=Prad*2e-2*N.pi*cort*Ro #puissance rayonnee totale!
 
     
 #on evite les puissances negatives
 ss1=N.where(Prad<0) [0]
 Prad[ss1]=0

#calcul puissance rayonnee par cone de visee (16 voies)
 
 for ll in range(16): 
   Ps=bolof[:,ll]*delta2[ll]*2e-2*N.pi*cort*Ro  
   Pchan=N.append(Pchan,Ps)
   
 Pchan=N.reshape(Pchan,(N.size(to),16),order='f')  
 
#les voies interpolées sont mises à zero pour representation graphique
 mm=N.where(etat==0) [0]
 for ll in range(len(mm)):
     Pchan[:,mm[ll]]=Pchan[:,mm[ll]]-Pchan[:,mm[ll]]
     
 #Pchan[:,mm]=0
       
#calcul rapport d'assymetrie du plasma
#bas du plasma
 A1=deltab[3]*bolof[:,3]
 for ll in range(4,6):
     B1=deltab[ll]*bolof[:,ll]
     A1=A1+B1
 ss3=N.where(A1<=0) [0]
 A1[ss3]=1e-3
     
#haut du plasma
 A2=deltah[3]*bolof[:,10]
 for ll in range(4,6):
     B2=deltah[ll]*bolof[:,ll+7]
     A2=A2+B2
 ss3=N.where(A2<=1e-3) [0]
 A2[ss3]=1

#rapport assymetrie bas/haut
 assym1=A1/A2
 
#pas d'assymetrie trop grande ou negative
 ss3=N.where(assym1>=3) [0]
 assym1[ss3]=1
 ss3=N.where(assym1<0) [0]
 assym1[ss3]=1
 
#calcul puissance rayonnee dans le divertor: Pdiv

#bas du tokamak 3 premieres voies
 Si=[]
 P1=bolof[:,0]*delta1[0]
 for ll in range(1,3):
     Si=delta1[ll]*bolof[:,ll]
     P1=P1+Si 
 P1=P1*2e-2*N.pi*cort*Ro
 
#haut du tokamak 3 dernieres voies
 Si=[]   
 P2=bolof[:,13]*delta1[13]
 for ll in range(14,16):
     Si=delta1[ll]*bolof[:,ll]
     P2=P2+Si 
 P2=P2*2e-2*N.pi*cort*Ro
 P2i=P2*1.0
 
 """Ici on teste s'il existe un rayonnement significatif en haut du plasma
 Si c'est le cas,
 il faut corriger le profil en haut du plasma pour calculer la puissance divertor haut. 
 On corrige ensuite la puissance divertor bas.
 Ceci est fait à l'aide d'une méthode histogrammique qui 
 permet une correction en moyenne.
 on a  alors une approximation de la puissance divertor bas plus precise"""
 
 passe=1
 if passe==1:
  #jj1=plt.find(P1<=0)
  jj1=N.where(P1<=0) [0]
  P1[jj1]=0.005
  #jj2=plt.find(P2<=0)
  jj2=N.where(P2<=0) [0]
  P2[jj2]=0.005
  #rb12=P2/P1
 
 
   
 #test niveau du signal
 ld=N.arange(len(to))
 kk3=[kk for kk in ld if to[kk]>0 if to[kk]<10]
 mP1=N.mean(P1[kk3],dtype=N.float32)
 mP2=N.mean(P2[kk3],dtype=N.float32)
# import pdb; pdb.set_trace()
 if N.max([mP1,mP2])>1e-2: 
     ev=1
     plt.disp('sufficient signal to be meaningfull')
 else:
     ev=0
     plt.disp('not enough signal to be meaningfull')
    
 
#correction du profil si presence de rayonnement en haut
 if passe==1: 
   Sig0=bolof[:,13]*delta2[13]
   ff0=N.where(Sig0<0) [0]
   Sig0[ff0]=0
   Sig1=bolof[:,14]*delta2[14]
   ff1=N.where(Sig1<0) [0]
   Sig1[ff1]=0
   Sig2=bolof[:,15]*delta2[15]
   ff2=N.where(Sig2<0) [0]
   Sig2[ff2]=0

   ld=N.arange(len(to)) 
   tests=(bolof[:,7]*delta2[7]+bolof[:,8]*delta2[8])/2
   tests=filterdata(tests)
   
   
   zzz=[kk for kk in ld  if to[kk]>0 if P2[kk]>0.05 if P2[kk]<1 if tests[kk]>0.11]
   if N.size(zzz)>1:
    mz=max(zzz)
   else:
    mz=1   
    
   zzz1=[kk for kk in ld  if to[kk]>0 if P2[kk]<=0.05 if kk<=mz if tests[kk]>0.11]
   if N.size(zzz1)>0:
    [c,d]=N.histogram(Sig1[zzz1]/tests[zzz1],100)
    [e,f]=N.histogram(Sig0[zzz1]/tests[zzz1],100)
    lu=N.arange(len(c))
    lv=N.arange(len(e))
    hh=[kk for kk in lu if c[kk]>0 if d[kk]>0]
    ii=[kk for kk in lv if e[kk]>0 if f[kk]>0]
    uu=N.sum(c[hh]*d[hh])/N.sum(c[hh])
    vv=N.sum(e[ii]*f[ii])/N.sum(e[ii])
    Sig1[zzz]=uu*tests[zzz]
    Sig0[zzz]=vv*tests[zzz]
   
   P2=Sig0+Sig1+Sig2
   plt.disp('radiation profile corrected to take into account radiation at the top')
   P2=P2*2e-2*N.pi*cort*Ro
   
 
#determination de l'assymetrie consideree
#suivant l'appui du plasma
 if N.size(zzz1)>0:   
  Pdivh=P2i-P2
  P3=P2*assym1
  Pdivb=P1-P3
 else:
   Pdivh=P2
   Pdivb=P1
 
 #Pdivb=P1i-P1
  

  
#pas de valeur de Pdiv bas negative
 ssa=N.where(Pdivb<0) [0]
 Pdivb[ssa]=0.0001
 
#pas de valeur de Pdiv haut negative
 ssb=N.where(Pdivh<0) [0]
 Pdivh[ssb]=0.0001
 Pdivhi=Pdivh*1.
 #on discrimine les valeurs basses de pdivh
 ssb=N.where(Pdivh<0.005) [0]
 Pdivh[ssb]=40
 
#recalcul du profil de Prad en haut apres correction histogrammique
 passe2=0
 if passe2!=1:
  gg1=[kk for kk in ld if Pdivh[kk]>0.005 if Pdivh[kk]!=40 if to[kk]>0]
  gg2=[kk for kk in ld if Pdivh[kk]==40 if to[kk]>0]
  if N.size(gg1)>0:
   Pdivhm=N.interp(to,to[gg1],Pdivh[gg1])
   Pdivh=Pdivhm*1.
   Pdivh[gg2]=Pdivhi[gg2]
  else:
   Pdivh=Pdivhi
   
#Pdiv toujours inferieur ou egal a Prad
 ss4=N.where(Pdivb>Prad) [0] 
 Pdivb[ss4]=Prad[ss4]
 sss4=N.where(Pdivh>Prad) [0] 
 Pdivh[sss4]=Prad[sss4]
 
#calcul Pbulk
 if passe==1:
   Pbulk=Prad-Pdivb-Pdivh
   
 
#temps pour le signal traité
 trad=to+torigin

 
#representation graphique des resultats Prad,Pbulk,Pdivh,Pdivb
 if fi==1:
  plt.figure(1)
  orig=0;
  plt.plot(trad-orig,Prad,'r',trad-orig,Pbulk,'b',trad-orig,Pdivb,'g',trad-orig,Pdivh,'y',linewidth=2)
  plt.ylim(0,max(Prad)+0.5)
  plt.xlabel('time [s]',fontsize=20,fontweight='bold')
  plt.ylabel('radiated Power [MW]',fontsize=20,fontweight='bold')
  plt.legend(['Prad','Pbulk','Pdiv low','Pdiv high'])
  plt.grid('on')
  plt.title('shot  {}' .format(shot),fontsize=20,fontweight='bold')
  plt.show('')

#representation du temps reel skip=0  ou pas skip=1
 
 
 orig=0   
 if west==2:
  skip=1
  if skip==0:
   [bolor,tbolor]=pywed.tsmat(shot,'DBOLO-GDATREEL','+')
   Pradr=bolor[:,0]
   Pbulkr=bolor[:,1]
   Pdivr=bolor[:,2]
   tradr=tbolor[:,0]
   plt.figure(3)
   plt.plot(tradr-orig,Pradr,'r',tradr-orig,Pbulkr,'b',tradr-orig,Pdivr,'g',linewidth=2)
   plt.xlabel('time [s]',fontsize=20,fontweight='bold')
   plt.ylabel('radiated Power [MW]',fontsize=20,fontweight='bold')
   plt.grid('on')
   plt.title('shot {} real time calculation' .format(shot),fontsize=20,fontweight='bold')
 

 plt.disp('*********************************************************')
 plt.disp('version 1, no reading  of plasma large  radius, assumed to be:')
 if west==2:
  #plt.legend(['Prad total','Pbulk','Pdiv'])
  plt.disp('2.5m for WEST ')
 else:
  #plt.legend(['Prad total','Pbulk','Plim'])
  plt.disp(' 2.38m for Tore Supra')

 plt.disp('all signals resampled at 1 ms')

 if west==2:
    if shot>100:
        if ev==1:
           bb=[kk for kk in ld if Prad[kk]<3*N.mean(Prad) if trad[kk]>32]
           if N.trapz(Pdivb[bb],trad[bb])>N.trapz(Pdivh[bb],trad[bb]):
             plt.disp('.')
             plt.disp('MORE RADIATION NEAR BOTTOM DIVERTOR')
             plt.disp('.')
           else:
             plt.disp('.')
             plt.disp('MORE RADIATION NEAR TOP DIVERTOR')
             plt.disp('.')
        else:
           plt.disp('.')
           plt.disp('RADIATION EVERYWHERE')
           plt.disp('.')
    else:
        plt.disp('.')
        plt.disp('TEST INFO')
        plt.disp('.')

    plt.disp('Prad=total radiated power [MW]')   
    plt.disp('Pdivb=estimated radiated power in low divertor [MW]')
    plt.disp('Pdivh=estimated radiated power in top divertor [MW]')
 else:
   plt.disp('Prad=total radiated power [MW]')
   plt.disp('Pdiv=estimated radiated above limiter  [MW]')

 plt.disp('Pbulk= estimated radiated power in bulk [MW]')
 plt.disp('Pchan=radiated power on each channel integrated toroidally [MW]')
 plt.disp('trad=time  [s]')
 plt.disp('*********************************************************')

#representation puissance rayonnée par ligne de visée 
 if fi==1:
  plt.figure(2)
  plt.subplot(2,2,1)
  plt.plot(trad-orig,Pchan[:,0],'r',trad-orig,Pchan[:,1],'b',trad-orig,Pchan[:,2],'g',trad-orig,Pchan[:,3],'k',linewidth=2)
  plt.grid('on')
  plt.legend(['chan. 1','2','3','4'])
  plt.subplot(2,2,2)
  plt.plot(trad-orig,Pchan[:,4],'r',trad-orig,Pchan[:,5],'b',trad-orig,Pchan[:,6],'g',trad-orig,Pchan[:,7],'k',linewidth=2)
  plt.grid('on')
  plt.legend(['5','6','7','8'])
  plt.subplot(2,2,3)
  plt.plot(trad-orig,Pchan[:,8],'r',trad-orig,Pchan[:,9],'b',trad-orig,Pchan[:,10],'g',trad-orig,Pchan[:,11],'k',linewidth=2)
  plt.grid('on')
  plt.legend(['9','10','11','12'])
  plt.subplot(2,2,4)
  plt.plot(trad-orig,Pchan[:,12],'r',trad-orig,Pchan[:,13],'b',trad-orig,Pchan[:,14],'g',trad-orig,Pchan[:,15],'k',linewidth=2)
  plt.legend(['13','14','15','16'])
  plt.grid('on')
 
  plt.xlabel('time [s]',fontsize=12,fontweight='bold')
  plt.ylabel('radiated Power [MW]',fontsize=12,fontweight='bold')
  plt.title('shot {}' .format(shot),fontsize=16,fontweight='bold')
  plt.show('')
 if passe==1:
  return Prad,Pbulk,Pdivb,Pdivh,Pchan,bolofmas,tbolo,trad
 else:
  return Prad,Pbulk,Pdivb,Pdivh,Pchan,bolofmas,tbolo,trad
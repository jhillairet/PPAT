function [x,t]=AcqNL_Alex(date,heuredeb,heurefin,Num)
[x,t]=tsbase('gnivl',date,heuredeb,heurefin);
size(x)
Param= []; Param.DateFormat = 'HH:MM:SS';
t=t(:,1)/3600/24;




% Voie n�1 EANS1

EANS1=x(:,1);
%Lin�arisation � partir de analincAcq.m
EANS1P=analincAcq('eans1',EANS1);


% Voie n�2 EANS2

EANS2=x(:,2);
%Lin�arisation � partir de analincAcq.m
EANS2P=analincAcq('eans2',EANS2);


% Voie n�3 EANS3

EANS3=x(:,3);
%Lin�arisation � partir de analincAcq.m
EANS3P=analincAcq('eans3',EANS3);


% Voie n�4 EANS4


EANS4=x(:,4);
%Lin�arisation � partir de analincAcq.m
EANS4P=analincAcq('eans4',EANS4);


% Voie n�5 EANS5

EANS5=x(:,5);
%Lin�arisation � partir de analincAcq.m
EANS5P=analincAcq('eans5',EANS5);


% Voie n�6 EANS6

EANS6=x(:,6);
%Lin�arisation � partir de analincAcq.m
EANS6P=analincAcq('eans6',EANS6);


% Voie n�7 EANS7

EANS7=x(:,7);
%Lin�arisation � partir de analincAcq.m
EANS7P=analincAcq('eans7',EANS7);


% Voie n�8 EANS8

EANS8=x(:,8);
%Lin�arisation � partir de analincAcq.m
EANS8P=analincAcq('eans8',EANS8);


% Voie n�9 EANS9

EANS9=x(:,9);
%Lin�arisation � partir de analincAcq.m
EANS9P=analincAcq('eans9',EANS9);


% Voie n�10 EANS10

EANS10=x(:,10);
%Lin�arisation � partir de analincAcq.m
EANS10P=analincAcq('eans10',EANS10);


% Voie n�11 EANS11

EANS11=x(:,11);
%Lin�arisation � partir de analincAcq.m
EANS11P=analincAcq('eans11',EANS11);


% Voie n�12 EANS12

EANS12=x(:,12);
%Lin�arisation � partir de analincAcq.m
EANS12P=analincAcq('eans12',EANS12);


% Voie n�13 EANS13A

EANS13A=x(:,13);
%Lin�arisation � partir de analincAcq.m
EANS13P=analincAcq('eans13a',EANS13A);


% Voie n�14 EANS13B

EANS13B=x(:,14);
%Lin�arisation � partir de analincAcq.m
EANS14P=analincAcq('eans13b',EANS13B);


% Voie n�15 EANS14A

EANS14A=x(:,15);
%Lin�arisation � partir de analincAcq.m
EANS15P=analincAcq('eans14a',EANS14A);


% Voie n�16 EANS14B

EANS14B=x(:,16);
%Lin�arisation � partir de analincAcq.m
EANS16P=analincAcq('eans14b',EANS14B);


% Voie n�17 EANS15A

EANS15A=x(:,17);
%Lin�arisation � partir de analincAcq.m
EANS17P=analincAcq('eans15a',EANS15A);


% Voie n�18 EANS15B

EANS15B=x(:,18);
%Lin�arisation � partir de analincAcq.m
EANS18P=analincAcq('eans15b',EANS15B);


% Voie n�19 EANS16A

EANS16A=x(:,19);
%Lin�arisation � partir de analincAcq.m
EANS19P=analincAcq('eans16a',EANS16A);


% Voie n�20 EANS16B

EANS16B=x(:,20);
%Lin�arisation � partir de analincAcq.m
EANS20P=analincAcq('eans16b',EANS16B);


% Voie n�21 EANS17A

EANS17A=x(:,21);
%Lin�arisation � partir de analincAcq.m
EANS21P=analincAcq('eans17a',EANS17A);


% Voie n�22 EANS17B

EANS17B=x(:,22);
%Lin�arisation � partir de analincAcq.m
EANS22P=analincAcq('eans17b',EANS17B);

% Voie n�23 EANS18A

EANS18A=x(:,23);
%Lin�arisation � partir de analincAcq.m
EANS23P=analincAcq('eans18a',EANS18A);


% Voie n�24 EANS18B

EANS18B=x(:,24);
%Lin�arisation � partir de analincAcq.m
EANS24P=analincAcq('eans18b',EANS18B);

x=[EANS1P,EANS2P,EANS3P,EANS4P,EANS5P,EANS6P,EANS7P,EANS8P,EANS9P,EANS10P,...
    EANS11P,EANS12P,EANS13P,EANS14P,EANS15P,EANS16P,EANS17P,EANS18P,EANS19P,EANS20P,EANS21P,EANS22P,EANS23P,EANS24P];





%     figure(2);clf;
%     if Num==0
%         subplot(2,1,1)
%         plot_vs_date_V1(t,x(:,[1:12]),Param);
%         legend ('NL01','NL02','NL03','NL04','NL05','NL06','NL07','NL08','NL09','NL10','NL11','NL12');
%         ylabel('TEMP en K');
%         xlabel('Temps en h');
%         title('Temperature niveaux liquides');
% 
%         subplot(2,1,2)
%         plot_vs_date_V1(t,x(:,[12:24]),Param);
%         legend ('NL13','NL14','NL15','NL16','NL17','NL18', 'NL13B', 'NL14B', 'NL15B', 'NL16B', 'NL17B', 'NL18B');
%     else
%         plot_vs_date_V1(t,x(:,Num),Param);	
%         legend(['NL',num2str(Num)]);	
%     end
%     
% ylabel('TEMP en K');
% xlabel('Temps en h');
% title('Temperature niveaux liquides');
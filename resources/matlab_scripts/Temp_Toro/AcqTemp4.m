function [x,t]=AcqTemp4(date,heuredeb,heurefin,Num)
[x,t]=tsbase('gtemp',date,heuredeb,heurefin);
t=t(:,1)/3600/24; 
Param= []; Param.DateFormat = 'HH:MM:SS';

MT=[];
      for j=1:18
	 V=x(:,j);
	 if j<10
	 NomCapt=['tabt0',num2str(j)];
	 else
	 NomCapt=['tabt',num2str(j)];
	 end
	 Temp=analincAcq(NomCapt,V);
	     MT=[MT,Temp];	 		 	
      end; 
  MT1=MT(:,[1:9]);
  MT2=MT(:,[10:18]);
  if (Num>=1 & Num <=18) Typ='n'; else Typ='o';end;
%   figure(2);clf
%   if strcmp(Typ,'o')==1
   	x=MT;
% 	subplot(2,1,1);plot_vs_date_V1(t,MT1,Param);
% 	title('TEMPERATURES AMENEES DE COURANT EN �K sauf Valeur > 5V en V'); 
%  	xlabel('Temps en h');
%   	ylabel('Temp�ratures en �K');
%   	legend ('BT01','BT02','BT03','BT04','BT05','BT06','BT07','BT08','BT09');
%   
% 	subplot(2,1,2);plot_vs_date_V1(t,MT2,Param);
% 	title('TEMPERATURES AMENEES DE COURANT EN �K sauf Valeur > 5V en V'); 
%  	xlabel('Temps en h');
%   	ylabel('Temp�ratures en �K');
%   	legend ('BT10','BT11','BT12','BT13','BT14','BT15','BT16','BT17','BT18');
%   else
%   MT3=MT(:,Num);
%   x=MT;
%   plot_vs_date_V1(t,MT3,Param);
%   	title('TEMPERATURE AMENEE DE COURANT EN �K sauf Valeur > 5V en V'); 
%  	xlabel('Temps en h');
%   	ylabel('Temp�ratures en �K');
% 	legend(['BT',num2str(Num)]);
%  end;
 return

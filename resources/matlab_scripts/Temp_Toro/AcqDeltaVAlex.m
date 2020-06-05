function [x2,t]=AcqDeltaVAlex(date,heuredeb,heurefin,Num)
[x,t]=tsbase('gvbt',date,heuredeb,heurefin);
Param= []; Param.DateFormat = 'HH:MM:SS';

t=t(:,1)/3600/24;

V01=x(:,1);
V02=x(:,2);
V03=x(:,3);
V04=x(:,4);
V05=x(:,5);
V06=x(:,6);
V07=x(:,7);
V08=x(:,8);
V09=x(:,9);
V10=x(:,10);
V11=x(:,11);
V12=x(:,12);
V13=x(:,13);
V14=x(:,14);
V15=x(:,15);
V16=x(:,16);
V17=x(:,17);
V18=x(:,18);

DV1=V02-V04;
DV2=V06-V18;
DV3=V08-V10;
DV4=V08-V12;
DV5=V14-V18;
DV6=V04-V16;
DV7=V01-V05;
DV8=V03-V15;
DV9=V07-V11;
DV10=V09-V17;
DV11=V11-V13;
DV12=V05-V07;
DV13=V03-V09;
DV14=V01-V13;
DV15=V15-V17;
DV16=V02-V10;
DV17=V06-V12;
DV18=V14-V16;

x2=[DV1,DV2,DV3,DV4,DV5,DV6,DV7,DV8,DV9,DV10,DV11,DV12,DV13,DV14,DV15,DV16,DV17,DV18];

% leg={'DV1=V02-V04','DV2=V06-V18','DV3=V08-V10','DV4=V08-V12','DV5=V14-V18',...
%       'DV6=V04-V16','DV7=V01-V05','DV8=V03-V15','DV9=V07-V11','DV10=V09-V17',...
%       'DV11=V11-V13','DV12=V05-V07','DV13=V03-V09','DV14=V01-V13','DV15=V15-V17','DV16=V02-V10','DV17=V06-V12','DV18=V14-V16'};
% 
% % figure(2);clf;
% if Num==0
%   plot_vs_date_V1(t,x2,Param);
%   legend ('DV1=V02-V04','DV2=V06-V18','DV3=V08-V10','DV4=V08-V12','DV5=V14-V18',...
%       'DV6=V04-V16','DV7=V01-V05','DV8=V03-V15','DV9=V07-V11','DV10=V09-V17',...
%       'DV11=V11-V13','DV12=V05-V07','DV13=V03-V09','DV14=V01-V13','DV15=V15-V17','DV16=V02-V10','DV17=V06-V12','DV18=V14-V16');
%   title('DeltaV Alex sans coeffs de matriçage')
% else
%   plot_vs_date_V1(t,x2(:,Num),Param);
%   legend(leg(Num));
%   title('DeltaV Alex sans coeffs de matriçage')
% end
% 
% ylabel('Tension en V');
% xlabel('Temps en h');
% title('BASSES TENSIONS');
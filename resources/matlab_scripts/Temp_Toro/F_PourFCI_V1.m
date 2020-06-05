%% Script de balayage des chocs pour trac� des siggnaux plasma et TORO.
%--------------------------------------------------------------------------
%
% Fonction de tracé des signaux de détéction de Quench pour voir la
% perturbation par rapport a FCI...
%
% 53640

function []=F_PourFCI_V1(NumChoc)

close all;

% Pour Utiliser les lin�arisation et calibration AcqTemp4.m


% D�finition du choc
Choc0=NumChoc;    % choc 11h37 ele 17/07/18

Choc=Choc0;

% D�finition du fen�trage autour du point de temps ORIGINE
DeltatM=2; % � soustraire - En secondes
DeltatP=45; % � ajouter - En secondes

i=1;

    % R�cup�ration de la date absolue du point "ORIGINE" du choc en cours
    dat0=tsmat(Choc,'APILOTE;+VME_PIL;Date_Choc');
    dat=strtrim(dat0)
    if isempty(str2num(dat(end)))
        dat(end+1:end+3)='000';
    end
    
    
    if isempty(dat)
        
    else
        dmy=dat(1:9);
        dmy2=datestr(datenum(dmy,'dd-mmm-yy'),'dd/mm/yyyy'); % DD/MM/YYYY de ORIGINE
        hms=dat(end-11:end); 
        hms2=hms(1:8);  % HH:MM:SS de ORIGINE
        hms3=str2num(hms2(1:2))*60*60+str2num(hms2(4:5))*60+str2num(hms2(7:8));

        % Definition de l'heure de d�but pour les Acquisitions Continues
        heuredeb0=datestr(datenum(dat,'dd-mmm-yy HH:MM:SS.FFF')-DeltatM/(24*60*60));
        heuredeb=heuredeb0(13:20);
        % Definition de l'heure de d�but pour les Acquisitions Continues
        heurefin0=datestr(datenum(dat,'dd-mmm-yy HH:MM:SS.FFF')+DeltatP/(24*60*60));
        heurefin=heurefin0(13:20);
        % Date du choc
        date=dmy2;

        % Chargement des donn�es:
            % Courant Plasma:
            [Ip,t1]=tsbase(Choc,'smag_ip','+');     % t1 de -30s � +31s environ, centr� sur dat
            [FluNtn,t2]=tsbase(Choc,'gfluntn','+');
            
            % Nouvelles basses tensions
            [NVBT,t]=tsbase('GTOR_NVBT',date,heuredeb,heurefin);    % t
            if isempty(NVBT)
                [NVBT,t]=tsbase('GTOR_VBT',date,heuredeb,heurefin);    % t
                NVBTresc=Ip.*0;     % Calibration idem que dans AcqNewSecuVBT.m
                tresc=t1;              % Rescale du temps
            else
                NVBTresc=(NVBT./2^15) * 50;     % Calibration idem que dans AcqNewSecuVBT.m
                tresc=t(:,1)-hms3;              % Rescale du temps
            end
            
            % Anciennes basses tensions
            [VBT,t]=tsbase('gvbt',date,heuredeb,heurefin);    % t
            taresc=t(:,1)-hms3;              % Rescale du temps
            
            % DeltaV
            [DV,tdv]=AcqDeltaVAlex(date,heuredeb,heurefin,0);
            tdv2=tdv(:,1)*3600*24-hms3;
            
            
            % Temp�ratures
            [T,tt]=AcqTemp4(date,heuredeb,heurefin,0);
            
            ttresc=tt(:,1)*3600*24-hms3;
            
            % Pression
            [Pres,tp]=tsbase('gpressions',date,heuredeb,heurefin);
            tpres=tp(:,1)-hms3;
            
            
            % NiveauxLiquides
            [NL,tnl]=AcqNL_Alex(date,heuredeb,heurefin,0)
%             [NL,tnl]=tsbase('gnivl',date,heuredeb,heurefin);
            tnivl=tnl(:,1)*3600*24-hms3;
            
            
            
            
            % Puissance FCI
            [Pfci,tfci]=tsbase(NumChoc,'GICHANTPOWQ2','+');
            if isempty(Pfci)
                Pfci=[0 0 0]; tfci=0;
            end
            %             tfci2=tfci(:,1)-hms3;
            figure; plot(tfci,Pfci(:,1));
            
            % Puissance Hybride
            [Phyb,thyb]=tsbase(NumChoc,'GPHYB','+');
            if isempty(Phyb)
                Phyb=[0 0 0]; thyb=0;
            end
%             tfci2=tfci(:,1)-hms3;
            figure; plot(thyb,Phyb(:,3));
                        
            
            
close all
        % TRAC�    
        figure;
%         Hall=[]; % Toutes les handles de plots
%         Hall2=[]; % Toutes les handles de plots
%         Hall3=[]; % Toutes les handles de plots
%         Leg={};  % L�gende dynamique
%         Leg2={};  % L�gende dynamique
%         Leg3={};  % L�gende dynamique

        % Trac� du courant plasma et des tensions
        ax1=subplot(4,2,1);
            hp=plot(t1,Ip,'r','LineWidth',2);
            hold on;
            hfci=plot(tfci(:,1),Pfci(:,1).*10,'b','LineWidth',2);
            hhyb=plot(thyb(:,1),Phyb(:,3).*500,'m-','LineWidth',1);
            xlim([30 DeltatP]);ylim([-100 800]);
            ylabel('Ip [kA]');
            legend([hfci,hhyb],{'P_F_C_I*10','P_H_Y_B*500'});
%             legend(hhyb,'P_H_Y_B*500');
        ax2=subplot(4,2,3);
            hv=plot(tresc,NVBTresc);
            hold on;
            %plot([30 DeltatP],[30 DeltatP].*0+2,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([-1 4]);
            ylabel('New VBT [V]');
        ax3=subplot(4,2,5);            
            hva=plot(taresc,VBT);
            hold on;
            %plot([30 DeltatP],[30 DeltatP].*0+2,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([-1 4]);
            ylabel('Old VBT [V]');
        ax4=subplot(4,2,7);            
            hvt=plot(tdv2,DV);
            hold on;
            plot([30 DeltatP],[30 DeltatP].*0+2,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([-1 2.5]);
            ylabel('DV [V]');
            title('Seuil >2V/Tempo 1s');
    linkaxes([ax1,ax2,ax3,ax4],'x');            
            
        ax11=subplot(4,2,2);
            hp=plot(t1,Ip,'r','LineWidth',2);
            hold on;
            hfci=plot(tfci(:,1),Pfci(:,1).*10,'b','LineWidth',2);
            hhyb=plot(thyb(:,1),Phyb(:,3).*500,'m-','LineWidth',1);
            xlim([30 DeltatP]);ylim([-100 800]);
            ylabel('Ip [kA]');
            legend([hfci,hhyb],'P_F_C_I*10','P_H_Y_B*500');
%             legend(hhyb,'P_H_Y_B*500');
        ax21=subplot(4,2,4);
            hp=plot(tpres,Pres*10);
            hold on;
            plot([30 DeltatP],[30 DeltatP].*0+2,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([1 3]);
            ylabel('Pressions [bar]');
            title('Seuil >2b/Tempo 200ms');
        ax31=subplot(4,2,6);            
            hnl=plot(tnivl,NL);
            hold on;
            plot([30 DeltatP],[30 DeltatP].*0+1.95,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([1 3]);
            ylabel('Niveaux Liquides [K]');
            title('Seuil <1.95K/Tempo 1s');
        ax41=subplot(4,2,8);            
            hvt=plot(ttresc,T);
            hold on;
            plot([30 DeltatP],[30 DeltatP].*0+1.98,'k-','LineWidth',4);
            xlim([30 DeltatP]);ylim([1.5 2.5]);
            ylabel('Tbob [K]');
            title('Seuil >1.98K/Tempo 1s');
        linkaxes([ax11,ax21,ax31,ax41],'x');                       

        set(gcf,'Position',[0 0 1000 1000]);
        set(gcf,'color','w');   

            


    end
    

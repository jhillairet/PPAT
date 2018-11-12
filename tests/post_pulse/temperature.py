

clear all;
close all;
tic

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Derni?re modification du code : 15/10/18 par J. Gaspar
% Code valide pour les pulses ? partir du 52933 (C3)
% Plot des TC/FBG (divertor bas + baffle) en T? absolue et ?chauffement
% (ne fonctionne pas lors des 'cleaning pulses')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

prompt = {'Enter the pulse number:'};
title = 'N? choc';
dims = [1 35];
last_choc=52933; % A changer avec r?cup?ration du dernier num?ro de choc
definput = {num2str(last_choc)};
answer_choc = inputdlg(prompt,title,dims,definput);

choc = str2num(answer_choc{1});

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Limite heating rate WOI 15/10/18
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DTlim_div=100;
DTlim_baffle=20;

try

    
 [Ip,tip]=tsbase(choc,'SMAG_IP');                                         % Plasma current
[VLOOP,tvloop]=tsbase(choc,'GMAG_VLOOP');
Nvloop=size(VLOOP);
for i=1:17
    POHM(:,i)=VLOOP(:,i).*Ip(:,1);
end

for i=1:Nvloop(1)
    Ohmic_power(i,1)=mean(POHM(i,:))*1e-3;                            % Ohmic power
end;

% filtrage
windowSize = 25;
b = (1/windowSize)*ones(1,windowSize);
a = 1;
POHM_f = filter(b,a,Ohmic_power);
% figure(1)
% plot(tip,Ohmic_power,'b',tip,POHM_f ,'r')


[PLH,tplh]=tsbase(choc,'SHYBPTOT');                                  % LH power

% figure(2)
% plot(tplh,PLH)
[PFCI,tpfci]=tsbase(choc,'SICHPTOT');                                 % ICRH power
PFCI=PFCI*1e-3;
% filtrage de PFCI
windowSize = 25;
b = (1/windowSize)*ones(1,windowSize);
a = 1;
PFCI_f = filter(b,a,PFCI);

ind1=find(tip>tplh(1));
ind2=find(tip<tplh(end));

tptot=tip(ind1(1)):0.020:tip(ind2(end))'; % base de temps de PTOT demandee

% choc avec hybride et FCI
% réechantillonnage
if (~isempty(PLH)) && (~isempty(PFCI))
    %[POHM_f_rs,PLH_rs,PFCI_rs,tptot]=SAMPLETS(POHM_f(ind1(1):ind2(end)), tip(ind1(1):ind2(end)),PLH,tplh,PFCI_f,tpfci);
    POHM_f_rs= interp1(tip(ind1(1):ind2(end)),POHM_f(ind1(1):ind2(end)),tptot);
    PLH_rs= interp1(tplh,PLH,tptot);
    PFCI_f_rs= interp1(tpfci,PFCI_f,tptot);
    PTOT= POHM_f_rs + PLH_rs +PFCI_f_rs;
    
    % choc avec hybride seulement
    % réechantillonnage
elseif  (~isempty(PLH))
    POHM_f_rs= interp1(tip(ind1(1):ind2(end)),POHM_f(ind1(1):ind2(end)),tptot);
    PLH_rs= interp1(tplh,PLH,tptot);
    PTOT= POHM_f_rs +PLH_rs  ;
    
    % choc avec FCI seulement
    % réechantillonnage
elseif  (~isempty(PFCI) )
    POHM_f_rs= interp1(tip(ind1(1):ind2(end)),POHM_f(ind1(1):ind2(end)),tptot);
    PFCI_f_rs= interp1(tpfci,PFCI_f,tptot);
    PTOT= POHM_f_rs +PFCI_f_rs ;
    % choc ohmique
    % réechantillonnage
else
    POHM_f_rs= interp1(tip(ind1(1):ind2(end)),POHM_f(ind1(1):ind2(end)),tptot);
    PTOT= POHM_f_rs;
end;    
    
    
  flag_ptot=1;
catch
    flag_ptot=0;
    disp('Probleme calcul Ptot  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
end

try
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % R?cup?ration des donn?es FBG
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    [cr]=tsrfile(choc,'FTFIB_TEMP',strcat('dtfib',answer_choc{1,1},'.zip'));
    
    unzip(strcat('dtfib',answer_choc{1,1},'.zip'));
    
    % % Recherche des fichiers avec ce num?ro de choc
    fstruct_L1 = dir([answer_choc{1} '_temperatures_L1']);
    fstruct_L2 = dir([answer_choc{1} '_temperatures_L2']);
    fstruct_L3 = dir([answer_choc{1} '_temperatures_L3']);
    fstruct_L4 = dir([answer_choc{1} '_temperatures_L4']);
    
    %%% Ici mettre les noms (ou chemin) des fichiers des 4 voies
    filename{1,1} = fstruct_L1.name; % Voie 1
    filename{2,1} = fstruct_L2.name; % Voie 2
    filename{3,1} = fstruct_L3.name; % Voie 3
    filename{4,1} = fstruct_L4.name; % Voie 4
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    % Lecture du fichier FBG
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    
    FBG_voie=4;
    
    delimiter = '\t';
    
    %%% Read columns of data as strings:
    % For more information, see the TEXTSCAN documentation.
    formatSpec = '%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';
    
    %%% Open the text file.
    fileID = fopen(filename{FBG_voie,1},'r');
    
    %%% Read columns of data according to format string.
    % This call is based on the structure of the file used to generate this
    % code. If an error occurs for a different file, try regenerating the code
    % from the Import Tool.
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);
    
    %%% Close the text file.
    fclose(fileID);
    
    %%% Convert the contents of columns containing numeric strings to numbers.
    % Replace non-numeric strings with NaN.
    raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
    for col=1:length(dataArray)-1
        raw(1:length(dataArray{col}),col) = dataArray{col};
    end
    numericData = NaN(size(dataArray{1},1),size(dataArray,2));
    
    for col=[1,2,3,4,5,6,7,8,9,10,11,12]
        % Converts strings in the input cell array to numbers. Replaced non-numeric
        % strings with NaN.
        rawData = dataArray{col};
        for row=1:size(rawData, 1);
            % Create a regular expression to detect and remove non-numeric prefixes and
            % suffixes.
            regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\.]*)+[\,]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\.]*)*[\,]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
            try
                result = regexp(rawData{row}, regexstr, 'names');
                numbers = result.numbers;
                
                % Detected commas in non-thousand locations.
                invalidThousandsSeparator = false;
                if any(numbers=='.');
                    thousandsRegExp = '^\d+?(\.\d{3})*\,{0,1}\d*$';
                    if isempty(regexp(thousandsRegExp, '.', 'once'));
                        numbers = NaN;
                        invalidThousandsSeparator = true;
                    end
                end
                % Convert numeric strings to numbers.
                if ~invalidThousandsSeparator;
                    numbers = strrep(numbers, '.', '');
                    numbers = strrep(numbers, ',', '.');
                    numbers = textscan(numbers, '%f');
                    numericData(row, col) = numbers{1};
                    raw{row, col} = numbers{1};
                end
            catch me
            end
        end
    end
    %%% Create output variable
    FBG_temperatures_RAW{FBG_voie,1} = cell2mat(raw);
    
    %%% Clear temporary variables
    clearvars delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me;
    
    
    % Suppression des fichiers DTFIB
    delete ([answer_choc{1} '_temperatures_L1']);
    delete ([answer_choc{1} '_temperatures_L2']);
    delete ([answer_choc{1} '_temperatures_L3']);
    delete ([answer_choc{1} '_temperatures_L4']);
    delete (strcat('dtfib',answer_choc{1,1},'.zip'));
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    % Fin de lecture du fichier FBG
    %%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Calcul de l'?chauffement glissant (5s)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % D?finition du t=0 32s apr?s origine
    FBG_time_L4(:,1)=(FBG_temperatures_RAW{4,1}(:,1)-FBG_temperatures_RAW{4,1}(1,1))*1E-9-32;
    FBG_temperatures_L4(:,:)=FBG_temperatures_RAW{4,1}(:,2:12);
    
    nFBG=size(FBG_time_L4,1);
    
    inst_t_0=[];
    
    inst_t_0=find(FBG_time_L4(:,1)>0);
    
    
    for i=1:11
        for k=inst_t_0(1,1):nFBG
            FBG_heating_rate_L4(k,i)=FBG_temperatures_L4(k,i)-mean(FBG_temperatures_L4(k-52:k-48,i)); %moyenne glissante de rayon 2, 5s avant le temps courant
        end
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Plot des courbes FBG
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    figure('Name','L4 Q3A 7mm');
    clf
    subplot(2,1,1);
    %[hP,hL1,hL2]=plotyy(FBG_time_L4,FBG_temperatures_L4(:,1),tptot,PTOT);
    %set(hL2,'LineWidth',2,'color','y'); set(hP(2),'ycolor','y'); ylabel(hP(2),'Total Power (MW) ') % right y-axis
    plot(FBG_time_L4,FBG_temperatures_L4(:,1),'-b');
    hold on;
    plot(FBG_time_L4,FBG_temperatures_L4(:,2),'-r');
    plot(FBG_time_L4,FBG_temperatures_L4(:,3),'-g');
    plot(FBG_time_L4,FBG_temperatures_L4(:,4),'-c');
    plot(FBG_time_L4,FBG_temperatures_L4(:,5),'-m');
    plot(FBG_time_L4,FBG_temperatures_L4(:,6),'-k');
    plot(FBG_time_L4,FBG_temperatures_L4(:,7),'--b');
    plot(FBG_time_L4,FBG_temperatures_L4(:,8),'--r');
    plot(FBG_time_L4,FBG_temperatures_L4(:,9),'--g');
    plot(FBG_time_L4,FBG_temperatures_L4(:,10),'--c');
    if flag_ptot<1
    plot(FBG_time_L4,FBG_temperatures_L4(:,11),'--m');
    legend('FBG 1','FBG 2','FBG 3','FBG 4','FBG 5','FBG 6','FBG 7','FBG 8','FBG 9','FBG 10','FBG 11')
    else
    [AX,H1,H2] =plotyy(FBG_time_L4,FBG_temperatures_L4(:,11),tptot,PTOT);
    set(H1,'LineStyle','--','Color','m');
    set(H2,'LineStyle','-','Color','k');
    legend('FBG 1','FBG 2','FBG 3','FBG 4','FBG 5','FBG 6','FBG 7','FBG 8','FBG 9','FBG 10','FBG 11','Ptot')
    end
    xlabel('Time (s)');     
    ylabel('T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');    
    
    subplot(2,1,2);
    plot(Vxlim,[DTlim_div,DTlim_div],'Color','r','LineWidth',[2]);
    hold on;
    plot(FBG_time_L4,FBG_heating_rate_L4(:,1),'-b');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,2),'-r');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,3),'-g');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,4),'-c');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,5),'-m');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,6),'-k');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,7),'--b');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,8),'--r');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,9),'--g');
    plot(FBG_time_L4,FBG_heating_rate_L4(:,10),'--c');
    if flag_ptot<1
    plot(FBG_time_L4,FBG_heating_rate_L4(:,11),'--m');
    legend('seuil','FBG 1','FBG 2','FBG 3','FBG 4','FBG 5','FBG 6','FBG 7','FBG 8','FBG 9','FBG 10','FBG 11')
    else
    [AX,H1,H2] =plotyy(FBG_time_L4,FBG_heating_rate_L4(:,11),tptot,PTOT);
    set(H1,'LineStyle','--','Color','m');
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','FBG 1','FBG 2','FBG 3','FBG 4','FBG 5','FBG 6','FBG 7','FBG 8','FBG 9','FBG 10','FBG 11','Ptot')
    end
    xlabel('Time (s)');
    ylabel('T(t)-T(t-5s) (?C)');

    grid; 
   
catch
    disp('PAS DE DONNEES FBG  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
end

try
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % R?cup?ration des donn?es TC div + baffle
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Param?tres pour TC
    nt=1; % nombre de fois t_finacqu augment?
    
    correction=1 ; % correction ou non des sauts de temps >1 ==> correction, <1 pas de correction
    
    % R?cup?ration de la date du choc avec tsdate ou tsmat(APILOTE)
    
    [date_pilote]=tsmat(choc,'APILOTE;+VME_PIL;Date_Choc');
    C=textscan(date_pilote,'%s %f:%f:%f');
    date_choc=datestr(datenum(C{1,1}),'dd/mm/yy');
    
    % R?cup?ration de la datation du pc DCALOR (en ms depuis minuit) lorsqu'il re?oit ORIGINE (et donc
    % commence l'acquisition), instant qui sera t=0s dans notre signal
    [inst]=tsmat(choc,'DCALOR;PARAM;ORIGINE');
    
    % Conversion en nombre de la variable de datation de DCALOR seulement pour
    % les chocs des campagnes (>100)
    if(choc>100)
        try
            t_origine=str2num(inst); %en ms
        catch
           t_origine=(C{1,2}*3600+C{1,3}*60+C{1,4})*1000; %en ms
        end
    else
        t_origine=(C{1,2}*3600+C{1,3}*60+C{1,4})*1000; %en ms
    end
    % R?cup?ration de la dur?e entre ORIGINE et finacquisition
    
    t_finacq=tsmat(choc,'FINACQ|1') ;
    
    
    % r?cup?ration des donn?es sur l'ensemble de la journ?e pour ?viter tout
    % bug avec les sauts temporels
    heuredeb='00:01:00';
    heurefin='23:59:00';
    
    % R?cup?ration des signaux TC
    
    [d1,t1] = tsbase('GETC_ISP_6A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    [d2,t2] = tsbase('GETC_OSP_6A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    [d3,t3] = tsbase('GETC_OSP_1A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    [d4,t4] = tsbase('GETC_RIPL_6A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    [d5,t5] = tsbase('GETC_BAFF_2A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    [d6,t6] = tsbase('GETC_BAFF_5A',date_choc,heuredeb,heurefin); %r?cup?ration des donn?es
    
    % D?finition de t=0s ? l'aide de la variable 'DCALOR;PARAM;ORIGINE'
    % stockant la date de DCALOR ? r?ception du code origine
    
    trescale1=t1-(t_origine/1000)-32; %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    trescale2=t2-(t_origine/1000)-32;  %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    trescale3=t3-(t_origine/1000)-32;  %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    trescale4=t4-(t_origine/1000)-32;  %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    trescale5=t5-(t_origine/1000)-32;  %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    trescale6=t6-(t_origine/1000)-32;  %Changement du vecteur temps en d?finissant t=0s comme l'instant d'ORIGINE enregistr? par DCALOR
    
    
    % Partie qui deviendra inutile apr?s r?solution du bug de saut temporel
    
    if correction > 0
        % R?cup?ration des index des temps entre 0 et t_finacq
        
        for i=1:4
            idx1(:,i) = find(trescale1(:,i)<nt*t_finacq-32 & trescale1(:,i)>-32);
            idx2(:,i) = find(trescale2(:,i)<nt*t_finacq-32 & trescale2(:,i)>-32);
            idx3(:,i) = find(trescale3(:,i)<nt*t_finacq-32 & trescale3(:,i)>-32);
            idx5(:,i) = find(trescale5(:,i)<nt*t_finacq-32 & trescale5(:,i)>-32);
            idx6(:,i) = find(trescale6(:,i)<nt*t_finacq-32 & trescale6(:,i)>-32);
        end
        
        for i=1:8
            idx4(:,i) = find(trescale4(:,i)<nt*t_finacq-32 & trescale4(:,i)>-32);
        end
        
        % D?finition des variables avec seulement les instants d'interets
        
        for i=1:4
            tfinal1(:,i) = trescale1(idx1(:,i),i);
            dfinal1(:,i) = d1(idx1(:,i),i);
            tfinal2(:,i) = trescale2(idx2(:,i),i);
            dfinal2(:,i) = d2(idx2(:,i),i);
            tfinal3(:,i) = trescale3(idx3(:,i),i);
            dfinal3(:,i) = d3(idx3(:,i),i);
            tfinal5(:,i) = trescale5(idx5(:,i),i);
            dfinal5(:,i) = d5(idx5(:,i),i);
            tfinal6(:,i) = trescale6(idx6(:,i),i);
            dfinal6(:,i) = d6(idx6(:,i),i);
        end
        
        for i=1:8
            tfinal4(:,i) = trescale4(idx4(:,i),i);
            dfinal4(:,i) = d4(idx4(:,i),i);
        end
        
    else
        % R?cup?ration de tout le signal (POUR TEST)
        
        tfinal1=trescale1;
        tfinal2=trescale2;
        tfinal3=trescale3;
        tfinal4=trescale4;
        tfinal5=trescale5;
        tfinal6=trescale6;
        
        dfinal1=d1;
        dfinal2=d2;
        dfinal3=d3;
        dfinal4=d4;
        dfinal5=d5;
        dfinal6=d6;
        
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Calcul de l'?chauffement glissant (5s)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
    % D?finition du t=0 32s apr?s origine
        
        nTC=size(dfinal1,1);
    
    inst_t_0=[];
    inst_t_0=find(tfinal1(:,1)>0);
    
    for i=1:4
        for k=inst_t_0(1,1):nTC
            hfinal1(k,i)= dfinal1(k,i)-mean(dfinal1(k-102:k-98,i)) ;
            hfinal2(k,i)= dfinal2(k,i)-mean(dfinal2(k-102:k-98,i)) ;
            hfinal3(k,i)= dfinal3(k,i)-mean(dfinal3(k-102:k-98,i)) ;
            hfinal5(k,i)= dfinal5(k,i)-mean(dfinal5(k-102:k-98,i)) ;
            hfinal6(k,i)= dfinal6(k,i)-mean(dfinal6(k-102:k-98,i)) ;
        end
    end
    
    for i=1:8
        for k=inst_t_0(1,1):nTC
            hfinal4(k,i)= dfinal4(k,i)-mean(dfinal4(k-102:k-98,i)) ;
        end
    end
        
    figure('Name','TC Divertor Poloidaux');
    clf
    subplot(3,2,1);
    if flag_ptot<1
    plot(tfinal1,dfinal1);
    legend('Q6A-31L-TCI','Q6A-31L-TCMI','Q6A-31L-TCMO','Q6A-31L-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal1,dfinal1,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q6A-31L-TCI','Q6A-31L-TCMI','Q6A-31L-TCMO','Q6A-31L-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel('ISP 6A T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');

    subplot(3,2,2);
    plot(Vxlim,[DTlim_div,DTlim_div],'Color','r','LineWidth',[2]);
    hold on;
    if flag_ptot<1
    plot(tfinal1,hfinal1);
    legend('seuil','Q6A-31L-TCI','Q6A-31L-TCMI','Q6A-31L-TCMO','Q6A-31L-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal1,hfinal1,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q6A-31L-TCI','Q6A-31L-TCMI','Q6A-31L-TCMO','Q6A-31L-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel('ISP 6A T(t)-T(t-5s) (?C)');

    grid,
    
    subplot(3,2,3);
    if flag_ptot<1
    plot(tfinal2,dfinal2);
    legend('Q6A-21L-TCI','Q6A-21L-TCMI','Q6A-21L-TCMO','Q6A-21L-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal2,dfinal2,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q6A-21L-TCI','Q6A-21L-TCMI','Q6A-21L-TCMO','Q6A-21L-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel('OSP 6A T(t) (?C)');
    grid;   
    Vxlim=[];
    Vxlim=get(gca,'xlim');
    
     subplot(3,2,4);
    plot(Vxlim,[DTlim_div,DTlim_div],'Color','r','LineWidth',[2]);
    hold on;
    if flag_ptot<1
    plot(tfinal2,hfinal2);
    legend('seuil','Q6A-21L-TCI','Q6A-21L-TCMI','Q6A-21L-TCMO','Q6A-21L-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal2,hfinal2,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q6A-21L-TCI','Q6A-21L-TCMI','Q6A-21L-TCMO','Q6A-21L-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel('OSP 6A T(t)-T(t-5s) (?C)');
   
    grid;
        
    subplot(3,2,5);
    if flag_ptot<1
    plot(tfinal3,dfinal3);
    legend('Q1A-21-TCI','Q1A-21-TCMI','Q1A-21-TCMO','Q1A-21-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal3,dfinal3,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q1A-21-TCI','Q1A-21-TCMI','Q1A-21-TCMO','Q1A-21-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel('OSP 1A T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');
    
     subplot(3,2,6);
    plot(Vxlim,[DTlim_div,DTlim_div],'Color','r','LineWidth',[2]);
    hold on;
    if flag_ptot<1
    plot(tfinal3,hfinal3);
    legend('seuil','Q1A-21-TCI','Q1A-21-TCMI','Q1A-21-TCMO','Q1A-21-TCO')
    else
    [AX,H1,H2] =plotyy(tfinal3,hfinal3,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q1A-21-TCI','Q1A-21-TCMI','Q1A-21-TCMO','Q1A-21-TCO','Ptot')
    end
    xlabel('Time (s)');
    ylabel(' OSP 1A T(t)-T(t-5s) (?C)');
    grid;
    
    
    figure('Name','TC Divertor toroidaux');
    subplot(2,1,1);
    if flag_ptot<1
    plot(tfinal4,dfinal4);
    legend('Q6A-13-TCMI','Q6A-15-TCMI','Q6A-17-TCMI','Q6A-22-TCMI','Q6A-23-TCMI','Q6A-25-TCMI','Q6A-27-TCMI','Q6A-29-TCMI')
    else
    [AX,H1,H2] =plotyy(tfinal4,dfinal4,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q6A-13-TCMI','Q6A-15-TCMI','Q6A-17-TCMI','Q6A-22-TCMI','Q6A-23-TCMI','Q6A-25-TCMI','Q6A-27-TCMI','Q6A-29-TCMI','Ptot')
    end
    xlabel('Time (s)');
    ylabel('OSP TOROIDAUX 6A T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');
    
    subplot(2,1,2);
    plot(Vxlim,[DTlim_div,DTlim_div],'Color','r','LineWidth',[2]);
    hold on;
    if flag_ptot<1
    plot(tfinal4,hfinal4);
    legend('seuil','Q6A-13-TCMI','Q6A-15-TCMI','Q6A-17-TCMI','Q6A-22-TCMI','Q6A-23-TCMI','Q6A-25-TCMI','Q6A-27-TCMI','Q6A-29-TCMI')
    else
    [AX,H1,H2] =plotyy(tfinal4,hfinal4,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q6A-13-TCMI','Q6A-15-TCMI','Q6A-17-TCMI','Q6A-22-TCMI','Q6A-23-TCMI','Q6A-25-TCMI','Q6A-27-TCMI','Q6A-29-TCMI','Ptot')
    end
    xlabel('Time (s)');
    ylabel('OSP TOROIDAUX 6A T(t)-T(t-5s) (?C)');

    grid;
    
    
    figure('Name','TC Baffle');
    
    subplot(2,2,1);
    if flag_ptot<1
    plot(tfinal5,dfinal5);
    legend('Q2A-6','Q2A-6','Q2A-10 ','Q2A-10')
    else
    [AX,H1,H2] =plotyy(tfinal5,dfinal5,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q2A-6','Q2A-6','Q2A-10 ','Q2A-10','Ptot')
    end
    xlabel('Time (s)');
    ylabel('BAFFLE 2A T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');
    
    subplot(2,2,2);
    plot(Vxlim,[DTlim_baffle,DTlim_baffle],'Color','r','LineWidth',[2]);
    hold on;
    if flag_ptot<1
    plot(tfinal5,hfinal5);
    legend('seuil','Q2A-6','Q2A-6','Q2A-10 ','Q2A-10')
    else
    [AX,H1,H2] =plotyy(tfinal5,hfinal5,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q2A-6','Q2A-6','Q2A-10 ','Q2A-10','Ptot')
    end
    xlabel('Time (s)');
    ylabel('BAFFLE 2A T(t)-T(t-5s) (?C)');

    grid;
    
    subplot(2,2,3);
     if flag_ptot<1
    plot(tfinal6,dfinal6);
    legend('Q5A-6','Q5A-6','Q5A-10','Q5A-10')
    else
    [AX,H1,H2] =plotyy(tfinal6,dfinal6,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('Q5A-6','Q5A-6','Q5A-10','Q5A-10','Ptot')
    end
    xlabel('Time (s)');
    ylabel('BAFFLE 5A T(t) (?C)');
    grid;
    Vxlim=[];
    Vxlim=get(gca,'xlim');
   
    subplot(2,2,4)
    plot(Vxlim,[DTlim_baffle,DTlim_baffle],'Color','r','LineWidth',[2]);
    hold on;
        if flag_ptot<1
    plot(tfinal6,hfinal6);
    legend('seuil','Q5A-6','Q5A-6','Q5A-10','Q5A-10')
    else
    [AX,H1,H2] =plotyy(tfinal6,hfinal6,tptot,PTOT);
    set(H2,'LineStyle','-','Color','k');
    legend('seuil','Q5A-6','Q5A-6','Q5A-10','Q5A-10','Ptot')
    end
    xlabel('Time (s)');
    ylabel('BAFFLE 5A T(t)-T(t-5s) (?C)');

    grid;
    
catch
    disp('PAS DE DONNEES TC  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
end





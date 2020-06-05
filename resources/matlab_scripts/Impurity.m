clear all ;      close all ;       % run_gui_dc % Equinox

%--------------------------------------------------------------------------
shots = [53974] ;                        % Overview shot number ...
%--------------------------------------------------------------------------

% WEST_suivi_NF_01(shots) ;

interval = [0 12] ;     % Time interval where you want to look

figure;     [B,A]=butter(1,0.01);   % 1st order low pass filter @ 100Hz 

t_ign = tsmat(shots(1),'IGNITRON|1');


%% ------- Plot impurity from EUV -----------------------------------------

figure;     hold on;  linkaxes([ax1,ax2,ax3,ax4,ax5],'x');

% Lecture donnees du SURVIE -----------------------------------------------

% function [surface]=surfn(sp,ind1,ind2,ind3,ind4,ind5,ind6)   
% surface=sum(sp(ind3:ind4,:),1)-(sum(sp(ind1:ind2,:),1)+sum(sp(ind5:ind6,:),1))/(ind2-ind1+ind6-ind5+2)*(ind4-ind3+1);
% end


ti=tne(:,1);

    if shots(1)==38129
        Fe15=zeros(size(ti));
        Fe24=zeros(size(ti));
        O4a=zeros(size(ti));
        C4=zeros(size(ti));
        O4b=zeros(size(ti));
        B5=zeros(size(ti));
        Cu19=zeros(size(ti));
    else
        [spbgl,tspgl,c1]=tsbase(shots(1),'SSURVIE1');
        tspgl = tsbase(shots(1),'GDATESURVIE');
        if (~isempty(spbgl) & ~isempty(tspgl))
            % Datation des spectres
            t_une = tsmat(shots(1),'UNE|1');
            t_ign = tsmat(shots(1),'IGNITRON|1');
            if isempty(t_ign) & ~isempty(t_une)
                t_ign = t_une + 1;
            elseif ~isempty(t_ign) & isempty(t_une)
                t_une = t_ign - 1;
            elseif isempty(t_ign) & isempty(t_une)
                t_une = 31;
                t_ign = 32;
            end
            tsurv = find(tspgl(:,2)<0); tspgl(tsurv,2) = tspgl(tsurv,2)+65536; tsp2 = tspgl(:,1)*65536+tspgl(:,2); tspgl = tsp2/1e6;
            tspgl = tspgl - t_ign;
            tspgl=tspgl(:,1);
            texpogl=mean(diff(tspgl));
            
            % On met le spectre sous forme de matrice (nbre pixels x nbre de spectres)
            spbgl = reshape(spbgl,1340,length(spbgl)/1340);
            if (shots(1)>37993)
                % On retourne le spectre --> camera voie les spectres � l'envers en mode High-Cap 16/10/2006 (choc: 37993)
                spbgl=flipud(spbgl);
            end
            [nb,nb_spbgl] = size(spbgl);
            
            %TEST FILTRAGE DES PARASITES
            ssl=spbgl;
            for i=1:nb_spbgl
                for j=110:1300
                    if spbgl(j,i)>(3*spbgl(j-1,i))
                        spbgl(j,i)=spbgl(j-1,i);
                    end
                end
            end
            
            % SOUSTRACTION DU BRUIT A voir en fonction des premi�res mesures OM 3/04/2006 --> on teste avec spectre 10 (� 100 ms)
            bruitgl = spbgl(:,10)*ones(1,nb_spbgl);
            spglb=spbgl;
            spbgl=spbgl-bruitgl;
            
            % NORMALISATION AU TEMPS D'EXPOSITION
            spgl=spbgl/texpogl;
            
            % Calcul des raies
            % Raies trait�es: FeXV (284,15 A), Fe XXIV (255.09 A), Cu XIX (273,36 A)
            %                 O IVa (279.9 A avec Cr)), C IV (289,2 A), B V (262.37 A)
            %                 He II (256.32 A) O IVb (272.5 avec Fe XXV)
            
           if  shots(1) < 50000    
            Fe15=surfn(spgl,978,982,994,1005,1028,1032); % OM Modif 30/10/2007: 878 --> 978
            Fe24=surfn(spgl,457,461,522,539,587,590);
            O4a=surfn(spgl,846,851,919,933,976,980);
            C4=surfn(spgl,1028,1032,1078,1091,1106,1112); % OM Modif 30/10/2007: 1012 --> 1112
            O4b=surfn(spgl,745,750,788,808,809,813);
            B5=surfn(spgl,587,590,638,652,745,750);
            Cu19=surfn(spgl,809,813,816,827,846,850);
            He2=surfn(spgl,457,461,544,556,587,590);
            Ni18=surfn(spgl,1106,1112,1126,1138,1147,1151);
            Ag16=surfn(spgl,648,651,655,660,662,664);
           else
            trans = 9;
            Fe15=surfn(spgl,(978-trans),(982-trans),(994-trans),(1005-trans),(1028-trans),(1032-trans)); % OM Modif 30/10/2007: 878 --> 978
            Fe24=surfn(spgl,(457-trans),(461-trans),(522-trans),(539-trans),(587-trans),(590-trans));
            O4a=surfn(spgl,(846-trans),(851-trans),(919-trans),(933-trans),(976-trans),(980-trans));
            C4=surfn(spgl,(1028-trans),(1032-trans),(1078-trans),(1091-trans),(1106-trans),(1112-trans)); % OM Modif 30/10/2007: 1012 --> 1112
            O4b=surfn(spgl,(745-trans),(750-trans),(788-trans),(808-trans),(809-trans),(813-trans));
            B5=surfn(spgl,(587-trans),(590-trans),(638-trans),(652-trans),(745-trans),(750-trans));
            Cu19=surfn(spgl,(809-trans),(813-trans),(816-trans),(827-trans),(846-trans),(850-trans));
            He2=surfn(spgl,(457-trans),(461-trans),(544-trans),(556-trans),(587-trans),(590-trans));
            Ni18=surfn(spgl,(1106-trans),(1112-trans),(1126-trans),(1138-trans),(1147-trans),(1151-trans));
            Ag16=surfn(spgl,(648-trans),(651-trans),(655-trans),(660-trans),(662-trans),(664-trans));
           end
            % Lissage des signaux et normalisation
            n=1e4;
            [ord,cut]=butter(5,.2);
            Cu19s=filtfilt(ord,cut,Cu19)/n;
            Fe15s=filtfilt(ord,cut,Fe15)/n;
            Fe24s=filtfilt(ord,cut,Fe24)/n;
            O4as=filtfilt(ord,cut,O4a)/n;
            O4bs=filtfilt(ord,cut,O4b)/n;
            C4s=filtfilt(ord,cut,C4)/n;
            B5s=filtfilt(ord,cut,B5)/n;
            He2s=filtfilt(ord,cut,He2)/n;
            Ag16s=filtfilt(ord,cut,Ag16)/n;
            % r��chantillonnage sur la bonne base de temps
            Fe15s = tsample(Fe15s',tspgl,ti');
            Fe24s = tsample(Fe24s',tspgl,ti');
            O4as  = tsample(O4as',tspgl,ti');
            C4s   = tsample(C4s',tspgl,ti');
            O4bs  = tsample(O4bs',tspgl,ti');
            B5s   = tsample(B5s',tspgl,ti');
            Cu19s = tsample(Cu19s',tspgl,ti');
            He2s  = tsample(He2s',tspgl,ti');
            Ag16s = tsample(Ag16s',tspgl,ti');
        else % pas de donn�es
            Fe15=zeros(size(tspgl));
            Fe24=zeros(size(tspgl));
            O4a=zeros(size(tspgl));
            C4=zeros(size(tspgl));
            O4b=zeros(size(tspgl));
            B5=zeros(size(tspgl));
            Cu19=zeros(size(tspgl));
            He2=zeros(size(tspgl));
            Ni18=zeros(size(tspgl));
            Ag16=zeros(size(tspgl));
            
            
            Fe15s=zeros(size(ti));
            Fe24s=zeros(size(ti));
            O4as=zeros(size(ti));
            C4s=zeros(size(ti));
            O4bs=zeros(size(ti));
            B5s=zeros(size(ti));
            Cu19s=zeros(size(ti));
            He2s=zeros(size(tspgl));
            Ag16s=zeros(size(tspgl));
        end
    end
    
    
% Lecture donnees du SIR --------------------------------------------------
    
if shots(1) < 50000
    if (shots(1)>40154) % remise en service SIR automne 2007
        % Remont�e spectres sp1, sp2
        err_lec_sir = tsrfile(shots(1),'FDSIR1','temp_sir');
        if err_lec_sir<0
            disp('lecdonneesciel - SIR data are not in the datsbase for this pulse')
            sp1=[];
        else
            [id_fichier,message_err_open_fichier] = fopen('temp_sir','r');
            if id_fichier<0
                disp(message_err_open_fichier)
                sp1=[];
            else
                sp1 = fread(id_fichier,inf,'uint16');
            end
            fclose(id_fichier);
        end
        
        err_lec_sir = tsrfile(shots(1),'FDSIR2','temp_sir');
        % err_lec_sir=1; OM 10/01/2011
        if err_lec_sir<0
            disp('lecdonneesciel - SIR data are not in the database for this pulse')
            sp2=[];
        else
            [id_fichier,message_err_open_fichier] = fopen('temp_sir','r');
            if id_fichier<0
                disp(message_err_open_fichier)
                sp2=[];
            else
                sp2 = fread(id_fichier,inf,'uint16');
            end
            fclose(id_fichier);
        end
        
        %Remont�e temps tsp1, tsp2
        err_lec_sir = tsrfile(shots(1),'FDATEDSIR1','temp_sir');
        if err_lec_sir<0
            disp('lecdonneesciel - t SIR data are not in the database for this pulse')
            tsp1=[];
        else
            [id_fichier,message_err_open_fichier] = fopen('temp_sir','r');
            if id_fichier<0
                disp(message_err_open_fichier)
                tsp1=[];
            else
                tsp1 = fread(id_fichier,inf,'uint32');
                tsp1 = tsp1/1e6 - t_ign; % passage en secondes
            end
            fclose(id_fichier);
        end
        
        err_lec_sir = tsrfile(shots(1),'FDATEDSIR2','temp_sir');
        if err_lec_sir<0
            disp('lecdonneesciel - t SIR data are not in the database for this pulse')
            tsp2=[];
        else
            [id_fichier,message_err_open_fichier] = fopen('temp_sir','r');
            if id_fichier<0
                disp(message_err_open_fichier)
            else
                tsp2 = fread(id_fichier,inf,'uint32');
                tsp2 = tsp2/1e6 - t_ign; % passage en secondes
            end
            fclose(id_fichier);
        end
        
        %Remont�e et traitement param�tres
        [dect1,dect2,texpo,reseau,statut_osc,trajectoire,HT]=tsmat(shots(1),'DSIR;PILOTAGE;DETECT1',...
            'DSIR;PILOTAGE;DETECT2','DSIR;PILOTAGE;TEXPO',...
            'DSIR;PILOTAGE;RESEAU','DSIR;PILOTAGE;STATUTOSC','DSIR;PILOTAGE;TRAJECTOIRE','DSIR;PILOTAGE;CONSIGNEHT');
        if (~isempty(sp1))
            texpo1=texpo(1)/1000;
            texpo2=texpo(2)/1000;
        end
        
        lam1=(dect1-180480)/512.06;
        lam2=(dect2-798413)/512;
        
        % Mise en forme des spectres (vecteur-->matrice;retournement pour mode high-cap;normalisation temps d'expo)
        if (~isempty(sp1))
            sp1 = reshape(sp1(1:1340*floor(length(sp1)/1340)),1340,floor(length(sp1)/1340));
            [n1,nb_sp1] = size(sp1);
            sp1=flipud(sp1);
            sp1=sp1/texpo1;
        end
        if (~isempty(sp2))
            sp2 = reshape(sp2(1:1340*floor(length(sp2)/1340)),1340,floor(length(sp2)/1340));
            [n1,nb_sp2] = size(sp2);
            sp2=flipud(sp2);
            sp2=sp2/texpo2;
        end
        
        % ajustement des vecteurs temps
        if (~isempty(tsp1))
            tsp1=tsp1(1:size(sp1,2));
        end
        if (~isempty(tsp2))
            tsp2=tsp2(1:size(sp2,2));
        end
        
        %Donn�es trait�s
        % PL
        if (lam1>120.88 & lam1<121.12 & ~isempty(tsp1) & ~isempty(sp1) & exist('sp1') & (reseau==2))
            % Calcul des surfaces nettes PL
            O8=surfn(sp1,80,85,85,110,110,115);
            O7=surfn(sp1,200,205,210,240,245,250);
            C6=surfn(sp1,780,785,800,850,860,865);
            C6beta=surfn(sp1,525,530,535,570,570,575);
            C5a=surfn(sp1,1160,1165,1190,1224,1250,1255);
            C5b=surfn(sp1,1160,1165,1224,1248,1250,1255);
            % R��chantillonage C6, O8
            O8s = tsample(O8',tsp1,ti');
            C6s = tsample(C6',tsp1,ti');
            C6betas = tsample(C6beta',tsp1,ti');
        else
            if (~isempty(tsp1) & ~isempty(sp1) & (reseau==2))
                disp('Mauvaise position detecteur 1');
            elseif (reseau==1)
                disp('Réseau 300 tr/mm');
            end
            O8=zeros(size(tsp1));
            O8s=zeros(size(ti));
            O7=zeros(size(tsp1));
            C6=zeros(size(tsp1));
            C6beta=zeros(size(tsp1));
            C6s=zeros(size(ti));
            C6betas=zeros(size(ti));
            C5a=zeros(size(tsp1));
            C5b=zeros(size(tsp1));
        end
        
        % GL
        if (lam2>361.88 & lam2<362.12 & ~isempty(tsp2) & ~isempty(sp2) & exist('sp2') & (reseau==2))
            % Calcul des surfaces nettes GL
            Fe15_sir=surfn(sp2,990,995,1007,1027,1045,1050);
            Cu19_sir=surfn(sp2,789,792,794,807,826,829);
            Fe24_sir=surfn(sp2,372,376,449,466,522,527);
            %O4a=surfn(sp2,846,851,919,933,976,980);
            C4_sir=surfn(sp2,1104,1109,1110,1127,1130,1135);
            O4b_sir=surfn(sp2,715,719,762,781,789,792);
            Ni18_sir=surfn(sp2,1158,1164,1168,1185,1190,1195);
            He2_sir=surfn(sp2,372,376,471,489,522,527);
            B5_sir=surfn(sp2,522,527,587,600,715,719);
            Fe15_sirs = tsample(Fe15_sir',tsp2,ti');
            Cu19_sirs = tsample(Cu19_sir',tsp2,ti');
            B5_sirs = tsample(B5_sir',tsp2,ti');
            He2_sirs = tsample(He2_sir',tsp2,ti');
        else
            if (~isempty(tsp2) & ~isempty(sp2) & (reseau==2))
                   disp('Mauvaise position detecteur 2');
            elseif (reseau==1)
                    disp('Réseau 300 tr/mm');
            end
            Fe15_sir=zeros(size(tsp2));
            Cu19_sir=zeros(size(tsp2));
            Fe24_sir=zeros(size(tsp2));
            %O4a=zeros(size(tsp2));
            C4_sir=zeros(size(tsp2));
            O4b_sir=zeros(size(tsp2));
            Ni18_sir=zeros(size(tsp2));
            He2_sir=zeros(size(tsp2));
            B5_sir=zeros(size(tsp2));
            Fe15_sirs = zeros(size(ti));
            Cu19_sirs = zeros(size(ti));
            B5_sirs = zeros(size(ti));
            He2_sirs = zeros(size(ti));
        end
    else
        tsp2=ti;
        tsp1=ti;
        Fe15_sir=zeros(size(tsp2));
        Cu19_sir=zeros(size(tsp2));
        Fe24_sir=zeros(size(tsp2));
        %O4a=zeros(size(tsp2));
        C4_sir=zeros(size(tsp2));
        O4b_sir=zeros(size(tsp2));
        Ni18_sir=zeros(size(tsp2));
        He2_sir=zeros(size(tsp2));
        B5_sir=zeros(size(tsp2));
        Fe15_sirs = zeros(size(ti));
        Cu19_sirs = zeros(size(ti));
        B5_sirs = zeros(size(ti));
        He2_sirs = zeros(size(ti));
        O8=zeros(size(tsp1));
        O8s=zeros(size(ti));
        O7=zeros(size(tsp1));
        C6=zeros(size(tsp1));
        C6beta=zeros(size(tsp1));
        C6s=zeros(size(ti));
        C6betas=zeros(size(ti));
        C5a=zeros(size(tsp1));
        C5b=zeros(size(tsp1));
    end
else
    
    [dat1,dat2]=ImpVUV (shots(1));
    
        tsp2=dat2.t;   %time from detector 2
        tsp1=dat1.t;   %time form detector 1
        
        Fe15_sir= dat2.FeXV_284; if Fe15_sir == 0; Fe15_sir(1:size(tsp2)) = 0; end
        Cu19_sir=dat2.CuXIX_273; if Cu19_sir == 0; Cu19_sir(1:size(tsp2)) = 0; end
        Fe24_sir=dat2.FeXXIV_255;if Fe24_sir == 0; Fe24_sir(1:size(tsp2)) = 0; end
        He2_sir=dat2.HeII_256; if He2_sir == 0; He2_sir(1:size(tsp2)) = 0; end
        Ni18_sir=dat2.NiXVIII_292; if Ni18_sir == 0; Ni18_sir(1:size(tsp2)) = 0; end
        O8s_sir=dat1.OVIII_19; if O8s_sir == 0; O8s_sir(1:size(tsp1)) = 0; end
        O7_sir=dat1.OVII_21; if O7_sir == 0; O7_sir(1:size(tsp1)) = 0; end
        C6_sir=dat1.CVI_34; if C6_sir == 0; C6_sir(1:size(tsp1)) = 0; end
        C6beta_sir=dat1.CVI_28; if C6beta_sir == 0; C6beta_sir(1:size(tsp1)) = 0; end
        
        %New signal 
        W29_sir = dat1.WXXIX_50; if W29_sir == 0; W29_sir(1:size(tsp1)) = 0; end
        N7_sir = dat1.NVII_25; if N7_sir == 0; N7_sir(1:size(tsp1)) = 0; end
        Mo9_sir = dat2.MoIX_277; if Mo9_sir == 0; Mo9_sir(1:size(tsp2)) = 0; end
        
        W46_sir = dat2.WXLVI_127; if W46_sir == 0; W46_sir(1:size(tsp2)) = 0; end
        W44_sir = dat2.WXLIV_126; if W44_sir == 0; W44_sir(1:size(tsp2)) = 0; end
        W42_sir = dat2.WXLII_139; if W42_sir == 0; W42_sir(1:size(tsp2)) = 0; end
        O6_sir = dat2.OVI_150; if O6_sir == 0; O6_sir(1:size(tsp2)) = 0; end
        B5_sir=dat2.BV_264; if B5_sir == 0; B5_sir(1:size(tsp2)) = 0; end
        
        
      
        %Old signal go to Zero;
        %O4a=zeros(size(tsp2));
        C4_sir=zeros(size(tsp2));
        O4b_sir=zeros(size(tsp2));
        %B5_sir=zeros(size(tsp2));
        B5_sirs = zeros(size(tsp2));    
        C6betas=zeros(size(tsp2));
        C5a=zeros(size(tsp2));
        C5b=zeros(size(tsp2));
end
   
          % Affichage impuretes SIR & SURVIE
    if isempty(tspgl) || isempty(tsp2)
        disp('No SURVIE and SIR data');
        spgl = 0;
    end

dat2.WXXXVIII_129(dat2.WXXXVIII_129<0)=0;
dat2.WXLII_139(dat2.WXLII_139<0)=0;
dat2.WXLVI_127(dat2.WXLVI_127<0)=0;
Fe15(Fe15<0)=0;  Cu19(Cu19<0)=0;

plot(tspgl,Cu19,'r',tspgl,Fe15,'k'); hold on;
plot(dat2.t,dat2.WXXXVIII_129,'m',dat2.t,dat2.WXLII_139,'c',dat2.t,dat2.WXLVI_127,'b');
plot(tspgl,Ag16,'g');
plot(dat2.t,dat2.AgXXXVI_160,'color',[0 0.6 0]);


ylabel('Impurity'); xlim(interval); % ylim([0 12e5]);
legend('Cu^1^9','Fe^1^5','W^3^8','W^4^3','W^4^6','Ag') ;
title('Impurity from SIR & SURVIE') ;
set(gca,'FontSize', 14);


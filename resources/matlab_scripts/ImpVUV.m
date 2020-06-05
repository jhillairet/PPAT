%                        ---- ImpVUV ----
%
%  
%   O. MEYER le 15/11/2018
%
%   Programme de calcul des evolutions temporelles des surfaces nettes des
%   raies du SIR, plot et superposition des courbes choc à choc 
%
%   Appel: [struc1,struc2]=ImpVUV(numchoc)
%
%   Raies traitees:
%
%       O VIII
%       O VII
%       C VI
%       N VII
%       Mo IX
%       Cu XIX
%       Fe XV
%       W XXXIX QC @ 50 A (W38+ to W45+)
%       
%   Sortie:
%
%       - struc1{} data detector1
%                - t
%                - OVIII_19
%                - OVII_21
%                - NVII_25
%                - CVI_34
%                - CVI_28
%                - WXXIX_50
%        
%        - struc2{} data detector 2
%                - t
%                - MoIX_277
%                - CuXIX_273
%                - FeXV_284
%                - FeXXIV_255
%                - NiXVIII_292
%                - HeII_256
%                - WXLVI_127
%                - WXLIV_126
%                - WXLII_139
%                - OVI_150
%                - BV_264
%                - WXXXVIII
%                - Ag XXXVI 
%                
%       
%
%




function [dat1,dat2]=ImpVUV (numchoc)

clr_vec=[[0,0,1];[0,1,1];[1,0,0];[1,0,1];[0,1,0];[0,0,0];[1,1,1]*0.4;[1,1,1]*0.7];

global ListeRaies


%   Definition des raies (A)
ListeRaies={'Raies traitées'};
Ind_OVIII_19=[18.8 19.1];
Ind_OVII_21=[21.45 21.94];
Ind_NVII_25=[24.6 25];
Ind_CVI_34=[33.55 34.13];
Ind_CVI_28=[28.05 28.85];
Ind_CV_40=[40.3 40.7];
Ind_CV_41=[40.85 41.12];
Ind_MoIX_277=[276.5 277.3];
Ind_CuXIX_273=[272.8 273.4];
Ind_FeXV_284=[283.8 284.3];
Ind_WXXIX_50=[44.45 55];
Ind_FeXXIV_255=[254.8 255.4];
Ind_NiXVIII_292=[291.9 292.5];
Ind_HeII_256=[256.1 256.7];
Ind_WXLVI_127=[126.6 127.2];
Ind_WXLIV_126=[125.9 127.4];
Ind_WXXXVIII_129=[129.5 130.1];
Ind_WXLII_139=[138.5 139.1];
Ind_OVI_150=[149.5 150.1];
Ind_BV_264=[264 264.4];
Ind_AgXXXVI_160=[159.7 160.1];


%   Saisie # choc
%numchoc = input('\nShot number : ');

%   Remont??e des donn??es pilotage

% etat vanne
vanne=tsmat(numchoc,'EXP=T=S;DIAGNOSTIC;VSDSIR');
if isempty(vanne)
    disp(' ')
    disp('DIAGNOSTIC VALVE STATUS UNKNOWN')
    vanne=0;
elseif vanne ~=0
    disp(' ')
    disp('	DIAGNOSTIC VALVE CLOSED')
    disp(' ')
    return
else
    disp('	DIAGNOSTIC VALVE OPEN')
end

% donnees spectro
[dect1,dect2,texpo,reseau,statut_osc,trajectoire,HT]=tsmat(numchoc,'DSIR;PILOTAGE;DETECT1',...
        'DSIR;PILOTAGE;DETECT2','DSIR;PILOTAGE;TEXPO',...
        'DSIR;PILOTAGE;RESEAU','DSIR;PILOTAGE;STATUTOSC','DSIR;PILOTAGE;TRAJECTOIRE','DSIR;PILOTAGE;CONSIGNEHT');
    
% donnes datation
t_une = tsmat(numchoc,'UNE|1');
t_ign = tsmat(numchoc,'IGNITRON|1');   
    
%   Remont??e des donn??es physiques

% Remontee spectres sp1, sp2
err_lec_sir = tsrfile(numchoc,'FDSIR1','temp_sir');
if err_lec_sir<0
    disp('lecdonneesciel - SIR data are not in the database for this pulse')
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

err_lec_sir = tsrfile(numchoc,'FDSIR2','temp_sir');
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

%Remontee temps tsp1, tsp2
err_lec_sir = tsrfile(numchoc,'FDATEDSIR1','temp_sir');
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
        tsp1b=tsp1;
    end
    fclose(id_fichier);
end
err_lec_sir = tsrfile(numchoc,'FDATEDSIR2','temp_sir');
if err_lec_sir<0
    disp('lecdonneesciel - t SIR data are not in the database for this pulse')
    tsp2=[];
else
    [id_fichier,message_err_open_fichier] = fopen('temp_sir','r');
    if id_fichier<0
        disp(message_err_open_fichier)
        tsp2=[];
    else
        tsp2 = fread(id_fichier,inf,'uint32');
        tsp2 = tsp2/1e6 - t_ign; % passage en secondesInd_OVII_21
        tsp2b=tsp2;
    end
    fclose(id_fichier);
end

%   Mise en forme des donnees
texpo1=texpo(1)/1000;
texpo2=texpo(2)/1000;

%   Application de l'etalonnage aux detecteurs
lam1=(dect1-180480)/512.06;
lam2=(dect2-798413)/512;

%   
if isempty(t_ign) & ~isempty(t_une)
    t_ign = t_une + 1;
elseif ~isempty(t_ign) & isempty(t_une)
    t_une = t_ign - 1;
elseif isempty(t_ign) & isempty(t_une)
    t_une = 31;
    t_ign = 32;
end

nbpixels = 1340;
nb_spl=(length(sp1)/nbpixels); % floor( ...) retir? 27/11/2007
nb_sgl=(length(sp2)/nbpixels);

% Mise en forme sp2
sp2 = reshape(sp2,1340,nb_sgl);
tsp2=tsp2(1:nb_sgl);
sp2 = flipud(sp2);
sp2=sp2./texpo2;

% Mise en forme sp1
sp1 = reshape(sp1,1340,nb_spl);
tsp1=tsp1(1:nb_spl);
sp1 = flipud(sp1);
sp1=sp1./texpo1;

% Calcul des vecteurs de longueur d'onde
[lamb1,err1] = Convlambda2010(numchoc,1:1340,'s',lam1,reseau);
[lamb2,err2] = Convlambda2010(numchoc,1:1340,'l',lam2,reseau);

% On fixe la couleur de légende au noir
set(0,'defaulttextcolor',[0 0 0]);

% Evolution temporelle O VIII
[OVIII_19]=EvolTemp({'OVIII_19'}, Ind_OVIII_19, lamb1, sp1);

dat1.t=tsp1;
dat1.OVIII_19=OVIII_19;

% Evolution temporelle O VII
[OVII_21]=EvolTemp({'OVII_21'}, Ind_OVII_21, lamb1, sp1);
dat1.OVII_21=OVII_21;

% Evolution temporelle C VI
[CVI_34]=EvolTemp({'CVI_34'}, Ind_CVI_34, lamb1, sp1);

dat1.CVI_34=CVI_34;

% Evolution temporelle C VI (28)
[CVI_28]=EvolTemp({'CVI_28'}, Ind_CVI_28, lamb1, sp1);
dat1.CVI_28=CVI_28;

% Evolution temporelle Mo V
[MoIX_277]=EvolTemp({'MoIX_277'}, Ind_MoIX_277, lamb2, sp2);

dat2.t=tsp2;
dat2.MoIX_277=MoIX_277;

% Evolution temporelle Cu XIX
[CuXIX_273]=EvolTemp({'CuXIX_273'}, Ind_CuXIX_273, lamb2, sp2);

dat2.CuXIX_273=CuXIX_273;

% Evolution temporelle N VII
[NVII_25]=EvolTemp({'NVII_25'}, Ind_NVII_25, lamb1, sp1);

dat1.NVII_25=NVII_25;

% Evolution temporelle Fe XV
[FeXV_284]=EvolTemp({'FeXV_284'}, Ind_FeXV_284, lamb2, sp2);

dat2.FeXV_284=FeXV_284;

% Evolution temporelle W XXIX
[WXXIX_50]=EvolTemp({'WXXIX_WXLVI_50'}, Ind_WXXIX_50, lamb1, sp1);

dat1.WXXIX_50=WXXIX_50;

% Evolution temporelle Fe XXIV
[FeXXIV_255]=EvolTemp({'FeXXIV_255'}, Ind_FeXXIV_255, lamb2, sp2);
dat2.FeXXIV_255=FeXXIV_255;

% Evolution temporelle Ni XVIII
[NiXVIII_292]=EvolTemp({'NiXVIII_292'}, Ind_NiXVIII_292, lamb2, sp2);
dat2.NiXVIII_292=NiXVIII_292;

% Evolution temporelle Fe XXIV
[HeII_256]=EvolTemp({'HeII_256'}, Ind_HeII_256, lamb2, sp2);
dat2.HeII_256=HeII_256;

% Evolution temporelle W XLVI
[WXLVI_127]=EvolTemp({'WXLVI_127'}, Ind_WXLVI_127, lamb2, sp2);
dat2.WXLVI_127=WXLVI_127;

% Evolution temporelle W XXXVII
[WXXXVIII_129]=EvolTemp({'WXXXVIII_129'}, Ind_WXXXVIII_129, lamb2, sp2);
dat2.WXXXVIII_129=WXXXVIII_129;

% Evolution temporelle Ag XXXVI
[AgXXXVI_160]=EvolTemp({'AgXXXVI_160'}, Ind_AgXXXVI_160, lamb2, sp2);
dat2.AgXXXVI_160=AgXXXVI_160;

% Evolution temporelle W XLIV
[WXLIV_126]=EvolTemp({'WXLIV_126'}, Ind_WXLIV_126, lamb2, sp2);
dat2.WXLIV_126=WXLIV_126;

%Evolution temporelle W XLII
[WXLII_139]=EvolTemp({'WXLII_139'}, Ind_WXLII_139, lamb2, sp2);
dat2.WXLII_139=WXLII_139;


%Evolution temporelle O VI
[OVI_150]=EvolTemp({'OVI_150'}, Ind_OVI_150, lamb2, sp2);
dat2.OVI_150=OVI_150;

%Evolution temporelle B V

Ind_BV_264=[264 264.4];
[BV_264]=EvolTemp({'BV_264'}, Ind_BV_264, lamb2, sp2);
dat2.BV_264=BV_264;

disp(ListeRaies);
end

function [SurfNette]=EvolTemp(Raie, Indices, Lamb, sp)

global ListeRaies

ind2=find(Lamb<Indices(1));
if isempty(ind2)
%     disp(Raie);
%     disp('non disponible');
    SurfNette=0;
    return;
else
    ind2=max(ind2);
end
ind5=find(Lamb>Indices(2));
if isempty(ind5)
%     disp(Raie);
%     disp('non disponible');
    SurfNette=0;
    return;
else
    ind5=min(ind5);
end
ind1=ind2-3;
ind3=ind2;
ind4=ind5;
ind6=ind5+3;
i=size(ListeRaies);
ListeRaies(i(2)+1)=Raie;
SurfNette=surfn(sp,ind1,ind2,ind3,ind4,ind5,ind6);
end

function [surface]=surfn(sp,ind1,ind2,ind3,ind4,ind5,ind6)

surface=sum(sp(ind3:ind4,:),1)-(sum(sp(ind1:ind2,:),1)+sum(sp(ind5:ind6,:),1))/(ind2-ind1+ind6-ind5+2)*(ind4-ind3+1);
end

function [Lambda,err_mess] = Convlambda2010(numchoc,pixels,detector,spec_position,rezo)


if rezo == 1
    N = 300;
else
    N = 600;
end
% disp(sprintf('	RESEAU = %d',rezo));
% disp(sprintf('	trait/mm = %d',N));
% disp(detector);
%******************* PARAMETERS **************
%%N=600;               % unit:l/mm -- N grating groove density
R=2000;              % unit:mm   -- R grating radius (Rowland Circle)
l=1062.7;            % unit:mm   -- l distance OJ betwen swivel joint center and rowland circle center
h=49.8;              % unit:mm   -- h height of nut pivot above Rowland circle
xl=478.8;            % unit:mm   -- arc from grating
xs=29;               % unit:mm   --
alpha=(1.5*pi)/180;  % unit:rad  -- angle d'incidence
n=50;                % unit:   --  nbr of pixel per unit lengt on PDA or MCD etector

if detector=='l'
    M=1.740;             % unit:     -- fiber optic taper magnification
    yc=455.7;            % unit:mm   -- calibration constant
    p0=673;              % unit:   -- central pixel N� od PDA or CCD
else
    M=1.730;             % unit:     -- fiber optic taper magnification for pl
    yc=453.7;            % unit:mm   -- calibration constant
    p0=705;             % unit:   -- central pixel N� od PDA or CCD
end


%******************* VARIABLES / FUNCTIONS **************

y=[0:400];            % unit:mm --position of SCD or MCD
lambda0=[0:350];      % unit:   ---Agmtrom  --wavelengt
%%%x0=[52:480];            % unit:mm --arc along rowland circle
p=pixels;            % unit:   ---pixel number on ccd or pda

%*******************   x0=f(y0) y0:position du chariot                    **********

KK=(-(yc-spec_position)^2+l*l+(R/2+h)^2)/(2*l*(R/2+h));
x0=xl-xs-(R/2*acos(KK));


%*******************   wavelengt as a function of pixel                    **********

b0=x0/R;
z0=(R*n)./((p-p0)*M);
k0=acot(cot(b0)+z0);

Lambda=1E7/N*(cos(alpha)-cos(b0+k0));
err_mess=1;
%figure
%plot(p,Lambda,'r');
end

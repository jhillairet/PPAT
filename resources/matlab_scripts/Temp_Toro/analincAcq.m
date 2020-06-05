function [conversion]=conv(nom_capteur,tension); 

%Cette fonction renvoie un fichier converti en unite physique
% Utilisation possible :
% 	Analyseur d'incident
%	Conversion de donnees

%Programme réalisé par Manuel TENA en juillet 1996
%		Modifié en MARS 1998

% Temperature jonction verticale bobine 16

if strcmp(nom_capteur,'tjv16')
	% a=max(tension);
	% b=min(tension);
	  if ( tension > 5 ) 	
	    % disp('Hors gamme');
	    conversion=tension;
	    else
      XX(1)=37.840;
      XX(2)=28.674;
      XX(3)=23.176;
      XX(4)=19.545;
      XX(5)=15.966;
      XX(6)=12.457; 
      XX(7)=10.393; 
      XX(8)=8.003; 
      XX(9)=6.743;              
      XX(10)=5.936;
      XX(11)=5.370;
      XX(12)=4.775;
      XX(13)=4.481;
      XX(14)=4.042;
      XX(15)=3.727;
      XX(16)=3.298; 
      XX(17)=2.903; 
      XX(18)=2.377; 
      XX(19)=2.198;              
      XX(20)=2.068;
      XX(21)=1.888; 
      XX(22)=1.766; 
      XX(23)=1.676; 
      XX(24)=1.586;              
      XX(25)=1.541;             
      XX(26)=1.496;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=450;
      YY(9)=550;
      YY(10)=650;
      YY(11)=750;
      YY(12)=900;
      YY(13)=1000;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1800;
      YY(17)=2400;
      YY(18)=4000;
      YY(19)=5000;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.; 
  end          	
end


% Pression froide bobine 13

if strcmp(nom_capteur,'pfbt13')
     
    conversion=20*(tension-1)/4;

end 


% Pression chaude bobine 16 9 capteur relatif

if strcmp(nom_capteur,'pcbt16')

    conversion=(3.5*(tension-1)/4)+1;

end 

% mesure avec LEM 10A

if strcmp(nom_capteur,'lem10')
conversion = ((tension - 3)/ 0.2) ;

end

% mesure avec LEM 100A

if strcmp(nom_capteur,'lem100')
conversion = ((tension - 3)/ 0.02) ;

end

% Temperature jonction verticale 13

   if strcmp(nom_capteur,'tjv13')
	%a=max(tension);
	 %b=min(tension);
	    if (tension > 5) 
	      % disp('Hors gamme');
	      conversion=tension;
	    else
      XX(1)=41.531;
      XX(2)=31.365;
      XX(3)=25.261;
      XX(4)=21.235;
      XX(5)=17.275;
      XX(6)=13.407; 
      XX(7)=11.140; 
      XX(8)=8.498; 
      XX(9)=7.139;              
      XX(10)=6.272;
      XX(11)=5.666;
      XX(12)=5.030;
      XX(13)=4.717;
      XX(14)=4.251;
      XX(15)=3.916;
      XX(16)=3.460; 
      XX(17)=3.042; 
      XX(18)=2.486; 
      XX(19)=2.296;              
      XX(20)=2.159;
      XX(21)=1.969; 
      XX(22)=1.840; 
      XX(23)=1.746; 
      XX(24)=1.653;              
      XX(25)=1.606;             
      XX(26)=1.558;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=450;
      YY(9)=550;
      YY(10)=650;
      YY(11)=750;
      YY(12)=900;
      YY(13)=1000;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1800;
      YY(17)=2400;
      YY(18)=4000;
      YY(19)=5000;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
  end          	
end

% Temperature echangeur bobine 17

if strcmp(nom_capteur,'tebt17')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.631;
      XX(2)=27.413;
      XX(3)=22.387;
      XX(4)=19.019;
      XX(5)=15.655;
      XX(6)=12.309; 
      XX(7)=10.314; 
      XX(8)=7.882; 
      XX(9)=6.582;              
      XX(10)=5.764;
      XX(11)=5.197;
      XX(12)=4.779;
      XX(13)=4.355;
      XX(14)=4.038;
      XX(15)=3.720;
      XX(16)=3.206; 
      XX(17)=2.843; 
      XX(18)=2.489; 
      XX(19)=2.247;              
      XX(20)=2.064;
      XX(21)=1.889; 
      XX(22)=1.770; 
      XX(23)=1.684; 
      XX(24)=1.616;              
      XX(25)=1.588;             
      XX(26)=1.562;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature echangeur bobine 16

if strcmp(nom_capteur,'tebt16')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else

      XX(1)=36.474;
      XX(2)=27.835;
      XX(3)=22.625;
      XX(4)=19.163;
      XX(5)=15.728;
      XX(6)=12.333; 
      XX(7)=10.319; 
      XX(8)=7.873; 
      XX(9)=6.569;              
      XX(10)=5.750;
      XX(11)=5.183;
      XX(12)=4.765;
      XX(13)=4.341;
      XX(14)=4.025;
      XX(15)=3.707;
      XX(16)=3.194; 
      XX(17)=2.832; 
      XX(18)=2.479; 
      XX(19)=2.238;              
      XX(20)=2.056;
      XX(21)=1.881; 
      XX(22)=1.764; 
      XX(23)=1.677; 
      XX(24)=1.610;              
      XX(25)=1.581;             
      XX(26)=1.556;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature echangeur bobine 13

if strcmp(nom_capteur,'tebt13')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=34.930;
      XX(2)=26.870;
      XX(3)=21.964;
      XX(4)=18.683;
      XX(5)=15.407;
      XX(6)=12.147; 
      XX(7)=10.200; 
      XX(8)=7.822; 
      XX(9)=6.546;              
      XX(10)=5.742;
      XX(11)=5.184;
      XX(12)=4.772;
      XX(13)=4.353;
      XX(14)=4.040;
      XX(15)=3.725;
      XX(16)=3.216; 
      XX(17)=2.855; 
      XX(18)=2.503; 
      XX(19)=2.262;              
      XX(20)=2.080;
      XX(21)=1.904; 
      XX(22)=1.786; 
      XX(23)=1.699; 
      XX(24)=1.632;              
      XX(25)=1.603;             
      XX(26)=1.577;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end        	
end

% Temperature Amenee de courant bobine 18

if strcmp(nom_capteur,'tabt18')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.466;
      XX(2)=25.955;
      XX(3)=21.320;
      XX(4)=18.193;
      XX(5)=15.050;
      XX(6)=11.901; 
      XX(7)=10.011; 
      XX(8)=7.692; 
      XX(9)=6.444;              
      XX(10)=5.656;
      XX(11)=5.109;
      XX(12)=4.703;
      XX(13)=4.292;
      XX(14)=3.984;
      XX(15)=3.674;
      XX(16)=3.173; 
      XX(17)=2.818; 
      XX(18)=2.470; 
      XX(19)=2.233;              
      XX(20)=2.053;
      XX(21)=1.880; 
      XX(22)=1.764; 
      XX(23)=1.678; 
      XX(24)=1.611;              
      XX(25)=1.583;             
      XX(26)=1.558;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 17
% Attention le 15/01/98 remplacement tabt17 par tjv17
if strcmp(nom_capteur,'tabt17')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=40.218;
      XX(2)=29.970;
      XX(3)=24.081;
      XX(4)=20.273;
      XX(5)=16.565;
      XX(6)=12.960; 
      XX(7)=10.843; 
      XX(8)=8.453; 
      XX(9)=7.126;              
      XX(10)=6.274;
      XX(11)=5.675;
      XX(12)=5.044;
      XX(13)=4.732;
      XX(14)=4.267;
      XX(15)=3.933;
      XX(16)=3.477; 
      XX(17)=3.058; 
      XX(18)=2.501; 
      XX(19)=2.311;              
      XX(20)=2.173;
      XX(21)=1.984; 
      XX(22)=1.855; 
      XX(23)=1.761; 
      XX(24)=1.687;              
      XX(25)=1.656;             
      XX(26)=1.627;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=450;
      YY(9)=550;
      YY(10)=650;
      YY(11)=750;
      YY(12)=900;
      YY(13)=1000;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1800;
      YY(17)=2400;
      YY(18)=4000;
      YY(19)=5000;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 16

if strcmp(nom_capteur,'tabt16')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.534;
      XX(2)=26.679;
      XX(3)=21.848;
      XX(4)=18.599;
      XX(5)=15.343;
      XX(6)=12.092; 
      XX(7)=10.148; 
      XX(8)=7.772; 
      XX(9)=6.498;              
      XX(10)=5.695;
      XX(11)=5.139;
      XX(12)=4.727;
      XX(13)=4.310;
      XX(14)=3.998;
      XX(15)=3.684;
      XX(16)=3.178; 
      XX(17)=2.819; 
      XX(18)=2.469; 
      XX(19)=2.230;              
      XX(20)=2.050;
      XX(21)=1.876; 
      XX(22)=1.759; 
      XX(23)=1.673; 
      XX(24)=1.606;              
      XX(25)=1.578;             
      XX(26)=1.552;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 15

if strcmp(nom_capteur,'tabt15')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.543;
      XX(2)=27.321;
      XX(3)=22.304;
      XX(4)=18.946;
      XX(5)=15.594;
      XX(6)=12.262; 
      XX(7)=10.277; 
      XX(8)=7.856; 
      XX(9)=6.562;              
      XX(10)=5.747;
      XX(11)=5.183;
      XX(12)=4.766;
      XX(13)=4.344;
      XX(14)=4.029;
      XX(15)=3.712;
      XX(16)=3.200; 
      XX(17)=2.838; 
      XX(18)=2.485; 
      XX(19)=2.244;              
      XX(20)=2.062;
      XX(21)=1.886; 
      XX(22)=1.768; 
      XX(23)=1.682; 
      XX(24)=1.614;              
      XX(25)=1.586;             
      XX(26)=1.560;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 14

if strcmp(nom_capteur,'tabt14')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.407;
      XX(2)=27.844;
      XX(3)=22.661;
      XX(4)=19.211;
      XX(5)=15.780;
      XX(6)=12.384; 
      XX(7)=10.366; 
      XX(8)=7.914; 
      XX(9)=6.604;              
      XX(10)=5.782;
      XX(11)=5.213;
      XX(12)=4.792;
      XX(13)=4.367;
      XX(14)=4.049;
      XX(15)=3.729;
      XX(16)=3.214; 
      XX(17)=2.850; 
      XX(18)=2.495; 
      XX(19)=2.253;              
      XX(20)=2.070;
      XX(21)=1.893; 
      XX(22)=1.775; 
      XX(23)=1.688; 
      XX(24)=1.620;              
      XX(25)=1.592;             
      XX(26)=1.566;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 13

  if strcmp(nom_capteur,'tabt13')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.661;
      XX(2)=27.425;
      XX(3)=22.399;
      XX(4)=19.035;
      XX(5)=15.676;
      XX(6)=12.335; 
      XX(7)=10.342; 
      XX(8)=7.913; 
      XX(9)=6.612;              
      XX(10)=5.793;
      XX(11)=5.226;
      XX(12)=4.807;
      XX(13)=4.382;
      XX(14)=4.064;
      XX(15)=3.745;
      XX(16)=3.229; 
      XX(17)=2.865; 
      XX(18)=2.509; 
      XX(19)=2.266;              
      XX(20)=2.082;
      XX(21)=1.906; 
      XX(22)=1.787; 
      XX(23)=1.699; 
      XX(24)=1.631;              
      XX(25)=1.603;             
      XX(26)=1.577;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 12

if strcmp(nom_capteur,'tabt12')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=36.264;
      XX(2)=28.06;
      XX(3)=22.965;
      XX(4)=19.525;
      XX(5)=16.070;
      XX(6)=12.621; 
      XX(7)=10.561; 
      XX(8)=8.051; 
      XX(9)=6.710;              
      XX(10)=5.868;
      XX(11)=5.285;
      XX(12)=4.855;
      XX(13)=4.419;
      XX(14)=4.094;
      XX(15)=3.768;
      XX(16)=3.243; 
      XX(17)=2.872; 
      XX(18)=2.511; 
      XX(19)=2.265;              
      XX(20)=2.079;
      XX(21)=1.900; 
      XX(22)=1.780; 
      XX(23)=1.692; 
      XX(24)=1.624;              
      XX(25)=1.595;             
      XX(26)=1.569;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 11

if strcmp(nom_capteur,'tabt11')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=34.954;
      XX(2)=27.087;
      XX(3)=22.219;
      XX(4)=18.934;
      XX(5)=15.632;
      XX(6)=12.329; 
      XX(7)=10.350; 
      XX(8)=7.928; 
      XX(9)=6.628;              
      XX(10)=5.809;
      XX(11)=5.241;
      XX(12)=4.821;
      XX(13)=4.395;
      XX(14)=4.077;
      XX(15)=3.757;
      XX(16)=3.240; 
      XX(17)=2.874; 
      XX(18)=2.517; 
      XX(19)=2.273;              
      XX(20)=2.089;
      XX(21)=1.911; 
      XX(22)=1.792; 
      XX(23)=1.704; 
      XX(24)=1.636;              
      XX(25)=1.607;             
      XX(26)=1.581;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 10

if strcmp(nom_capteur,'tabt10')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=36.424;
      XX(2)=27.691;
      XX(3)=22.440;
      XX(4)=18.961;
      XX(5)=15.518;
      XX(6)=12.128; 
      XX(7)=10.123; 
      XX(8)=7.698; 
      XX(9)=6.409;              
      XX(10)=5.602;
      XX(11)=5.044;
      XX(12)=4.633;
      XX(13)=4.217;
      XX(14)=3.907;
      XX(15)=3.596;
      XX(16)=3.095; 
      XX(17)=2.741; 
      XX(18)=2.397; 
      XX(19)=2.163;              
      XX(20)=1.986;
      XX(21)=1.815; 
      XX(22)=1.701; 
      XX(23)=1.617; 
      XX(24)=1.552;              
      XX(25)=1.524;             
      XX(26)=1.499;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 09

if strcmp(nom_capteur,'tabt09')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.519;
      XX(2)=27.119;
      XX(3)=22.066;
      XX(4)=18.712;
      XX(5)=15.384;
      XX(6)=12.091; 
      XX(7)=10.134; 
      XX(8)=7.754; 
      XX(9)=6.481;              
      XX(10)=5.680;
      XX(11)=5.126;
      XX(12)=4.716;
      XX(13)=4.300;
      XX(14)=3.990;
      XX(15)=3.677;
      XX(16)=3.173; 
      XX(17)=2.816; 
      XX(18)=2.467; 
      XX(19)=2.229;              
      XX(20)=2.049;
      XX(21)=1.876; 
      XX(22)=1.759; 
      XX(23)=1.674; 
      XX(24)=1.607;              
      XX(25)=1.579;             
      XX(26)=1.553;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end

% Temperature Amenee de courant bobine 08

if strcmp(nom_capteur,'tabt08')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.738;
      XX(2)=27.594;
      XX(3)=22.570;
      XX(4)=19.189;
      XX(5)=15.799;
      XX(6)=12.420; 
      XX(7)=10.403; 
      XX(8)=7.943; 
      XX(9)=6.627;              
      XX(10)=5.800;
      XX(11)=5.227;
      XX(12)=4.804;
      XX(13)=4.376;
      XX(14)=4.056;
      XX(15)=3.735;
      XX(16)=3.217; 
      XX(17)=2.851; 
      XX(18)=2.494; 
      XX(19)=2.251;              
      XX(20)=2.067;
      XX(21)=1.891; 
      XX(22)=1.772; 
      XX(23)=1.685; 
      XX(24)=1.617;              
      XX(25)=1.588;             
      XX(26)=1.562;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end         	
end

% Temperature Amenee de courant bobine 07

if strcmp(nom_capteur,'tabt07')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=36.180;
      XX(2)=27.863;
      XX(3)=22.744;
      XX(4)=19.306;
      XX(5)=15.867;
      XX(6)=12.447; 
      XX(7)=10.410; 
      XX(8)=7.932; 
      XX(9)=6.610;              
      XX(10)=5.780;
      XX(11)=5.206;
      XX(12)=4.782;
      XX(13)=4.353;
      XX(14)=4.034;
      XX(15)=3.713;
      XX(16)=3.195; 
      XX(17)=2.830; 
      XX(18)=2.474; 
      XX(19)=2.232;              
      XX(20)=2.049;
      XX(21)=1.874; 
      XX(22)=1.755; 
      XX(23)=1.669; 
      XX(24)=1.601;              
      XX(25)=1.573;             
      XX(26)=1.547;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 06

if strcmp(nom_capteur,'tabt06')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=36.985;
      XX(2)=28.472;
      XX(3)=23.24;
      XX(4)=19.729;
      XX(5)=16.218;
      XX(6)=12.727; 
      XX(7)=10.648; 
      XX(8)=8.117; 
      XX(9)=6.767;              
      XX(10)=5.919;
      XX(11)=5.332;
      XX(12)=4.899;
      XX(13)=4.461;
      XX(14)=4.133;
      XX(15)=3.805;
      XX(16)=3.276; 
      XX(17)=2.902; 
      XX(18)=2.538; 
      XX(19)=2.290;              
      XX(20)=2.103;
      XX(21)=1.922; 
      XX(22)=1.801; 
      XX(23)=1.712; 
      XX(24)=1.644;              
      XX(25)=1.614;             
      XX(26)=1.588;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 05

if strcmp(nom_capteur,'tabt05')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=38.156;
      XX(2)=29.481;
      XX(3)=23.973;
      XX(4)=20.294;
      XX(5)=16.634;
      XX(6)=13.011; 
      XX(7)=10.863; 
      XX(8)=8.258; 
      XX(9)=6.873;              
      XX(10)=6.005;
      XX(11)=5.405;
      XX(12)=4.963;
      XX(13)=4.517;
      XX(14)=4.183;
      XX(15)=3.849;
      XX(16)=3.311; 
      XX(17)=2.931; 
      XX(18)=2.562; 
      XX(19)=2.310;              
      XX(20)=2.120;
      XX(21)=1.938; 
      XX(22)=1.816; 
      XX(23)=1.726; 
      XX(24)=1.656;              
      XX(25)=1.626;             
      XX(26)=1.600;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 04

if strcmp(nom_capteur,'tabt04')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=41.277;
      XX(2)=31.253;
      XX(3)=25.240;
      XX(4)=21.266;
      XX(5)=17.345;
      XX(6)=13.500; 
      XX(7)=11.235; 
      XX(8)=8.507; 
      XX(9)=7.064;              
      XX(10)=6.163;
      XX(11)=5.542;
      XX(12)=5.084;
      XX(13)=4.623;
      XX(14)=4.279;
      XX(15)=3.934;
      XX(16)=3.380; 
      XX(17)=2.990; 
      XX(18)=2.611; 
      XX(19)=2.354;              
      XX(20)=2.159;
      XX(21)=1.973; 
      XX(22)=1.848; 
      XX(23)=1.756; 
      XX(24)=1.684;              
      XX(25)=1.654;             
      XX(26)=1.627;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 03

if strcmp(nom_capteur,'tabt03')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=38.101;
      XX(2)=28.890;
      XX(3)=23.376;
      XX(4)=19.733;
      XX(5)=16.134;
      XX(6)=12.598; 
      XX(7)=10.510; 
      XX(8)=7.987; 
      XX(9)=6.648;              
      XX(10)=5.809;
      XX(11)=5.230;
      XX(12)=4.804;
      XX(13)=4.372;
      XX(14)=4.050;
      XX(15)=3.728;
      XX(16)=3.208; 
      XX(17)=2.841; 
      XX(18)=2.484; 
      XX(19)=2.241;              
      XX(20)=2.058;
      XX(21)=1.881; 
      XX(22)=1.763; 
      XX(23)=1.676; 
      XX(24)=1.608;              
      XX(25)=1.579;             
      XX(26)=1.554;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end          	
end


% Temperature Amenee de courant bobine 02

if strcmp(nom_capteur,'tabt02')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=39.613;
      XX(2)=30.007;
      XX(3)=24.254;
      XX(4)=20.454;
      XX(5)=16.703;
      XX(6)=13.021; 
      XX(7)=10.850; 
      XX(8)=8.231; 
      XX(9)=6.843;              
      XX(10)=5.975;
      XX(11)=5.376;
      XX(12)=4.935;
      XX(13)=4.489;
      XX(14)=4.157;
      XX(15)=3.824;
      XX(16)=3.288; 
      XX(17)=2.911; 
      XX(18)=2.544; 
      XX(19)=2.294;              
      XX(20)=2.105;
      XX(21)=1.924; 
      XX(22)=1.802; 
      XX(23)=1.713; 
      XX(24)=1.644;              
      XX(25)=1.614;             
      XX(26)=1.588;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
     end  
     end       	

% Temperature Amenee de courant bobine 01

if strcmp(nom_capteur,'tabt01')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=35.371;
      XX(2)=27.301;
      XX(3)=22.327;
      XX(4)=18.981;
      XX(5)=15.630;
      XX(6)=12.289; 
      XX(7)=10.294; 
      XX(8)=7.862; 
      XX(9)=6.561;              
      XX(10)=5.743;
      XX(11)=5.176;
      XX(12)=4.758;
      XX(13)=4.334;
      XX(14)=4.018;
      XX(15)=3.700;
      XX(16)=3.187; 
      XX(17)=2.825; 
      XX(18)=2.472; 
      XX(19)=2.231;              
      XX(20)=2.049;
      XX(21)=1.874; 
      XX(22)=1.756; 
      XX(23)=1.670; 
      XX(24)=1.603;              
      XX(25)=1.575;             
      XX(26)=1.549;	
      YY(1)=160;
      YY(2)=180;
      YY(3)=200;
      YY(4)=220;
      YY(5)=250;
      YY(6)=300;
      YY(7)=350;
      YY(8)=460;
      YY(9)=570;
      YY(10)=680;
      YY(11)=790;
      YY(12)=900;
      YY(13)=1050;
      YY(14)=1200;
      YY(15)=1400;
      YY(16)=1900;
      YY(17)=2500;
      YY(18)=3500;
      YY(19)=4650;
      YY(20)=6000;
      YY(21)=8000;
      YY(22)=10000;
      YY(23)=12000;
      YY(24)=14000;
      YY(25)=15000;
      YY(26)=16000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/15000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
     end         	
	end
% Temperature, Niveau liquide NL18A

if strcmp(nom_capteur,'eans18a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=90.315;
      XX(2)=76.471;
      XX(3)=66.153;
      XX(4)=58.203;
      XX(5)=51.915;
      XX(6)=46.830; 
      XX(7)=42.645; 
      XX(8)=36.182; 
      XX(9)=31.447;              
      XX(10)=27.841;
      XX(11)=25.013;
      XX(12)=22.740;
      XX(13)=20.875;
      XX(14)=19.320;
      XX(15)=18.005;
      XX(16)=16.878; 
      XX(17)=15.903; 
      XX(18)=12.501; 
      XX(19)=10.471;              
      XX(20)=9.195;
      XX(21)=8.213; 
      XX(22)=7.475; 
      XX(23)=6.898; 
      XX(24)=6.435;              
      XX(25)=6.054;             
      XX(26)=5.734;
      XX(27)=5.462;
      XX(28)=5.227;
      XX(29)=5.022;
      XX(30)=4.842;
      XX(31)=4.681;
      XX(32)=4.537; 
      XX(33)=4.084; 
      XX(34)=3.761; 
      XX(35)=3.516;              
      XX(36)=3.323;
      XX(37)=3.167;
      XX(38)=3.036;
      XX(39)=2.926;
      XX(40)=2.831;
      XX(41)=2.748;
      XX(42)=2.675; 
      XX(43)=2.407; 
      XX(44)=2.232; 
      XX(45)=2.108;              
      XX(46)=2.013;
      XX(47)=1.937; 
      XX(48)=1.875; 
      XX(49)=1.823; 
      XX(50)=1.779;              
      XX(51)=1.740;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
      
  % Conversion valeur ohmique en tension    
      ZZ=(YY*4/10000)+1;
 
    

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL18B ( Modifier les valeurs ou entrer l'équation ...)

if strcmp(nom_capteur,'eans18b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=90.315;
      XX(2)=76.471;
      XX(3)=66.153;
      XX(4)=58.203;
      XX(5)=51.915;
      XX(6)=46.830; 
      XX(7)=42.645; 
      XX(8)=36.182; 
      XX(9)=31.447;              
      XX(10)=27.841;
      XX(11)=25.013;
      XX(12)=22.740;
      XX(13)=20.875;
      XX(14)=19.320;
      XX(15)=18.005;
      XX(16)=16.878; 
      XX(17)=15.903; 
      XX(18)=12.501; 
      XX(19)=10.471;              
      XX(20)=9.195;
      XX(21)=8.213; 
      XX(22)=7.475; 
      XX(23)=6.898; 
      XX(24)=6.435;              
      XX(25)=6.054;             
      XX(26)=5.734;
      XX(27)=5.462;
      XX(28)=5.227;
      XX(29)=5.022;
      XX(30)=4.842;
      XX(31)=4.681;
      XX(32)=4.537; 
      XX(33)=4.084; 
      XX(34)=3.761; 
      XX(35)=3.516;              
      XX(36)=3.323;
      XX(37)=3.167;
      XX(38)=3.036;
      XX(39)=2.926;
      XX(40)=2.831;
      XX(41)=2.748;
      XX(42)=2.675; 
      XX(43)=2.407; 
      XX(44)=2.232; 
      XX(45)=2.108;              
      XX(46)=2.013;
      XX(47)=1.937; 
      XX(48)=1.875; 
      XX(49)=1.823; 
      XX(50)=1.779;              
      XX(51)=1.740;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL17A

if strcmp(nom_capteur,'eans17a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=92.827;
      XX(2)=77.864;
      XX(3)=66.864;
      XX(4)=58.482;
      XX(5)=51.910;
      XX(6)=46.636; 
      XX(7)=42.322; 
      XX(8)=35.714; 
      XX(9)=30.912;              
      XX(10)=27.281;
      XX(11)=24.447;
      XX(12)=22.180;
      XX(13)=20.328;
      XX(14)=18.788;
      XX(15)=17.489;
      XX(16)=16.379; 
      XX(17)=15.420; 
      XX(18)=12.091; 
      XX(19)=10.116;              
      XX(20)=8.856;
      XX(21)=7.912; 
      XX(22)=7.203; 
      XX(23)=6.651; 
      XX(24)=6.207;              
      XX(25)=5.842;             
      XX(26)=5.537;
      XX(27)=5.276;
      XX(28)=5.052;
      XX(29)=4.856;
      XX(30)=4.683;
      XX(31)=4.530;
      XX(32)=4.392; 
      XX(33)=3.959; 
      XX(34)=3.649; 
      XX(35)=3.415;              
      XX(36)=3.231;
      XX(37)=3.081;
      XX(38)=2.956;
      XX(39)=2.850;
      XX(40)=2.759;
      XX(41)=2.679;
      XX(42)=2.609; 
      XX(43)=2.351; 
      XX(44)=2.184; 
      XX(45)=2.064;              
      XX(46)=1.972;
      XX(47)=1.899; 
      XX(48)=1.840; 
      XX(49)=1.789; 
      XX(50)=1.746;              
      XX(51)=1.709;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL17B ( modifier les valeurs...)

if strcmp(nom_capteur,'eans17b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=92.827;
      XX(2)=77.864;
      XX(3)=66.864;
      XX(4)=58.482;
      XX(5)=51.910;
      XX(6)=46.636; 
      XX(7)=42.322; 
      XX(8)=35.714; 
      XX(9)=30.912;              
      XX(10)=27.281;
      XX(11)=24.447;
      XX(12)=22.180;
      XX(13)=20.328;
      XX(14)=18.788;
      XX(15)=17.489;
      XX(16)=16.379; 
      XX(17)=15.420; 
      XX(18)=12.091; 
      XX(19)=10.116;              
      XX(20)=8.856;
      XX(21)=7.912; 
      XX(22)=7.203; 
      XX(23)=6.651; 
      XX(24)=6.207;              
      XX(25)=5.842;             
      XX(26)=5.537;
      XX(27)=5.276;
      XX(28)=5.052;
      XX(29)=4.856;
      XX(30)=4.683;
      XX(31)=4.530;
      XX(32)=4.392; 
      XX(33)=3.959; 
      XX(34)=3.649; 
      XX(35)=3.415;              
      XX(36)=3.231;
      XX(37)=3.081;
      XX(38)=2.956;
      XX(39)=2.850;
      XX(40)=2.759;
      XX(41)=2.679;
      XX(42)=2.609; 
      XX(43)=2.351; 
      XX(44)=2.184; 
      XX(45)=2.064;              
      XX(46)=1.972;
      XX(47)=1.899; 
      XX(48)=1.840; 
      XX(49)=1.789; 
      XX(50)=1.746;              
      XX(51)=1.709;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL16A

if strcmp(nom_capteur,'eans16a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=105.734;
      XX(2)=88.316;
      XX(3)=75.510;
      XX(4)=65.769;
      XX(5)=58.151;
      XX(6)=52.057; 
      XX(7)=47.089; 
      XX(8)=39.511; 
      XX(9)=34.039;              
      XX(10)=29.924;
      XX(11)=26.728;
      XX(12)=24.183;
      XX(13)=22.111;
      XX(14)=20.394;
      XX(15)=18.951;
      XX(16)=17.720; 
      XX(17)=16.660; 
      XX(18)=13.001; 
      XX(19)=10.846;              
      XX(20)=9.426;
      XX(21)=8.418; 
      XX(22)=7.663; 
      XX(23)=7.075; 
      XX(24)=6.604;              
      XX(25)=6.216;             
      XX(26)=5.891;
      XX(27)=5.614;
      XX(28)=5.376;
      XX(29)=5.167;
      XX(30)=4.983;
      XX(31)=4.819;
      XX(32)=4.673; 
      XX(33)=4.210; 
      XX(34)=3.878; 
      XX(35)=3.626;              
      XX(36)=3.427;
      XX(37)=3.265;
      XX(38)=3.130;
      XX(39)=3.015;
      XX(40)=2.915;
      XX(41)=2.828;
      XX(42)=2.751; 
      XX(43)=2.467; 
      XX(44)=2.280; 
      XX(45)=2.145;              
      XX(46)=2.041;
      XX(47)=1.957; 
      XX(48)=1.889; 
      XX(49)=1.831; 
      XX(50)=1.780;              
      XX(51)=1.737;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
     end
end
% Temperature, Niveau liquide NL16B

if strcmp(nom_capteur,'eans16b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=105.734;
      XX(2)=88.316;
      XX(3)=75.510;
      XX(4)=65.769;
      XX(5)=58.151;
      XX(6)=52.057; 
      XX(7)=47.089; 
      XX(8)=39.511; 
      XX(9)=34.039;              
      XX(10)=29.924;
      XX(11)=26.728;
      XX(12)=24.183;
      XX(13)=22.111;
      XX(14)=20.394;
      XX(15)=18.951;
      XX(16)=17.720; 
      XX(17)=16.660; 
      XX(18)=13.001; 
      XX(19)=10.846;              
      XX(20)=9.426;
      XX(21)=8.418; 
      XX(22)=7.663; 
      XX(23)=7.075; 
      XX(24)=6.604;              
      XX(25)=6.216;             
      XX(26)=5.891;
      XX(27)=5.614;
      XX(28)=5.376;
      XX(29)=5.167;
      XX(30)=4.983;
      XX(31)=4.819;
      XX(32)=4.673; 
      XX(33)=4.210; 
      XX(34)=3.878; 
      XX(35)=3.626;              
      XX(36)=3.427;
      XX(37)=3.265;
      XX(38)=3.130;
      XX(39)=3.015;
      XX(40)=2.915;
      XX(41)=2.828;
      XX(42)=2.751; 
      XX(43)=2.467; 
      XX(44)=2.280; 
      XX(45)=2.145;              
      XX(46)=2.041;
      XX(47)=1.957; 
      XX(48)=1.889; 
      XX(49)=1.831; 
      XX(50)=1.780;              
      XX(51)=1.737;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL15A

if strcmp(nom_capteur,'eans15a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.248;
      XX(2)=68.692;
      XX(3)=59.872;
      XX(4)=52.961;
      XX(5)=47.425;
      XX(6)=42.906; 
      XX(7)=39.159; 
      XX(8)=33.328; 
      XX(9)=29.024;              
      XX(10)=25.731;
      XX(11)=23.139;
      XX(12)=21.050;
      XX(13)=19.335;
      XX(14)=17.903;
      XX(15)=16.690;
      XX(16)=15.651; 
      XX(17)=14.750; 
      XX(18)=11.609; 
      XX(19)=9.733;              
      XX(20)=8.486;
      XX(21)=7.595; 
      XX(22)=6.925; 
      XX(23)=6.401; 
      XX(24)=5.980;              
      XX(25)=5.633;             
      XX(26)=5.341;
      XX(27)=5.093;
      XX(28)=4.878;
      XX(29)=4.690;
      XX(30)=4.525;
      XX(31)=4.377;
      XX(32)=4.245; 
      XX(33)=3.826; 
      XX(34)=3.526; 
      XX(35)=3.298;              
      XX(36)=3.118;
      XX(37)=2.970;
      XX(38)=2.848;
      XX(39)=2.743;
      XX(40)=2.653;
      XX(41)=2.574;
      XX(42)=2.504; 
      XX(43)=2.245; 
      XX(44)=2.075; 
      XX(45)=1.952;              
      XX(46)=1.857;
      XX(47)=1.782; 
      XX(48)=1.719; 
      XX(49)=1.666; 
      XX(50)=1.620;              
      XX(51)=1.580;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL15B (valeurs a modifier )

if strcmp(nom_capteur,'eans15b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.248;
      XX(2)=68.692;
      XX(3)=59.872;
      XX(4)=52.961;
      XX(5)=47.425;
      XX(6)=42.906; 
      XX(7)=39.159; 
      XX(8)=33.328; 
      XX(9)=29.024;              
      XX(10)=25.731;
      XX(11)=23.139;
      XX(12)=21.050;
      XX(13)=19.335;
      XX(14)=17.903;
      XX(15)=16.690;
      XX(16)=15.651; 
      XX(17)=14.750; 
      XX(18)=11.609; 
      XX(19)=9.733;              
      XX(20)=8.486;
      XX(21)=7.595; 
      XX(22)=6.925; 
      XX(23)=6.401; 
      XX(24)=5.980;              
      XX(25)=5.633;             
      XX(26)=5.341;
      XX(27)=5.093;
      XX(28)=4.878;
      XX(29)=4.690;
      XX(30)=4.525;
      XX(31)=4.377;
      XX(32)=4.245; 
      XX(33)=3.826; 
      XX(34)=3.526; 
      XX(35)=3.298;              
      XX(36)=3.118;
      XX(37)=2.970;
      XX(38)=2.848;
      XX(39)=2.743;
      XX(40)=2.653;
      XX(41)=2.574;
      XX(42)=2.504; 
      XX(43)=2.245; 
      XX(44)=2.075; 
      XX(45)=1.952;              
      XX(46)=1.857;
      XX(47)=1.782; 
      XX(48)=1.719; 
      XX(49)=1.666; 
      XX(50)=1.620;              
      XX(51)=1.580;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL14A

if strcmp(nom_capteur,'eans14a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.851;
      XX(2)=69.242;
      XX(3)=60.376;
      XX(4)=53.424;
      XX(5)=47.852;
      XX(6)=43.303; 
      XX(7)=39.529; 
      XX(8)=33.656; 
      XX(9)=29.318;              
      XX(10)=25.999;
      XX(11)=23.385;
      XX(12)=21.280;
      XX(13)=19.550;
      XX(14)=18.105;
      XX(15)=16.882;
      XX(16)=15.833; 
      XX(17)=14.925; 
      XX(18)=11.754; 
      XX(19)=9.861;              
      XX(20)=8.602;
      XX(21)=7.702; 
      XX(22)=7.025; 
      XX(23)=6.496; 
      XX(24)=6.070;              
      XX(25)=5.720;             
      XX(26)=5.425;
      XX(27)=5.174;
      XX(28)=4.957;
      XX(29)=4.767;
      XX(30)=4.600;
      XX(31)=4.450;
      XX(32)=4.317; 
      XX(33)=3.894; 
      XX(34)=3.590; 
      XX(35)=3.359;              
      XX(36)=3.176;
      XX(37)=3.027;
      XX(38)=2.903;
      XX(39)=2.797;
      XX(40)=2.706;
      XX(41)=2.626;
      XX(42)=2.555; 
      XX(43)=2.293; 
      XX(44)=2.120; 
      XX(45)=1.995;              
      XX(46)=1.899;
      XX(47)=1.822; 
      XX(48)=1.758; 
      XX(49)=1.704; 
      XX(50)=1.658;              
      XX(51)=1.617;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end 
end
% Temperature, Niveau liquide NL14B ( modifier les valeurs ...)

if strcmp(nom_capteur,'eans14b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.851;
      XX(2)=69.242;
      XX(3)=60.376;
      XX(4)=53.424;
      XX(5)=47.852;
      XX(6)=43.303; 
      XX(7)=39.529; 
      XX(8)=33.656; 
      XX(9)=29.318;              
      XX(10)=25.999;
      XX(11)=23.385;
      XX(12)=21.280;
      XX(13)=19.550;
      XX(14)=18.105;
      XX(15)=16.882;
      XX(16)=15.833; 
      XX(17)=14.925; 
      XX(18)=11.754; 
      XX(19)=9.861;              
      XX(20)=8.602;
      XX(21)=7.702; 
      XX(22)=7.025; 
      XX(23)=6.496; 
      XX(24)=6.070;              
      XX(25)=5.720;             
      XX(26)=5.425;
      XX(27)=5.174;
      XX(28)=4.957;
      XX(29)=4.767;
      XX(30)=4.600;
      XX(31)=4.450;
      XX(32)=4.317; 
      XX(33)=3.894; 
      XX(34)=3.590; 
      XX(35)=3.359;              
      XX(36)=3.176;
      XX(37)=3.027;
      XX(38)=2.903;
      XX(39)=2.797;
      XX(40)=2.706;
      XX(41)=2.626;
      XX(42)=2.555; 
      XX(43)=2.293; 
      XX(44)=2.120; 
      XX(45)=1.995;              
      XX(46)=1.899;
      XX(47)=1.822; 
      XX(48)=1.758; 
      XX(49)=1.704; 
      XX(50)=1.658;              
      XX(51)=1.617;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end 
end
% Temperature, Niveau liquide NL13A

if strcmp(nom_capteur,'eans13a')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=91.956;
      XX(2)=77.578;
      XX(3)=66.875;
      XX(4)=58.647;
      XX(5)=52.152;
      XX(6)=46.915; 
      XX(7)=42.615; 
      XX(8)=35.999; 
      XX(9)=31.173;              
      XX(10)=27.514;
      XX(11)=24.654;
      XX(12)=22.363;
      XX(13)=20.489;
      XX(14)=18.930;
      XX(15)=17.615;
      XX(16)=16.490; 
      XX(17)=15.518; 
      XX(18)=12.144; 
      XX(19)=10.143;              
      XX(20)=8.817;
      XX(21)=7.873; 
      XX(22)=7.164; 
      XX(23)=6.612; 
      XX(24)=6.168;              
      XX(25)=5.803;             
      XX(26)=5.496;
      XX(27)=5.236;
      XX(28)=5.010;
      XX(29)=4.814;
      XX(30)=4.640;
      XX(31)=4.486;
      XX(32)=4.347; 
      XX(33)=3.911; 
      XX(34)=3.598; 
      XX(35)=3.361;              
      XX(36)=3.174;
      XX(37)=3.022;
      XX(38)=2.895;
      XX(39)=2.788;
      XX(40)=2.695;
      XX(41)=2.614;
      XX(42)=2.542; 
      XX(43)=2.278; 
      XX(44)=2.105; 
      XX(45)=1.981;              
      XX(46)=1.886;
      XX(47)=1.811; 
      XX(48)=1.749; 
      XX(49)=1.696; 
      XX(50)=1.651;              
      XX(51)=1.612;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
	       	
end
end


% Temperature, Niveau liquide NL13B ( modifier les valeurs ...)

if strcmp(nom_capteur,'eans13b')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=91.956;
      XX(2)=77.578;
      XX(3)=66.875;
      XX(4)=58.647;
      XX(5)=52.152;
      XX(6)=46.915; 
      XX(7)=42.615; 
      XX(8)=35.999; 
      XX(9)=31.173;              
      XX(10)=27.514;
      XX(11)=24.654;
      XX(12)=22.363;
      XX(13)=20.489;
      XX(14)=18.930;
      XX(15)=17.615;
      XX(16)=16.490; 
      XX(17)=15.518; 
      XX(18)=12.144; 
      XX(19)=10.143;              
      XX(20)=8.817;
      XX(21)=7.873; 
      XX(22)=7.164; 
      XX(23)=6.612; 
      XX(24)=6.168;              
      XX(25)=5.803;             
      XX(26)=5.496;
      XX(27)=5.236;
      XX(28)=5.010;
      XX(29)=4.814;
      XX(30)=4.640;
      XX(31)=4.486;
      XX(32)=4.347; 
      XX(33)=3.911; 
      XX(34)=3.598; 
      XX(35)=3.361;              
      XX(36)=3.174;
      XX(37)=3.022;
      XX(38)=2.895;
      XX(39)=2.788;
      XX(40)=2.695;
      XX(41)=2.614;
      XX(42)=2.542; 
      XX(43)=2.278; 
      XX(44)=2.105; 
      XX(45)=1.981;              
      XX(46)=1.886;
      XX(47)=1.811; 
      XX(48)=1.749; 
      XX(49)=1.696; 
      XX(50)=1.651;              
      XX(51)=1.612;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);
     conversion(isnan(conversion)) = 0.;
end	       	
end


% Temperature, Niveau liquide NL12

if strcmp(nom_capteur,'eans12')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.765;
      XX(2)=68.909;
      XX(3)=59.970;
      XX(4)=53.020;
      XX(5)=47.481;
      XX(6)=42.975; 
      XX(7)=39.247; 
      XX(8)=33.456; 
      XX(9)=29.183;              
      XX(10)=25.913;
      XX(11)=23.336;
      XX(12)=21.258;
      XX(13)=19.549;
      XX(14)=18.119;
      XX(15)=16.908;
      XX(16)=15.868; 
      XX(17)=14.966; 
      XX(18)=11.809; 
      XX(19)=9.916;              
      XX(20)=8.718;
      XX(21)=7.798; 
      XX(22)=7.104; 
      XX(23)=6.563; 
      XX(24)=6.127;              
      XX(25)=5.768;             
      XX(26)=5.467;
      XX(27)=5.211;
      XX(28)=4.989;
      XX(29)=4.796;
      XX(30)=4.625;
      XX(31)=4.474;
      XX(32)=4.338; 
      XX(33)=3.909; 
      XX(34)=3.603; 
      XX(35)=3.371;              
      XX(36)=3.188;
      XX(37)=3.040;
      XX(38)=2.916;
      XX(39)=2.811;
      XX(40)=2.721;
      XX(41)=2.642;
      XX(42)=2.573; 
      XX(43)=2.317; 
      XX(44)=2.151; 
      XX(45)=2.032;              
      XX(46)=1.942;
      XX(47)=1.870; 
      XX(48)=1.811; 
      XX(49)=1.762; 
      XX(50)=1.719;              
      XX(51)=1.683;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL11

if strcmp(nom_capteur,'eans11')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=81.672;
      XX(2)=69.481;
      XX(3)=60.320;
      XX(4)=53.217;
      XX(5)=47.570;
      XX(6)=42.987; 
      XX(7)=39.202; 
      XX(8)=33.336; 
      XX(9)=29.022;              
      XX(10)=25.727;
      XX(11)=23.137;
      XX(12)=21.052;
      XX(13)=19.339;
      XX(14)=17.909;
      XX(15)=16.698;
      XX(16)=15.660; 
      XX(17)=14.760; 
      XX(18)=11.619; 
      XX(19)=9.742;              
      XX(20)=8.550;
      XX(21)=7.642; 
      XX(22)=6.959; 
      XX(23)=6.425; 
      XX(24)=5.997;              
      XX(25)=5.644;             
      XX(26)=5.349;
      XX(27)=5.097;
      XX(28)=4.880;
      XX(29)=4.690;
      XX(30)=4.523;
      XX(31)=4.375;
      XX(32)=4.242; 
      XX(33)=3.822; 
      XX(34)=3.523; 
      XX(35)=3.296;              
      XX(36)=3.118;
      XX(37)=2.973;
      XX(38)=2.852;
      XX(39)=2.750;
      XX(40)=2.662;
      XX(41)=2.585;
      XX(42)=2.518; 
      XX(43)=2.269; 
      XX(44)=2.108; 
      XX(45)=1.993;              
      XX(46)=1.905;
      XX(47)=1.835; 
      XX(48)=1.778; 
      XX(49)=1.730; 
      XX(50)=1.689;              
      XX(51)=1.653;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

 % Temperature, Niveau liquide NL10

if strcmp(nom_capteur,'eans10')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=90.432;
      XX(2)=76.667;
      XX(3)=66.310;
      XX(4)=58.286;
      XX(5)=51.919;
      XX(6)=46.762; 
      XX(7)=42.515; 
      XX(8)=35.960; 
      XX(9)=31.163;              
      XX(10)=27.520;
      XX(11)=24.668;
      XX(12)=22.381;
      XX(13)=20.510;
      XX(14)=18.953;
      XX(15)=17.638;
      XX(16)=16.514; 
      XX(17)=15.543; 
      XX(18)=12.170; 
      XX(19)=10.169;              
      XX(20)=8.844;
      XX(21)=7.901; 
      XX(22)=7.193; 
      XX(23)=6.641; 
      XX(24)=6.197;              
      XX(25)=5.833;             
      XX(26)=5.527;
      XX(27)=5.266;
      XX(28)=5.041;
      XX(29)=4.844;
      XX(30)=4.671;
      XX(31)=4.516;
      XX(32)=4.378; 
      XX(33)=3.941; 
      XX(34)=3.628; 
      XX(35)=3.391;              
      XX(36)=3.203;
      XX(37)=3.050;
      XX(38)=2.923;
      XX(39)=2.814;
      XX(40)=2.721;
      XX(41)=2.639;
      XX(42)=2.566; 
      XX(43)=2.299; 
      XX(44)=2.124; 
      XX(45)=1.997;              
      XX(46)=1.900;
      XX(47)=1.822; 
      XX(48)=1.757; 
      XX(49)=1.703; 
      XX(50)=1.657;              
      XX(51)=1.616;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL9

if strcmp(nom_capteur,'eans9')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=97.635;
      XX(2)=81.842;
      XX(3)=70.239;
      XX(4)=61.402;
      XX(5)=54.475;
      XX(6)=48.919; 
      XX(7)=44.375; 
      XX(8)=37.416; 
      XX(9)=32.361;              
      XX(10)=28.540;
      XX(11)=25.560;
      XX(12)=23.175;
      XX(13)=21.228;
      XX(14)=19.609;
      XX(15)=18.244;
      XX(16)=17.078; 
      XX(17)=16.070; 
      XX(18)=12.575; 
      XX(19)=10.503;              
      XX(20)=9.196;
      XX(21)=8.204; 
      XX(22)=7.460; 
      XX(23)=6.880; 
      XX(24)=6.415;              
      XX(25)=6.032;             
      XX(26)=5.712;
      XX(27)=5.440;
      XX(28)=5.205;
      XX(29)=5.000;
      XX(30)=4.819;
      XX(31)=4.659;
      XX(32)=4.515; 
      XX(33)=4.063; 
      XX(34)=3.740; 
      XX(35)=3.497;              
      XX(36)=3.305;
      XX(37)=3.149;
      XX(38)=3.019;
      XX(39)=2.910;
      XX(40)=2.815;
      XX(41)=2.733;
      XX(42)=2.660; 
      XX(43)=2.393; 
      XX(44)=2.220; 
      XX(45)=2.096;              
      XX(46)=2.002;
      XX(47)=1.927; 
      XX(48)=1.865; 
      XX(49)=1.814; 
      XX(50)=1.770;              
      XX(51)=1.731;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL8 

if strcmp(nom_capteur,'eans8')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=91.491;
      XX(2)=77.492;
      XX(3)=67.055;
      XX(4)=59.011;
      XX(5)=52.646;
      XX(6)=47.499; 
      XX(7)=43.262; 
      XX(8)=36.718; 
      XX(9)=31.921;              
      XX(10)=28.269;
      XX(11)=25.404;
      XX(12)=23.100;
      XX(13)=21.211;
      XX(14)=19.635;
      XX(15)=18.301;
      XX(16)=17.159; 
      XX(17)=16.170; 
      XX(18)=12.721; 
      XX(19)=10.661;              
      XX(20)=9.365;
      XX(21)=8.370; 
      XX(22)=7.621; 
      XX(23)=7.036; 
      XX(24)=6.566;              
      XX(25)=6.179;             
      XX(26)=5.854;
      XX(27)=5.578;
      XX(28)=5.339;
      XX(29)=5.131;
      XX(30)=4.947;
      XX(31)=4.784;
      XX(32)=4.638; 
      XX(33)=4.177; 
      XX(34)=3.847; 
      XX(35)=3.598;              
      XX(36)=3.402;
      XX(37)=3.242;
      XX(38)=3.110;
      XX(39)=2.997;
      XX(40)=2.900;
      XX(41)=2.816;
      XX(42)=2.741; 
      XX(43)=2.467; 
      XX(44)=2.289; 
      XX(45)=2.161;              
      XX(46)=2.064;
      XX(47)=1.987; 
      XX(48)=1.924; 
      XX(49)=1.871; 
      XX(50)=1.825;              
      XX(51)=1.786;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL7 

if strcmp(nom_capteur,'eans7')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=97.484;
      XX(2)=82.162;
      XX(3)=70.807;
      XX(4)=62.099;
      XX(5)=55.238;
      XX(6)=49.710; 
      XX(7)=45.173; 
      XX(8)=38.195; 
      XX(9)=33.104;              
      XX(10)=29.242;
      XX(11)=26.222;
      XX(12)=23.800;
      XX(13)=21.818;
      XX(14)=20.168;
      XX(15)=18.775;
      XX(16)=17.584; 
      XX(17)=16.553; 
      XX(18)=12.972; 
      XX(19)=10.844;              
      XX(20)=9.503;
      XX(21)=8.481; 
      XX(22)=7.714; 
      XX(23)=7.115; 
      XX(24)=6.635;              
      XX(25)=6.240;             
      XX(26)=5.909;
      XX(27)=5.627;
      XX(28)=5.384;
      XX(29)=5.172;
      XX(30)=4.985;
      XX(31)=4.819;
      XX(32)=4.671; 
      XX(33)=4.203; 
      XX(34)=3.869; 
      XX(35)=3.617;              
      XX(36)=3.418;
      XX(37)=3.257;
      XX(38)=3.123;
      XX(39)=3.009;
      XX(40)=2.911;
      XX(41)=2.826;
      XX(42)=2.750; 
      XX(43)=2.474; 
      XX(44)=2.295; 
      XX(45)=2.166;              
      XX(46)=2.069;
      XX(47)=1.991; 
      XX(48)=1.928; 
      XX(49)=1.874; 
      XX(50)=1.829;              
      XX(51)=1.789;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL6 

if strcmp(nom_capteur,'eans6')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=86.692;
      XX(2)=73.892;
      XX(3)=64.180;
      XX(4)=56.606;
      XX(5)=50.563;
      XX(6)=45.648;
      XX(7)=41.584; 
      XX(8)=35.284; 
      XX(9)=30.652; 
      XX(10)=27.120;              
      XX(11)=24.348;
      XX(12)=22.120;
      XX(13)=20.293;
      XX(14)=18.770;
      XX(15)=17.482;
      XX(16)=16.380;
      XX(17)=15.427; 
      XX(18)=12.108; 
      XX(19)=10.133; 
      XX(20)=8.823;              
      XX(21)=7.889;
      XX(22)=7.187; 
      XX(23)=6.639; 
      XX(24)=6.199; 
      XX(25)=5.837;              
      XX(26)=5.533;             
      XX(27)=5.274;
      XX(28)=5.050;
      XX(29)=4.854;
      XX(30)=4.681;
      XX(31)=4.528;
      XX(32)=4.390;
      XX(33)=3.955; 
      XX(34)=3.643; 
      XX(35)=3.407; 
      XX(36)=3.219;              
      XX(37)=3.067;
      XX(38)=2.940;
      XX(39)=2.831;
      XX(40)=2.738;
      XX(41)=2.656;
      XX(42)=2.584;
      XX(43)=2.317; 
      XX(44)=2.141; 
      XX(45)=2.014; 
      XX(46)=1.917;              
      XX(47)=1.839;
      XX(48)=1.775; 
      XX(49)=1.720; 
      XX(50)=1.673; 
      XX(51)=1.633;              
                 
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end

% Temperature, Niveau liquide NL5 

if strcmp(nom_capteur,'eans5')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=78.445;
      XX(2)=67.485;
      XX(3)=59.059;
      XX(4)=52.417;
      XX(5)=47.068;
      XX(6)=42.684; 
      XX(7)=39.036; 
      XX(8)=33.334; 
      XX(9)=29.104;              
      XX(10)=25.855;
      XX(11)=23.290;
      XX(12)=21.218;
      XX(13)=19.513;
      XX(14)=18.086;
      XX(15)=16.875;
      XX(16)=15.837; 
      XX(17)=14.936; 
      XX(18)=11.784; 
      XX(19)=9.896;              
      XX(20)=8.638;
      XX(21)=7.737; 
      XX(22)=7.059; 
      XX(23)=6.529; 
      XX(24)=6.102;              
      XX(25)=5.750;             
      XX(26)=5.454;
      XX(27)=5.202;
      XX(28)=4.984;
      XX(29)=4.793;
      XX(30)=4.625;
      XX(31)=4.475;
      XX(32)=4.340; 
      XX(33)=3.915; 
      XX(34)=3.610; 
      XX(35)=3.378;              
      XX(36)=3.194;
      XX(37)=3.044;
      XX(38)=2.919;
      XX(39)=2.813;
      XX(40)=2.721;
      XX(41)=2.641;
      XX(42)=2.569; 
      XX(43)=2.306; 
      XX(44)=2.133; 
      XX(45)=2.008;              
      XX(46)=1.912;
      XX(47)=1.835; 
      XX(48)=1.771; 
      XX(49)=1.717; 
      XX(50)=1.671;              
      XX(51)=1.630;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL4 

if strcmp(nom_capteur,'eans4')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=82.410;
      XX(2)=70.491;
      XX(3)=61.368;
      XX(4)=54.210;
      XX(5)=48.473;
      XX(6)=43.791; 
      XX(7)=39.911; 
      XX(8)=33.881; 
      XX(9)=29.439;              
      XX(10)=26.047;
      XX(11)=23.382;
      XX(12)=21.240;
      XX(13)=19.483;
      XX(14)=18.019;
      XX(15)=16.781;
      XX(16)=15.721; 
      XX(17)=14.805; 
      XX(18)=11.616; 
      XX(19)=9.721;              
      XX(20)=8.465;
      XX(21)=7.570; 
      XX(22)=6.899; 
      XX(23)=6.375; 
      XX(24)=5.954;              
      XX(25)=5.607;             
      XX(26)=5.317;
      XX(27)=5.069;
      XX(28)=4.855;
      XX(29)=4.668;
      XX(30)=4.504;
      XX(31)=4.357;
      XX(32)=4.225; 
      XX(33)=3.810; 
      XX(34)=3.512; 
      XX(35)=3.286;              
      XX(36)=3.108;
      XX(37)=2.962;
      XX(38)=2.840;
      XX(39)=2.737;
      XX(40)=2.647;
      XX(41)=2.569;
      XX(42)=2.500; 
      XX(43)=2.243; 
      XX(44)=2.074; 
      XX(45)=1.952;              
      XX(46)=1.857;
      XX(47)=1.781; 
      XX(48)=1.719; 
      XX(49)=1.665; 
      XX(50)=1.619;              
      XX(51)=1.579;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL3 

if strcmp(nom_capteur,'eans3')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=87.076;
      XX(2)=73.783;
      XX(3)=63.865;
      XX(4)=56.216;
      XX(5)=50.161;
      XX(6)=45.262; 
      XX(7)=41.228; 
      XX(8)=34.996; 
      XX(9)=30.426;              
      XX(10)=26.946;
      XX(11)=24.214;
      XX(12)=22.018;
      XX(13)=20.217;
      XX(14)=18.714;
      XX(15)=17.442;
      XX(16)=16.353; 
      XX(17)=15.410; 
      XX(18)=12.119; 
      XX(19)=10.155;              
      XX(20)=8.917;
      XX(21)=7.966; 
      XX(22)=7.251; 
      XX(23)=6.693; 
      XX(24)=6.245;              
      XX(25)=5.876;             
      XX(26)=5.567;
      XX(27)=5.304;
      XX(28)=5.076;
      XX(29)=4.878;
      XX(30)=4.703;
      XX(31)=4.548;
      XX(32)=4.408; 
      XX(33)=3.970; 
      XX(34)=3.657; 
      XX(35)=3.420;              
      XX(36)=3.233;
      XX(37)=3.081;
      XX(38)=2.955;
      XX(39)=2.848;
      XX(40)=2.756;
      XX(41)=2.676;
      XX(42)=2.605; 
      XX(43)=2.345; 
      XX(44)=2.176; 
      XX(45)=2.055;              
      XX(46)=1.963;
      XX(47)=1.890; 
      XX(48)=1.831; 
      XX(49)=1.780; 
      XX(50)=1.737;              
      XX(51)=1.700;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL2 

if strcmp(nom_capteur,'eans2')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=80.973;
      XX(2)=69.471;
      XX(3)=60.647;
      XX(4)=53.707;
      XX(5)=48.131;
      XX(6)=43.570; 
      XX(7)=39.782; 
      XX(8)=33.877; 
      XX(9)=29.509;              
      XX(10)=26.165;
      XX(11)=23.530;
      XX(12)=21.406;
      XX(13)=19.660;
      XX(14)=18.203;
      XX(15)=16.968;
      XX(16)=15.910; 
      XX(17)=14.994; 
      XX(18)=11.795; 
      XX(19)=9.887;              
      XX(20)=8.618;
      XX(21)=7.712; 
      XX(22)=7.031; 
      XX(23)=6.499; 
      XX(24)=6.071;              
      XX(25)=5.719;             
      XX(26)=5.423;
      XX(27)=5.171;
      XX(28)=4.953;
      XX(29)=4.762;
      XX(30)=4.594;
      XX(31)=4.445;
      XX(32)=4.310; 
      XX(33)=3.887; 
      XX(34)=3.583; 
      XX(35)=3.352;              
      XX(36)=3.169;
      XX(37)=3.020;
      XX(38)=2.896;
      XX(39)=2.791;
      XX(40)=2.699;
      XX(41)=2.619;
      XX(42)=2.549; 
      XX(43)=2.288; 
      XX(44)=2.116; 
      XX(45)=1.992;              
      XX(46)=1.896;
      XX(47)=1.819; 
      XX(48)=1.756; 
      XX(49)=1.703; 
      XX(50)=1.657;              
      XX(51)=1.616;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end
% Temperature, Niveau liquide NL1 

if strcmp(nom_capteur,'eans1')
	% a=max(tension);
	% b=min(tension);
	if (tension > 5) 
	% disp('Hors gamme');
	conversion=tension;
	else
      XX(1)=81.639;
      XX(2)=69.894;
      XX(3)=60.912;
      XX(4)=53.864;
      XX(5)=48.214;
      XX(6)=43.601; 
      XX(7)=39.775; 
      XX(8)=33.822; 
      XX(9)=29.429;              
      XX(10)=26.071;
      XX(11)=23.429;
      XX(12)=21.301;
      XX(13)=19.555;
      XX(14)=18.098;
      XX(15)=16.865;
      XX(16)=15.808; 
      XX(17)=14.894; 
      XX(18)=11.707; 
      XX(19)=9.807;              
      XX(20)=8.546;
      XX(21)=7.646; 
      XX(22)=6.970; 
      XX(23)=6.442; 
      XX(24)=6.017;              
      XX(25)=5.668;             
      XX(26)=5.374;
      XX(27)=5.124;
      XX(28)=4.908;
      XX(29)=4.719;
      XX(30)=4.552;
      XX(31)=4.404;
      XX(32)=4.271; 
      XX(33)=3.851; 
      XX(34)=3.549; 
      XX(35)=3.320;              
      XX(36)=3.139;
      XX(37)=2.992;
      XX(38)=2.868;
      XX(39)=2.764;
      XX(40)=2.673;
      XX(41)=2.594;
      XX(42)=2.524; 
      XX(43)=2.264; 
      XX(44)=2.093; 
      XX(45)=1.970;              
      XX(46)=1.875;
      XX(47)=1.798; 
      XX(48)=1.735; 
      XX(49)=1.682; 
      XX(50)=1.636;              
      XX(51)=1.596 ;             
		
      YY(1)=120;
      YY(2)=125;
      YY(3)=130;
      YY(4)=135;
      YY(5)=140;
      YY(6)=145;
      YY(7)=150;
      YY(8)=160;
      YY(9)=170;
      YY(10)=180;
      YY(11)=190;
      YY(12)=200;
      YY(13)=210;
      YY(14)=220;
      YY(15)=230;
      YY(16)=240;
      YY(17)=250;
      YY(18)=300;
      YY(19)=350;
      YY(20)=400;
      YY(21)=450;
      YY(22)=500;
      YY(23)=550;
      YY(24)=600;
      YY(25)=650;
      YY(26)=700;		
      YY(27)=750;
      YY(28)=800;
      YY(29)=850;
      YY(30)=900;
      YY(31)=950;
      YY(32)=1000;
      YY(33)=1200;
      YY(34)=1400;
      YY(35)=1600;
      YY(36)=1800;
      YY(37)=2000;
      YY(38)=2200;
      YY(39)=2400;
      YY(40)=2600;
      YY(41)=2800;
      YY(42)=3000;
      YY(43)=4000;
      YY(44)=5000;
      YY(45)=6000;
      YY(46)=7000;
      YY(47)=8000;
      YY(48)=9000;
      YY(49)=10000;
      YY(50)=11000;
      YY(51)=12000;
 

% Conversion valeur ohmique en tension

      ZZ=(YY*4/10000)+1;

% Conversion du fichier de donnees

     conversion=interp1(ZZ,XX,tension);      
     conversion(isnan(conversion)) = 0.;
end
end


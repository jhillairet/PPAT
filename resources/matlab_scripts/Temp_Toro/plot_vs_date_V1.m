function hd = plot_vs_date_V1(varargin)
%
% Fonction plot_vs_date.m
% =======================
%
% Cette fonction permet de tracer des données avec des abscisses sous forme
% de dates jj/mm/aaaa ou hh:mm:ss
%
% Utilisation: hd = plot_vs_date(varargin)
%   Entrées:
%      tous les arguments sont ceux qui seront passés à la fonction plot
%      le dernier argument (optionnel) est une structure qui permet de
%      spécifier le format des dates à utiliser:
%          Param.DateFormat format date utilisable par la fonction datestr
%          Param.NbTick     Nb de tickmark sur l'axe X (défaut 7)
%   Sortie:
%      hd est le handle de la figure
%
% Ph. Moreau Version 0 du 05/12/2016
%

%
% Init sortie
% -----------
hd = [];

%
% Gestion des entrées
% -------------------
if isstruct(varargin {end})
    Param = varargin{end};
    nargPlot = nargin-1;
else
    Param = [];
    nargPlot = nargin;
end
if ~isfield(Param,'DateFormat'), Param.DateFormat = []; end
if ~isfield(Param,'NbTick'),     Param.NbTick     = 7;          end


%
% Preapare plot
% --------------
% ----> Get plot input parameters
[cax,args,nargs] = axescheck(varargin{:});
NmArgPlot = sprintf('Arg%.2d , ',1:nargPlot); NmArgPlot = NmArgPlot(1:end-3);
cmd = sprintf('[%s] = deal(args{1:nargPlot});',NmArgPlot);
eval(cmd)

% ----> plot Data
% keyboard
cmd = sprintf('hd = plot(%s);',NmArgPlot);
eval(cmd)
ax = gca; set(ax,'FontSize',12,'UserData',Param);
h = zoom; 
set(h,'ActionPostCallback',@Zoom_Plot_vs_date);
set(h,'Enable','on');
Zoom_Plot_vs_date([],ax);

% ********************************************************************
% *                                                                  *
% * Fonction that changes the XTicks to date                         *
% *                                                                  *
% ********************************************************************
function Zoom_Plot_vs_date(obj,evd)

if isstruct(evd)
    ax = evd.Axes;
else
    ax = evd;
end
axes(ax); Param = get(ax,'UserData');
SCR=axis; Xmin = SCR(1); Xmax=SCR(2); dX = Xmax-Xmin;
Val=[Xmin:(Xmax-Xmin)/(Param.NbTick-1):Xmax];
set(ax,'XTick',Val);
if ~isempty(Param.DateFormat)  % Date format has been specified
    XTickLabel = datestr(Val,Param.DateFormat);
else                           % Date format is automatically defined
    if dX>4
        XTickLabel = datestr(Val,'dd/mm/yyyy');
    elseif dX>1
        XTickLabel = datestr(Val,'dd/mm/yyyy HH:MM:SS');
    elseif dX>0.5
        XTickLabel = datestr(Val,'HH:MM:SS');
    else
        XTickLabel = datestr(Val,'HH:MM:SS.FFF');
    end
end
set(ax,'XTickLabel',XTickLabel);




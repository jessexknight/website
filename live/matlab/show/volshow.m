% VOLSHOW is a flexible debugging tool for displaying multiple volumes tightly
%         on the same figure. Mouse scroll wheel scrolls the z dimension.
%         Padding between images, grid dimensions, contrast scale, and
%         colourmaps can be specified. Attributes apply to all images. Best
%         results with same sized images. Grayscale or colour images. A
%         user-supplied click function can also be linked, with option to
%         plot some resulting data on an extra axes (e.g. local histogram)
% 
% Input arguments: (any order)
%    images(s) - any number of 3D grayscale or colour images. Rendered in the
%                order they are presented, top to bottom, left to right. 
%                * The x-dimension of any image should not have a size of 3,
%                  else it will be confused for a colourmap.
%                * multiple volumes should have the same 3rd dimension.
%                * if using colour volumes, the colour channels should be the
%                  last dimension.
% 
%    padval    - decimal value on the interval (0, 0.5) dictating the relative
%                padded spacing between images.
%                Default: 0.005
% 
%    gridstr   - string like "5x2", specifying the number of axes to tile
%                horizontally (5) and vertically (2)
%                Default: as square as possible, wider bias
% 
%    minmax    - minmax specification for contrast scaling, as in imshow(I,[]).
%                array of size: 1 by 2, or a empty array: []. Applies to all
%                volumes equally.
%                Default: []
% 
%    colourmap - colourmap used for displaying images:
%                array of size M by 3, or a colourmap function
%                Default: curent default figure colormap
% 
%    patchfcn  - user specified function which accepts some data and plots
%                some result from it after a double click in any of the axes.
%                Function should take the form:
%                function [] = patchfcn(ax, minmax, patchdata)
%                Inputs:  ax        - handle to the last unused axes
%                         minmax    - cell array of minmax for all image axes.
%                         patchdata - cell array of image data corresponding
%                                     to the clicked patch (from all axes).
%                         patchdata, mimax orders: {clicked axes, all others}.
%                Outputs: None required, but presumably plotting on the axes.
%                Default: None
% 
%    patchsize - size of the patch data passed to patchfcn
%                Default: [15, 15, 1]
% 
%              * if 2+ non-image arguments are given, only the last one is used.
% 
% Examples:
% 
%    volshow(I1, I2, I3, I4, hot, 0, [0,1], '4x1');
%                Show volumes I1, I2, I3, I4 using the hot colourmap, with no
%                space between, contrast from 0 to 1, and in a horizontal line.
% 
%    volshow(DB(:).I);
%                Show all volume fields .I in the struct array DB using the
%                default figure colourmap, automatic contrast scaling per image,
%                with 0.5% of total figure size padded between, and arranged as
%                close to square as possible.
% 
% Jesse Knight 2016

function varargout = volshow(varargin)
% -- do not edit: MATLAB GUIDE 
gui_Singleton = 0;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @volshow_OpeningFcn, ...
    'gui_OutputFcn',  @volshow_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end % -- end do not edit

% --- Executes just before volshow is made visible.
function volshow_OpeningFcn(hObject, ~, handles, varargin)

handles.output  = hObject;
handles.badcall = 0;
set(0,'defaultTextFontName','Courier New');

try % if any errors: abort and give error (to ensure GUI closes)
    % default values
    handles.img       = [];
    handles.minmax    = [];
    handles.patchfcn  = [];
    handles.patchsize = [15,15,1];
    handles.colourmap = get(0,'defaultfigurecolormap');
    handles.pad       = 0.005;
    
    % handle input arguments based on their dimensions
    for v = 1:numel(varargin)
        sizev = size(varargin{v});
        % image volume (possibly including colour in 3rd dimension)
        if numel(sizev) >= 3
            if islogical(varargin{v}), varargin{v} = single(varargin{v}); end
            handles.img(end+1).data  = varargin{v};
            handles.img(end).size    = size(handles.img(end).data);
            handles.img(end).frame   = round(handles.img(end).size(3)*0.5);
            handles.img(end).textpos = [round(handles.img(end).size(1)/20 + 1),...
                                        round(handles.img(end).size(2)/20 + 1)];
        
        % grid specification string
        elseif ischar(varargin{v}) && numel(sscanf(varargin{v},'%dx%d')) == 2
            xy = sscanf(varargin{v},'%dx%d');
            handles.nSubx = xy(1);
            handles.nSuby = xy(2);
        % click function
        elseif isa(varargin{v},'function_handle')
            handles.patchfcn = varargin{v};
        % patch size for the click
        elseif all(sizev == [1,3]) || all(sizev == [3,1])
            handles.patchsize = varargin{v};
        % pad value
        elseif all(sizev == [1,1])
            handles.pad = varargin{v};
        % minmax ([])
        elseif sizev(1) == 0
            handles.minmax = [];
        % minmax (numerical)
        elseif all(sizev == [1,2]) || all(sizev == [2,1])
            handles.minmax = varargin{v};
        % colourmap
        elseif sizev(2) == 3
            handles.colourmap = varargin{v};
        % argument not recognized: ignoring
        else
            warning(['Ignoring argument number ',num2str(v),'.']);
        end
    end
    % optimize display grid square-ish if not user specified
    handles.N = numel(handles.img) + ~isempty(handles.patchfcn);
    if ~all(isfield(handles,{'nSubx','nSuby'}))
      if handles.N ~= 3
        handles.nSubx = ceil(sqrt(handles.N));
        handles.nSuby = ceil(handles.N/handles.nSubx);
      else % special case for 3 - just looks better
        handles.nSubx = 3;
        handles.nSuby = 1;
      end
    end
    % defining per-image minmaxs
    for n = 1:numel(handles.img)
      if isempty(handles.minmax)
        handles.img(n).minmax = [min(handles.img(n).data(:)),...
                                 max(handles.img(n).data(:))];
      else
        handles.img(n).minmax = handles.minmax;
      end
    end
    % subplot handles initialization
    for a = 1:numel(handles.img)
      handles.ax(a) = subplot(handles.nSuby,handles.nSubx,a,...
          'ButtonDownFcn',{@clickfcn,handles},...
          'HitTest','off');%,'NextPlot','replacechildren');
    end
    if ~isempty(handles.patchfcn);
        handles.ax(end+1) = subplot(handles.nSuby,handles.nSubx,handles.N,...
          'xtick',[],'ytick',[]);
    end
    % subplot spacing (separate for overlap issue)
    for a = 1:handles.N
        y = ceil(a / handles.nSubx);
        x = mod(a, handles.nSubx);
        x(~x) = handles.nSubx;
        
        set(handles.ax(a),'position',[(x - 1) / handles.nSubx + 0.5*handles.pad,  ...
                                       1 - (y / handles.nSuby - 0.5*handles.pad), ...
                                            1 / handles.nSubx - handles.pad,  ...
                                            1 / handles.nSuby - handles.pad]);
    end
    % optimize figure display size for the current monitor and first image size
    % centres the figure in onscreen too.
    screensize = get(0,'screensize');
    aspect     = (size(handles.img(1).data,1) / size(handles.img(1).data,2));
    imgSize = min(800, (0.4*screensize(3)) / handles.nSubx);
    set(gcf,'color','k','position',...
        [(screensize(3) - (imgSize*handles.nSubx))/2,...
         (screensize(4) - (imgSize*handles.nSuby))/2,...
         (imgSize*handles.nSubx),...
         (imgSize*handles.nSuby*aspect)]);
    % render the middle frame of each volume to start
    imupdate(handles);
% input argument parsing failed: exit (could be more graceful)
catch
    warning('Error during initialization. Maybe bad arguments.');
    handles.badcall = 1;
end

guidata(hObject, handles);

% --- Outputs from this function are returned to the command line.
function varargout = volshow_OutputFcn(hObject, eventdata, handles)
varargout{1} = handles.output;
if handles.badcall
    figure1_CloseRequestFcn(hObject, eventdata, handles);
end

% --- Executes on scroll wheel click while the figure is in focus.
function figure1_WindowScrollWheelFcn(hObject, eventdata, handles)
% for all volumes
for i = 1:numel(handles.img)
    % adjust the frame index by the scroll count
    handles.img(i).frame = handles.img(i).frame + eventdata.VerticalScrollCount;
    % wrap around if z is less than 1 or larger than img.size
    if handles.img(i).frame > handles.img(i).size(3)
        handles.img(i).frame = 1;
    elseif handles.img(i).frame < 1
        handles.img(i).frame = handles.img(i).size(3);
    end
end
% update the frames onscreen
guidata(hObject, handles);
imupdate(handles);

% --- Called by other functions on WindowScrollWheelFcn movement.
function imupdate(handles)
% for all volumes
for i = 1:numel(handles.img)
    % show the current frame
    ha = imshow(squeeze(handles.img(i).data(:,:,handles.img(i).frame,:)),...
                handles.img(i).minmax,'parent',handles.ax(i));
    set(ha,'ButtonDownFcn',{@clickfcn,handles});
    % print the current frame number in the top left corner (red)
    text(handles.img(i).textpos(2),handles.img(i).textpos(1),...
        num2str(handles.img(i).frame),'color','r','parent',handles.ax(i));
end
colormap(handles.colourmap);

% --- Executes on any button click function within axes.
function clickfcn(hObject, ~, handles)
% need to do anything?
if isempty(handles.patchfcn)  
    return
end
% yes ...
% determine calling axes
for i = 1:numel(handles.img)
    if get(hObject,'Parent') == handles.ax(i)
        img = handles.img(i);
    end
end
% request the second click now that we know the calling axes
% should go smoothly on double click
[x,y] = ginput(1);
z     = img.frame;
% get the local patch coordinates and show the user
isize = img.size;
yy = floor(max(1,        y - handles.patchsize(1)/2)) : ...
     floor(min(isize(1), y + handles.patchsize(1)/2));
xx = floor(max(1,        x - handles.patchsize(2)/2)) : ...
     floor(min(isize(2), x + handles.patchsize(2)/2));
zz = floor(max(1,        z - handles.patchsize(3)/2)) : ...
     floor(min(isize(3), z + handles.patchsize(3)/2));
minmaxes{1} = highlightpatch(hObject,yy,xx,img.minmax);
drawnow;
% gather the patch data (might be 3D)
patches{1} = img.data(yy,xx,zz,:);
for i = 1:numel(handles.img)
    if get(hObject,'Parent') ~= handles.ax(i)
        patches{end+1}  = handles.img(i).data(yy,xx,zz,:);
        minmaxes{end+1} = handles.img(i).minmax;
    end
end
% try calling the user-specified function
try
  handles.patchfcn(handles.ax(end), minmaxes, patches);
end
% restore the images without patch highlighting
imupdate(handles);

% --- called by clickfcn to show the user where they've clicked
function [minmax] = highlightpatch(ax,yy,xx,minmax)
% get the frame data
I2 = get(ax,'CData');
% determine minmax if it isn't defined
if isempty(minmax)
  minmax = [min(I2(:)),max(I2(:))];
end
% paint the whole box bright
I2(yy,xx,:) = minmax(2);
% paint an inner box dark
I2(yy(2:end-1),xx(2:end-1),:) = minmax(1);
% refresh the frame data
set(ax,'CData',I2);

% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
delete(hObject);

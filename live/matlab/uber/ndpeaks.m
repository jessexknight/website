<html>
<head>

<title>Jesse Knight</title>
<script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/foundation/6.2.3/foundation.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/foundation/6.2.3/foundation.min.css">
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
<link rel="stylesheet" href="../custom.css">

</head>
<body>
  <div id='navbar' class='small-4 medium-3 large-2 columns'
       style='background-color:#333333; padding: 5 5 5 5;'>
<ul class='expanded dropdown menu' data-dropdown-menu><li>
      <a class='expanded button' href='../../pages/Home.html'>Home</a>
      <a class='expanded button' href='../../pages/Awards.html'>Awards</a>
      <a class='expanded button' href='../../pages/MATLAB.html'>MATLAB</a>
      <a class='expanded button' href='../../pages/Publications.html'>Publications</a>
      <a class='expanded button' href='../../pages/Teaching.html'>Teaching</a>
    </li></ul>  </div>
  <div id='content' class='small-8 medium-9 large-10 columns'
       style='background-color:#F5F5F5; padding: 5 5 5 5; min-height:100%'>
% [pks] = ndpeaks(X)
% 
% NDPEAKS finds all peaks in the N-D array X, in all directions. For each
%   direction, local maxima are incremented by 1. Thus, true local maxima 
%   will have pks == N for N-D array, while local maxima in only some
%   directoins will have 0 < pks < N. Edges will only have maxima in the 
%   non-truncated directions.
% 
% Args:
%   X  - ND array of real-valued data
% 
% Jesse Knight 2016

function [pks] = ndpeaks(X)
I     = double(X);
xsize = size(X);      % track input size
pks   = zeros(xsize); % initialize the output
nd    = numel(xsize); % num dim
for d = 1:nd % for all dimensions...
  XN        = shiftdim(X,d-1);  % shift the orientation
  xnsize    = size(XN);         % get size
  PN        = zeros(xnsize);    % initialize peak array in this orientation
  [~,idx]   = findpeaks(XN(:)); % find peaks in rastarized domain
  PN(idx)   = 1;                % logical mapping back to N-D space
  PN(1,:)   = 0;                % ignore the wrapped edges
  PN(end,:) = 0;                % ...
  P         = logical(shiftdim(PN,nd+1-d)); % map back to original orientation
  pks(P)    = pks(P) + 1;       % increment the global peak map
end
  
    </div>
</body>
</html>

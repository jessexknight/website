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
% [pYW,U] = pofwy(Y,X,op,varargin)
% 
% POFWY is a weighted histogram (normalized for unit norm).
%   This implementation uses a relatively fast data-removal technique.
%
% Input arguments:
%   Y - N-D data for which to compute the probability distribution.
%   W - N-D (same size) weights for each value in Y.
% 
%   varargin: passed straight to biny to bin the values in Y (see help biny).
%             N  - number of bins
%             mi - minmax (input)
%             mo - minmax (output)
% 
% Output arguments:
%   pYW - normalized histogram of Y, weighted by W
%   U   - unique bin values
% 
% Jesse Knight 2016


function [pYW,YU,U] = pofwy(Y,W,varargin)
% bin the data for easy lookup
[YU,U] = biny(Y,varargin{:});
YU = YU(:);
% initialize the output
pYW = nan(numel(U),1);
% calculating weighted histogram
% (remove data already counted for lookup speed *)
for u = 1:numel(U)
  idx     = (YU==U(u));  % lookup indices
  pYW(u)  = sum(W(idx)); % sum these weights
  YU(idx) = [];          % *
  W(idx)  = [];          % *
end
pYW = pYW./sum(W(:)); % normalization by sum of weights
  </div>
</body>
</html>

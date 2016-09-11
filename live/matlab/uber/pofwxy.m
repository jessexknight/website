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
% [pXYW,U] = pofwxy(Y,X,W,op,varargin)
% 
% POFWXY computes the weighted conditional probability of X given Y using
%   the user specified weighted conditional probability operator.
%   This implementation uses a relatively fast sort-lookup technique.
%
% Input arguments:
%   Y  - N-D data which is binned, then for each bin, the matching indices
%        are used to select data in X for computing the probability.
%   X  - N-D data (same size) on which the probability operation acts.
%   W  - N-D (same size) weights for each value in X
%   op - weighted probability operator - e.g. @wmean or
%        @(x,w)ksdensity(x,0.5,'weights',w);
% 
%   varargin: passed straight to biny to bin the values in Y (see help biny).
%             N  - number of bins
%             mi - minmax (input)
%             mo - minmax (output)
% 
% Output arguments:
%   pXYW - weighted conditional probability of x given y, by w
%   U    - unique bin values (of Y)
% 
% Jesse Knight 2016

function [pXYW,U] = pofwxy(Y,X,W,op,varargin)
% bin the data for easy lookup
[YU,U] = biny(Y,varargin{:});
% sort the data for faster lookup of paired data
[YS,s] = sort(YU(:));  % sorting source data
XS     = X(s);         % sorting paired data same order
WS     = W(s);         % sorting weights same order
% initialize the source data histogram (internal)
pY = nan(numel(U),1);
% calculating source histogram
% (remove data already counted for lookup speed *)
for u = 1:numel(U)
  idx     = (YS(:)==U(u));  % lookup indices
  pY(u)   = sum(idx);       % count these
  YS(idx) = [];             % *
end
% initialize paired data output
pXYW = zeros(numel(U),1);
% index ranges in sorted XS and WS: faster than lookup
idx = [0,cumsum(pY')];
% calculating paired data weighted histogram
for u = 1:numel(U)
  if (idx(u+1) > idx(u)+1) % not empty indices
    idxu = idx(u)+1:idx(u+1);
    if any(WS(idxu)) % not empty weights
      pXYW(u) = op( XS(idxu), WS(idxu) );
    else % empty weights
      pXYW(u) = nan;
    end
  else % empty indices
    pXYW(u) = nan;
  end
end
  </div>
</body>
</html>

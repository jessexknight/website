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
% [pXY,pY,U] = pofxy(Y,X,op,varargin)
% 
% POFXY computes the conditional probability of X given Y - p(X|Y),
%   "p of given y", using the user specified conditional probability operator.
%   This implementation uses a relatively fast sort-lookup technique.
%
% Input arguments:
%   Y  - N-D data which is binned, then for each bin, the matching indices
%        are used to select data in X for computing the probability.
%   X  - N-D data (same size) on which the probability operation acts.
%   op - probability operator - e.g. @mean or @(x)ksdensity(x,0.5);
% 
%   varargin: passed straight to biny to bin the values in Y (see help biny).
%             N  - number of bins
%             mi - minmax (input)
%             mo - minmax (output)
% 
% Output arguments:
%   pXY - conditional probability of x given y
%   pY  - normalized histogram of Y
%   U   - unique bin values (of Y)
% 
% Jesse Knight 2016

function [pXY,pY,U] = pofxy(Y,X,op,varargin)
% bin the data for easy lookup
[YU,U] = biny(Y,varargin{:});
% sort the data for faster lookup of paired data
[YS,s] = sort(YU(:));  % sorting source data
XS     = X(s);         % sorting paired data same order
% initialize the source data output
pY = nan(numel(U),1);
% calculating source histogram
% (remove data already counted for lookup speed *)
for u = 1:numel(U)
  idx     = (YS(:)==U(u));  % lookup indices
  pY(u)   = sum(idx);       % count these
  YS(idx) = [];             % *
end
% initialize paired data output
pXY = zeros(numel(U),1);
% index ranges in sorted XS: faster than lookup
idx = [0,cumsum(pY')];
% calculating paired data histogram
for u = 1:numel(U)
  if idx(u+1) > idx(u)+1 % not empty
    idxu = idx(u)+1 : idx(u+1);
    pXY(u) = op(XS(idxu));
  else % empty
    pXY(u) = nan;
  end
end
pY = pY'./numel(XS); % normalize the source histogram
  </div>
</body>
</html>
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
% [idx, ytrims] = alphatrim(Y, trims, mask)
% 
% ALPHATRIM computes a mask for an N-D array indicating values which are
%   within the specified alpha-"trims" (on the interval [0,1]).
%   An additional mask can be specified by the user to further refine the 
%   alpha-trim data; however the output indices may contain values outside
%   this mask. The cutoff values are also returned. This implementation
%   uses a fast sorting-based method.
% 
% Args:
%   Y      - ND array of real-valued data
%   trims  - 2-element vector on the interval [0,1] dictating what fractions
%            of the data in Y to exclude
%   mask   - (optional) additional mask within which to seach to find the 
%            alpha-trims only.
% 
% Returns:
%   idx    - indicies of valid elements: within alpha trims
%   ytrims - values corresponding to the alpha trim cutoffs
%   
% Jesse Knight 2016

function [idx, ytrims] = alphatrim(Y, trims, mask)
% vectorize the data with/out the mask
if ~isempty(mask)
  YB = Y(logical(mask));
  if isempty(YB)
    idx = []; ytrims = []; return;
  end
else
  YB = Y(:);
end
NY     = numel(YB); % count the elements 
[YS]   = sort(YB);  % sort the values
ntrims = NY.*trims; % find alpha trims in sorted-index space
ytrims = [YS(round(max(1, ntrims(1)))),...  % store the cutoff values
          YS(round(min(NY,ntrims(2))))];    % ...
idx    = (Y > ytrims(1)) & (Y < ytrims(2)); % 

  </div>
</body>
</html>
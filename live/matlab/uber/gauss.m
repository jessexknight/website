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
% [G] = gauss(sig)
% 
% GAUSS generates an N-D Gaussian probability density function having the 
%   standard deviations specified in the vector sig. Each element in sig 
%   corresponds to a dimension. Guaranteed to have unit norm.
% 
%   This function was designed for filtering 3D image volumes.
% 
% Jesse Knight 2016

function [G] = gauss(sig)
w = 3;          % how many std to include? (can edit)
N = numel(sig); % num dims
X = cell(1,N);  % N-D grid coordinates
W = cell(1,N);  % store size of the kernel later
for n = 1:N
  R{n} = floor(-w*sig(n)):ceil(+w*sig(n)); % sampling points in each dim
end
[X{:}] = ndgrid(R{:},1); % transform to grid N-D arrays
W(:)   = cellfun(@numel,R,'uni',false); % track exact size
for n = 1:N
  X{n} = X{n}(:); % vectorize the grids for mvnpdf below
end
G = mvnpdf(cat(2,X{:}),zeros(1,N),sig); % compute vectorized kernel values
G = reshape(G,cat(2,W{:},1)); % reshape to N-D array
G = G./sum(G(:)); % assert unit norm

  </div>
</body>
</html>
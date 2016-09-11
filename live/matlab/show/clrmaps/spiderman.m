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
      <a class='expanded button' href='../../../pages/Home.html'>Home</a>
      <a class='expanded button' href='../../../pages/Awards.html'>Awards</a>
      <a class='expanded button' href='../../../pages/MATLAB.html'>MATLAB</a>
      <a class='expanded button' href='../../../pages/Publications.html'>Publications</a>
      <a class='expanded button' href='../../../pages/Teaching.html'>Teaching</a>
    </li></ul>  </div>
  <div id='content' class='small-8 medium-9 large-10 columns'
       style='background-color:#F5F5F5; padding: 5 5 5 5; min-height:100%'>
function [cmap] = spiderman(m)
% colormap: blue-black-red (for difference images)
if nargin < 1
   m = size(get(gcf,'colormap'),1);
end
n = fix(m/2)-1;
r = [zeros(1,n+2) (1:+1:n)/n]';
g = zeros(1,m)';
b = [(n:-1:1)/n zeros(1,n+2)]';
cmap = [r,g,b];
  </div>
</body>
</html>
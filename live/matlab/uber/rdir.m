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
% [fulldir] = rdir(dirname)
% 
% RDIR builds a directory structure with the recursively found contents found
%      within directory 'dirname'. Similar to 'dir', but adds an additional
%      field 'pathname'.
%
% Input arguments:
%    dirname - Name of the directory to search.
%
% Output arguments:
%   fulldir - Struct array of the contents (files and folders) of dirname:
%             .name  - name of the file or folder.
%             .date  - date modified
%             .bytes - file size in bytes (folders are 0 regardless of contents)
%             .isdir - boolean
%             .datenum  - number of days since Jan 01, 0000 (for sorting)
%             .pathname - constructed path and filename string from 'dirname'
%                         up to and including .name.
% 
% Jesse Knight 2016

function [fulldir] = rdir(dirname)

basedir = dir(dirname);
fulldir = basedir(3:end);
for d = 3:numel(basedir)
    fulldir(d-2).pathname = fullfile(dirname,fulldir(d-2).name);
    if exist( fullfile(dirname, basedir(d).name), 'dir')
        appendingdir = rdir( fullfile(dirname, basedir(d).name) );
        if ~isempty(appendingdir)
            fulldir = [fulldir; appendingdir];
        end
    end
end
  </div>
</body>
</html>
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


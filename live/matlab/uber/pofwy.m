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

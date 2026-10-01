%% Filename: process_corrstats.m
% Project: Matrix of firms via portoflio holdings
% Author: Jesse Blocher
% Date: Nov 2009
% This program processes the results of create_corr_matrices.m
% 

%%
%load matrices
env;
qtrs = 116;

corrstats = zeros(qtrs,2);

for index = 1:qtrs
    %corr_stats = full([dens_neg dens_kept ]);
    filename = ['corr_stats',num2str(index),'.mat'];
    load(fullfile(outpath,filename), 'corr_stats');
    corrstats(index,:) = corr_stats;
end

% now save
filename = 'results_corrstats.mat';
save(fullfile(home,filename),'corrstats');
clear index qtrs filename corr_stats;

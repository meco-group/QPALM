function ub_eig = gershgorin_max(M)
% Use Gershgorin to lower bound the eigenvalues of the matrix M.

for row = 1:size(M,1)
    center = M(row,row);
    radius = sum(abs(M(row,:))) - abs(center);
    if row==1
        ub_eig = center + radius;
    else
        ub_eig = max(center+radius, ub_eig);
    end
end
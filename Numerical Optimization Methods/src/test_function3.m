function [F] = test_function3(x)
n = length(x);
F=0;
for k = 1:n
    if k == 1
        fk = x(k); % fk(x) = xk per k = 1;
    else
        fk = cos(x(k-1)) + x(k) - 1; % fk(x) per 1 < k ≤ n;
    end
    F = F + fk^2;
end
F = 0.5 * F;
end
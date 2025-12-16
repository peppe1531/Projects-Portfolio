function [x_opt, f_opt, iter, rates, simplex_collection] = nelder_mead(f, x0)

% Parameters (fixed and not changeable)
rho = 1;        % Reflection coefficient
chi = 2;        % Expansion coefficient
gamma = 0.5;    % Contraction coefficient
sigma = 0.5;    % Shrinkage coefficient
tol = 1e-13;     % Tolerance for convergence
maxIter = 60000;  % Maximum number of iterations
rates = zeros(maxIter, 1);
X4 = zeros(length(x0), 4);
% Input validation
if nargin < 2
    error('Not enough input arguments. Provide at least a function handle and initial guess.');
end
if ~isa(f, 'function_handle')
    error('First argument must be a function handle.');
end
if ~isvector(x0)
    error('Second argument must be a vector as the initial guess.');
end

% Initialization
n = length(x0); % Dimension of the problem
simplex = zeros(n, n+1); % Preallocate simplex matrix
simplex(:, 1) = x0; % First column is the initial guess
simplex_collection = zeros(n, n+1, maxIter);


for i = 2:n+1
    perturbation = zeros(n, 1);
    perturbation(i-1) = 1; % Perturb along each axis
    simplex(:, i) = x0 + perturbation; % Perturbed vertices
end

% Evaluate the function at the vertices of the simplex
f_vals = zeros(1, n+1);
for i = 1:n+1
    f_vals(i) = f(simplex(:, i));
end
iter=1;
while iter < maxIter && max(abs(f_vals-mean(f_vals)))>=tol
    [f_vals, idx] = sort(f_vals);
    simplex = simplex(:,idx);

    % this if-else is used to compute the experimental rate of convergence
    if iter<=4
        X4(:, iter) = simplex(:, 1);
        if iter==4
            rate = log(norm(X4(:,4)-X4(:,3))/norm(X4(:, 3)-X4(:, 2)))/log(norm(X4(:, 3)-X4(:, 2))/norm(X4(:, 2)-X4(:, 1)));
            rates(iter)=rate;
        end
    else 
        X4 = [X4(:, 2:end), simplex(:, 1)];
        rate = log(norm(X4(:,4)-X4(:,3))/norm(X4(:, 3)-X4(:, 2)))/log(norm(X4(:, 3)-X4(:, 2))/norm(X4(:, 2)-X4(:, 1)));
        rates(iter)=rate;
    end

    simplex_collection(:, :, iter) = simplex;
    
    %reflection phase
    baricenter = mean(simplex(:, 1:n), 2);
    x_reflection = baricenter + rho*(baricenter-simplex(:,n+1));
    f_reflection = f(x_reflection);
    if f_vals(1) <= f_reflection && f_reflection < f_vals(n)
       simplex(:,n+1) = x_reflection;
       f_vals(n+1) = f_reflection;
    
    %expansion phase   
    elseif f_reflection < f_vals(1)
       
       x_expansion = baricenter + chi*(x_reflection-baricenter);
       f_expansion = f(x_expansion);
       
       if f_expansion < f_reflection
           simplex(:,n+1) = x_expansion;
           f_vals(n+1) = f_expansion;
       else 
           simplex(:,n+1) = x_reflection;
           f_vals(n+1) = f_reflection;
       end
    
    %contraction phase
    elseif f_reflection >= f_vals(n)
        
        if f_vals(n+1) < f_reflection
            x_contraction = baricenter - gamma*(baricenter-simplex(:,n+1));
        else
            x_contraction = baricenter - gamma*(baricenter-x_reflection);
        end
        f_contraction = f(x_contraction);

        if f_contraction < f_vals(n+1)
            simplex(:,n+1) = x_contraction;
            f_vals(n+1) = f_contraction;
        else 
            %shrinkage phase
            for j=2:n+1
                simplex(:,j) = simplex(:,1) + sigma*(simplex(:,j)-simplex(:,1));
                f_vals(j) = f(simplex(:,j));
            end
        end
    end
   
    iter = iter+1;
    
end
x_opt = simplex(:,1);
f_opt = f(x_opt);
end



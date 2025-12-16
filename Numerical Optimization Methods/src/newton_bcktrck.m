function [xk, fk, gradfk_norm, k, xseq, btseq, rates] = ...
    newton_bcktrck(x0, f, gradf, Hessf, ...
    kmax, tolgrad, c1, rho, btmax)

farmijo = @(fk, alpha, c1_gradfk_pk) fk + alpha * c1_gradfk_pk;

% Initializations
xseq = zeros(length(x0), kmax);
btseq = zeros(1, kmax);
rates = zeros(kmax, 1);
X4 = zeros(length(x0), 4);
xk = x0;
fk = f(xk);
gradfk = gradf(xk); % computation of gradient
Hessfk = Hessf(xk); % computation of Hessian
k = 1;
gradfk_norm = norm(gradfk);

while k < kmax && gradfk_norm >= tolgrad
    try
        Hk = check_positive_definitess(Hessfk);
    catch ME
        disp('No sufficient positive definite Hessian found')
        break
    end
    R_hessf = sparse(Hk);
    y = R_hessf'\-gradfk;
    pk = R_hessf\y;
    
    % Reset the value of alpha
    alpha = 1;
    
    % Compute the candidate new xk
    xnew = xk + alpha * pk;
    % Compute the value of f in the candidate new xk
    fnew = f(xnew);
    
    c1_gradfk_pk = c1 * gradfk' * pk;
    bt = 0;
    % Backtracking strategy: 
    % 2nd condition is the Armijo condition not satisfied
    while bt < btmax && fnew > farmijo(fk, alpha, c1_gradfk_pk)
        % Reduce the value of alpha
        alpha = rho * alpha;
        % Update xnew and fnew w.r.t. the reduced alpha
        xnew = xk + alpha * pk;
        fnew = f(xnew);
        
        % Increase the counter by one
        bt = bt + 1;
    end
    if bt == btmax && fnew > farmijo(fk, alpha, c1_gradfk_pk)
        break
    end
    
    % Update xk, fk, gradfk_norm
    xk = xnew;
    fk = fnew;

    % this if-else is used to compute the experimental rate of
    % convergence
    if k<=4
        X4(:, k) = xk;
        if k==4
            rate = log(norm(X4(:,4)-X4(:,3))/norm(X4(:, 3)-X4(:, 2)))/log(norm(X4(:, 3)-X4(:, 2))/norm(X4(:, 2)-X4(:, 1)));
            rates(k)=rate;
        end
    else 
        X4 = [X4(:, 2:end), xk];
        rate = log(norm(X4(:,4)-X4(:,3))/norm(X4(:, 3)-X4(:, 2)))/log(norm(X4(:, 3)-X4(:, 2))/norm(X4(:, 2)-X4(:, 1)));
        rates(k)=rate;
    end
    gradfk = gradf(xk);
    gradfk_norm = norm(gradfk);
    Hessfk = Hessf(xk);
    % Increase the step by one
    k = k + 1;
    
    % Store current xk in xseq
    xseq(:, k) = xk;
    % Store bt iterations in btseq
    btseq(k) = bt;
end

xseq = xseq(:, 1:k);
btseq = btseq(1:k);
xseq = [x0, xseq];

end
function [xk, fk, gradfk_norm, k, rates] = ...
    newton_bcktrck_item3_function1(x0, f, ...
    kmax, tolgrad, c1, rho, btmax)


farmijo = @(fk, alpha, c1_gradfk_pk) fk + alpha * c1_gradfk_pk;

rates = zeros(kmax, 1);
X4 = zeros(length(x0), 4);
xk = x0;
fk = f(xk);
[Hessfk, gradfk] = hessian_gradient_test_function1(xk); % computation of the Hessian and gradient
k = 1;
gradfk_norm = norm(gradfk);

while k < kmax && gradfk_norm >= tolgrad
    disp(k)
    disp(Hessfk(1, 1))
    disp(gradfk_norm)
    disp(fk)
    try
        Hk = check_positive_definitess(Hessfk);
    catch ME
        disp(ME.message)
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
        disp('Maximum number of backtracks has been reached')
        break
    end
    
    % Update xk, fk, gradfk_norm
    xk = xnew;
    fk = fnew;

    % this if-else is used to compute the experimental rate of convergence
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
    
    [Hessfk, gradfk] = hessian_gradient_test_function1(xk);
    gradfk_norm = norm(gradfk);
    
    % Increase the step by one
    k = k + 1;
    
   
end



end
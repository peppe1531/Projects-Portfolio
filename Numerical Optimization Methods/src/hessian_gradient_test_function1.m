function [H, grad] = hessian_gradient_test_function1(x)
    n = length(x);

    % compute the Hessian
    H = sparse(n, n);
    for i = 2:n
            % Main diagonal
            H(i-1, i-1) = H(i-1, i-1) + (1200 * x(i-1)^2 - 400 * x(i) + 2);
            H(i, i) = H(i, i) + 200;
            
            % Elements outside the main diagonal
            H(i-1, i) = - 400 * x(i-1);
            H(i, i-1) = H(i-1, i); % Exploit the symmetry of the Hessian
    end
    
    %compute the gradient
    grad = zeros(n,1);
    
  
    for i=1:n
        if i==1
            grad(i) = 400*x(i)*(x(i)^2-x(i+1))+2*(x(i)-1);
        elseif i==n
            grad(i) = -200*(x(i-1)^2-x(i));
        else
            grad(i) = -200*(x(i-1)^2-x(i)) + 400*x(i)*(x(i)^2-x(i+1))+2*(x(i)-1);
        end
    end
end


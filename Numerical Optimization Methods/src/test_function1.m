function F = test_function1(x)
n = length(x);

    if n < 2
        error('The point x must have at least two components');
    end

    F = 0;
    for i = 2:n
        F = F + 100 * (x(i-1)^2 - x(i))^2 + (x(i-1) - 1)^2;
    end
end
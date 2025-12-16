function [y] = test_function2_1(x)
y=0;
for k=1:length(x)
    if k==1
        y = y + k*(1-cos(x(k))+sin(0)-sin(x(2)));
    elseif k==length(x)
        y = y + k*(1-cos(x(k))+sin(x(k-1))-sin(0));
    else
        y = y + k*(1-cos(x(k))+sin(x(k-1))-sin(x(k+1)));
    end
end
end
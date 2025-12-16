function [R] = check_positive_definitess(Hk)
beta = 10^-3;
min_el_diag = min(diag(Hk)); % take the minimum element of the diagonal of 
% the Hessian
already_notified = 0;
tau_max=5;
tau=0;
if min_el_diag>0
    tau=0;
else
    tau = -min_el_diag+beta;
end
while 1
    Bk = sparse(Hk+tau*speye(size(Hk))); % update slightly the Hessian to 
    % make it sufficiently positive definite
    try
        R = sparse(chol(Bk)); % if the Hessian is sufficiently positive 
        % definite, the chol command will work
        break;
    catch ME % otherwise update tau to continue modifing the Hessian, until
        % the maximum threshold tau_max is reached.
        if contains(ME.message, 'positive definite')
            if already_notified==0
                disp('the modifing of the Hessian was needed')
                already_notified=1;
            end
            tau = max([2*tau, beta]);
            if tau>=tau_max
                error('Tau exceeded the maximum allowed value (%e)', tau_max)
            end
        end

    end
end
end
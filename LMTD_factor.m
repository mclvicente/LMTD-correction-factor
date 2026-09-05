function LMTD_factor(T1, T2, t1, t2)

P = (t2 - t1) / (T1 - t1);
R = (T1 - T2) / (t2 - t1);

configs = [1 2 3 4 5 6];
labels = {"1-2", "2-4", "3-6", "4-8", "5-10", "6-12"};

fprintf("P = %.4f   R = %.4f\n\n", P, R);
fprintf("%-15s%10s\n", "Configuration", "Ft");
fprintf("%s\n", repmat('-', 1, 25));

for i = 1:length(configs)
    N = configs(i);
    F = ft_n_shells(P, R, N);
    if isnan(F)
        fprintf("%-15s%10s\n", labels{i}, "invalid");
    else
        fprintf("%-15s%10.8f\n", labels{i}, F);
    end
end

end


function F = ft_one_shell(P, R)

if P <= 1e-12
    F = 1.0;
    return
end

if abs(R - 1.0) < 1e-6
    num = P * sqrt(2) / (1 - P);
    arg_num = 2 - P * (2 - sqrt(2));
    arg_den = 2 - P * (2 + sqrt(2));
    if arg_den <= 0
        F = NaN;
        return
    end
    F = num / log(arg_num / arg_den);
    return
end

S = sqrt(R^2 + 1);
arg_num = 2 / P - 1 - R + S;
arg_den = 2 / P - 1 - R - S;
if arg_den <= 0
    F = NaN;
    return
end

numerator = S * log((1 - P) / (1 - R * P));
denominator = (R - 1) * log(arg_num / arg_den);
F = numerator / denominator;

end


function P1 = equivalent_P1(P, R, N)

if abs(R - 1.0) < 1e-6
    P1 = P / (N - (N - 1) * P);
    return
end

base = (1 - P * R) / (1 - P);
if base <= 0
    P1 = NaN;
    return
end

W = base ^ (1.0 / N);
P1 = (W - 1) / (W - R);

end


function F = ft_n_shells(P, R, N)

if P <= 1e-12
    F = 1.0;
    return
end

P1 = equivalent_P1(P, R, N);
if isnan(P1)
    F = NaN;
    return
end

F = ft_one_shell(P1, R);

end
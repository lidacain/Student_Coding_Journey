initial_capital = 1000;
months = 12;

capital_history = zeros(28, months + 1);

investments = [
    500, 500;
600, 400;
400, 600;
700, 300;
300, 700;
800, 200;
200, 800;
900, 100;
100, 900;
1000, 0;
0, 1000;
950, 50;
50, 950;
980, 20;
20, 980;
990, 10;
10, 990;
995, 5;
5, 995;
997, 3;
3, 997;
998, 2;
2, 998;
999, 1;
1, 999;
0, 1000;
1000, 0;
111, 889;
];


monthly_returns = zeros(1, months);
monthly_returns(1) = (1 + 0.15) ^ (1 / 12);
monthly_returns(2) = (1 + 0.08) ^ (1 / 12);

monthly_returns(3) = 1.03;
monthly_returns(4) = 1.02;
monthly_returns(8) = 0.97;

for i = 1:28
capital = initial_capital;
capital_history(i, 1) = capital;

for month = 1:months
stock_investment = investments(i, 1);
bond_investment = investments(i, 2);

capital = capital + stock_investment * monthly_returns(
    mod(month, length(monthly_returns)) + 1) + bond_investment * monthly_returns(
    mod(month, length(monthly_returns)) + 1);
capital_history(i, month + 1) = capital;
end
end

figure;
plot(0: months, capital_history
');
xlabel('Month');
ylabel('Capital');
title('Capital Dynamics for Different Investment Scenarios');
legend('Equal', 'Option 2', 'Option 3', 'Option 4', 'Option 5', 'Option 6', 'Option 7', 'Option 8', 'Option 9',
       'Option 10', 'Option 11', 'Option 12', 'Option 13', 'Option 14', 'Option 15', 'Option 16', 'Option 17',
       'Option 18', 'Option 19', 'Option 20', 'Option 21', 'Option 22', 'Option 23', 'Option 24', 'Option 25',
       'Option 26', 'Option 27', 'Option 28');
grid
on;
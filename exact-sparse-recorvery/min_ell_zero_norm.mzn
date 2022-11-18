int: dim_signal;
int: dim_measurement;
int: K;
float: precision = 0.001;

set of int: Ns = 1..dim_signal;
set of int: Ms = 1..dim_measurement;

array[Ns] of float: x0;
array[Ms, Ns] of float: A;
array[Ms] of float: y;

array[Ns] of var -10.0..10.0: x;
var int: norm;

constraint forall (m in Ms) (
    y[m] = sum(n in Ns)(A[m,n]*x[n])
);

constraint norm = count(i in x)(i!=0);

constraint norm = K;

solve :: float_search(x, precision, smallest, indomain_min) minimize norm;
% solve minimize norm;

output ["推定:   "] ++ [ "\(i), " | i in x ] ++
       [ "\n" ] ++
       ["L0ノルム: "] ++ [ "\(norm)" ] ++
       [ "\n" ] ++
       [ "\n" ] ++
       ["原信号: "] ++ [ "\(i), " | i in x0 ] ++
       [ "\n" ] ++
       ["L0ノルム: "] ++ [ "\(K)" ];

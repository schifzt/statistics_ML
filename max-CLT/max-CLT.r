# Description:
#     Let X1,...Xn follo iid Gaussian N(0,1).
#     Then, E[max{X1,...,Xn}] = sqrt{ 2log(n) - log(2pi) - loglog(n^2/(2pi)) } + o(log(n))
#
#     Plot n vs Xi(red), max{X1,...,Xn}(blue)
#
# Reference:
#     + https://math.stackexchange.com/questions/89030/expectation-of-the-maximum-of-gaussian-random-variables
#     + Fisher–Tippett–Gnedenko theorem
#         + https://en.wikipedia.org/wiki/Fisher%E2%80%93Tippett%E2%80%93Gnedenko_theorem


# =========================================
# データ作成
# =========================================

T = 20
N = 1000

# N*Tの空データフレームを事前に作成しておく
createEmptyDf = function(nrow, ncol, colnames = c()) {
  data.frame(matrix(vector(), nrow, ncol, dimnames = list(c(), colnames)))
}

df <-
  createEmptyDf(N * T,
                7,
                colnames = c("n", "sim", "simX", "simMax", "simMin", "theoryMax", "theoryMin"))

# T回シミュレーションする
for (t in 0:(T - 1)) {
  X <- rnorm(N, 0, 1)
  for (n in 1:N) {
    df$sim[t * N + n] <- toString(t)
    df$n[t * N + n] <- n
    df$simX[t * N + n] <- X[n]
    df$simMax[t * N + n] <- max(X[1:n])
    df$simMin[t * N + n] <- min(X[1:n])
    
    if (n == 1 || n == 2) {
      df$theoryMax[t * N + n] <- 0
      df$theoryMin[t * N + n] <- 0
    } else{
      df$theoryMax[t * N + n] <-
        sqrt(2 * log(n) - log(2 * pi) - log(2 * log(n) - log(2 * pi)))
      df$theoryMin[t * N + n] <- -df$theoryMax[n]
    }
  }
}

# =========================================
# グラフ
# =========================================
library(ggplot2)
source(file = "../theme_m.r")
g <- ggplot()

g <- g + theme_m()
g <- g +
  scale_x_continuous(sec.axis = dup_axis()) +
  scale_y_continuous(sec.axis = dup_axis())


# Xnをプロット
g <- g + geom_line(aes_string("n", "simX", group = "sim"), df, colour = alpha("blue", 0.1))

# max{X1,...Xn}をプロット
g <- g + geom_line(aes_string("n", "simMax", group = "sim"), df, colour = alpha("red", 0.8))
g <- g + geom_line(aes_string("n", "simMin", group = "sim"), df, colour = alpha("red", 0.8))

# 理論値をプロット
g <- g + geom_line(aes_string("n", "theoryMax", group = "sim"), df, colour = alpha("black", 1.0), linetype = "dashed")
g <- g + geom_line(aes_string("n", "theoryMin", group = "sim"), df, colour = alpha("black", 1.0), linetype = "dashed")

# 軸ラベル
g <- g + xlab("n")
g <- g + ylab("max(X1,...,Xn), Xn")

plot(g)

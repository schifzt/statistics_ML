N = 10000
M = 10

# N*Mの空データフレームを事前に作成しておく
createEmptyDf = function(nrow, ncol, colnames = c()){
    data.frame(matrix(vector(), nrow, ncol, dimnames = list(c(), colnames)))
}

col.names <- paste("s", as.character(1:M), sep = "")
df = createEmptyDf(N, M+1, colnames = c(col.names,"idx"))
df$idx <- 1:N

# M回シミュレーションする
for (sim in 1:M) {
    x = rchisq(N,10,0)
    mu = 10

    sum <- 0
    z <- rep(0, length = N)


    for (n in 1:N) {
      sum <- sum + x[n]
      # z[n] <- sum / n # Law of Large Numbers
      z[n] <- (sum / n - mu) * sqrt(n) # Centrl Limit Theorem
      # z[n] <- (sum / n - mu) * n^(1/3)
    }

    df[, sim] <- z
}

# 一つの図にまとめて折れ線プロットためにdfを縦1列の縦長に変換する（常套手段）
library(tidyr)
df2 <- df %>% tidyr::gather("id", "value", 1:M)

library(ggplot2)
ggplot() +
  geom_line(aes(idx, value, group = id), df2, colour = alpha("grey", 0.7))

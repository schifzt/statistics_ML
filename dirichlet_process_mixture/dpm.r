# ---------------------------------------
# dpmによるクラスタリング
#
# p(x_n|mu; lambda) = N(mu, lambda)
# p(mu;m, lambda_mu) = N(m, lambda_mu)
# ---------------------------------------

                                    # 1次元データ（入力）
x <- data.frame(data=rnorm(100, -2, 1), group_=1)
x <- rbind(x,data.frame(data=rnorm(100, 0, 1), group_=2))
x <- rbind(x,data.frame(data=rnorm(100, 2, 1), group_=3))
x <- rbind(x,data.frame(data=rnorm(100, 4, 1), group_=4))
x <- rbind(x,data.frame(data=rnorm(100, 10, 1), group_=5))

N <- length(x$data)                 # データ数
s <- 1:N                            # 各データの所属クラスタ（出力）
K <- N                              # クラスタ数（出力）
nc <- rep(1, K)                     # 各クラスタに属するデータ数

mu <- x$data                        # p(x_n|mu; lambda)の平均（出力）
lambda <- 1.0                       # p(x_n|mu; lambda)の精度
m <- 0.0                            # p(mu)の平均
lambda_mu <- 1                      # p(mu)の精度

                                    # DPの集中度
alpha <- 0.00001
Pmax <- 0                           # 事後確率の最大値

loop <- 1
while(TRUE){
    # 所属クラスタの更新
    for (n in 1:N) {
        k <- s[n]
        # x_nをクラスタs_nから除外する
        nc[k] <- nc[k] -1
        if (nc[k] == 0) {
            K <- K-1
            nc <- nc[-k]
            mu <- mu[-k]
            s[which(s>k)] <- s[which(s>k)]-1
        }

        Q <- rep(1, K+1)
        # カテゴリ分布のパラメータ（既存クラスタ）を計算する
        for (k in 1:K) {
              Q[k] <- nc[k]/(N-1+alpha)*dnorm(x$data[n], mu[k], 1/lambda)
        }
        # カテゴリ分布のパラメータ（新規クラスタ）を計算する
        Q[K+1] <- alpha/(N-1+alpha)*dnorm(x$data[n], m, (lambda+lambda_mu)/(lambda*lambda_mu))
        #
        # s_nをカテゴリ分布からサンプリングする
        s[n] <- which(rmultinom(1, 1, Q)==1)

        if(s[n]==K+1){
            nc[K+1] <- 1
            mu[K+1] <- 1
            K <- K+1
        }else{
            nc[s[n]] <- nc[s[n]] +1
        }

    }


    # パラメータの更新
    for(k in 1:K){
        # s[n]==kとなるnが存在するならば
        if(length(s[s==k])!=0){
            set_k <- which(s==k)

            mu_ <- (sum(x$data[set_k])*lambda +m *lambda_mu)/(nc[k] *lambda +lambda_mu)
            lambda_ <- nc[k]*lambda +lambda_mu

            mu[k] <- rnorm(1, mu_, 1/lambda_)
        }
    }

    # 事後確率の計算
    v <- 1
    for(k in 1:K){
        if(length(s[s==k])!=0){
            set_k <- which(s==k)
            mu_ <- (sum(x$data[set_k])*lambda +m *lambda_mu)/(nc[k] *lambda +lambda_mu)
            lambda_ <- nc[k]*lambda +lambda_mu

            v <- v + log(factorial(nc[k]-1)*dnorm(mu[k], mu_, 1/lambda_))
        }
    }

    # 事後確率最大化
    if(v > Pmax){
        # sを受理，つぎのループはこのsから続ける
        Pmax <- v

        s_save <- s
        nc_save <- nc
        mu_save <- mu
        K_save <- K

        loop <- 1
    }else{
        # sを棄てる
        s <- s_save
        nc <- nc_save
        mu <- mu_save
        K <- K_save

        loop <- loop + 1
    }

    # 終了判定
    if(loop > 30){
        break
    }
}

s <- as.character(s)
xx <- transform(x, group=s)

library(ggplot2)
# ヒストグラム
g1 <- ggplot(xx, aes(data, fill=group))
g1 <- g1 + geom_histogram(aes(y=..count../sum(..count..)), position="dodge")
g1 <- g1 + scale_fill_grey() + theme_bw()

# pdf
g2 <- ggplot(xx, aes(data, fill=group))
for(k in 1:K){
    g2 <- g2 + stat_function(fun=dnorm, args=list(mean=mu[k], sd=1))
}

stick_breaking <- function(G0,gamma){
    Y <- c()
    p <- c()
    cumprod<- 1

    # stickの残りがなくなるまで繰り返す
    while(cumprod > .Machine$double.eps){
        Y <- append(Y, G0(1))
        theta <- rbeta(1,1,gamma)
        p <- append(p, theta*cumprod)
        cumprod <- cumprod*(1-theta)
    }

    G <- data.frame(Y,p)
    G <- G[order(G$Y),]
    G <- transform(G,cdf = cumsum(G$p))

    return(G)
}

library(ggplot2)
library(latex2exp)

library(functional)
G0 <- Curry("rbeta",shape1=0.5,shape2=0.5)
gamma <- 20

pG0 <- Curry("pbeta",shape1=0.5,shape2=0.5)

# Gを10回生成してGsにまとめる
Gs <- transform(GP(G0,gamma), group = 1)
for(i in 2:20){
    Gs <- rbind(Gs,transform(stick_breaking(G0,gamma), group = i))
}

ggplot(Gs, aes(x = Y, y = cdf,group=group)) +
    geom_line(color="blue",alpha=0.3) +
    stat_function(fun=pG0,color="red") +
    theme_bw()
    # labs(title=TeX("$G\\sim DP(\\gamma=20, \\G_0=N(0,1))$"))

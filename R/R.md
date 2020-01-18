## R Studio
+ Ctrl-Shift-Enterでコード実行，このときコード編集用のウィンドウを閉じて置く．
+ Ctrl-A + Ctrl-Shift-Aでreformat code
+ 挙動がおかしなときは変数キャッシュのクリアを試してみる
+ `package_installer.r`にデフォルトにないがよく使うパッケージをまとめておいた
+ paneの配置は`View > Panes > Pane Layout...`で変更可能
    + 左にplot，右にconsole，編集は外部エディタ


## data.frame
### 定義
```
df <- data.frame(aaa=1,bbb=1)
df <- data.frame(x,y)       # x,yは定義済みの列ベクトル
str(df) # dfの型を確認
```

### よくやる操作
|操作|コード|
|----|------|
|新しい列を横にくっつける|`dfs <- transform(dfs, group = 1)`|
|新しい行を下にくっつける|`dfs <- rbind(dfs, df_new)`|
|指定した列の値についてソート|`df <- df[order(df$x), ]`|
|-|-|
|マッチするindexを取得|`which(df$x == 1)`|
|マッチする列を取得|`df[df$x == 1, ]`|
|df中のx列のAをBに置換|`df[df$x == A, ]$x = B`,`replace(df$x, which(df$x==A), B)`|
|ベクトルxから指定した要素を削除して詰める|`x[-(3:10)]`|
|-|-|
|dfのindexを生成|`1:nrow(df)`, `as.integer(rownames(df))`|
|dfの列名を取得|`header <- colnames(df)`|
|dfの列名を変更|`colnames(df) <- c("a","b","c")`|

### 整然データ
+ 1行が1観測となるように列の属性を増やす
+ 何個目の観測かを表す列属性を追加してもよい
+ `library(tidyverse)`を使う
+ いわゆる整然データツール(ggplot2など)は整然データを入力に想定しているので前準備が重要
    + 複数のシミュをdfsにまとめる --> ggplot2を最後に1回だけ使う(`aes(group=hoge)`を使う）
    + シミュを横に横にくっつけていくのは悪筋．
    + 区別するための列（group=1など）を新たに追加-->下に下にくっつける
+ `gather`:クロステーブルのタテヨコ属性を列属性にもつデータフレームに変換する
    +

## ggplot
### 折れ線グラフ
1. 現在，dfの列名は，"id, k0, k1, k2"だとする
    + もし，id列がない場合はこの段階で`df <- transform(df, id = 1:nrow(df))`として追加しておく
2. `df <- df %>% tidyr::gather(key = "k", value = "data", k0, k1, k2)`
    + ggplotに渡す整然データの列名："id, k, data"
3. `ggplot(df, aes(x = id, y = u, color = k)) + geom_line()`
    + `color`や`group`を指定することで結ぶ点列を指定できる

## 3次元plot
+ ggplotには3次元plotはないので`library(lattice)`を使う
### wireframe
+ 入力
    + 整然データ, 列名："x, y, z"
    + 全て数値型`df<-as.numeric(df$x)`,`df<-as.integer(df$x)`で変換しておく
```
# "k1" --> 1に変換
for (i in 0:6) {
  s = paste("k", i, sep = "")
  df2[df$k == s,]$k = i
}
df2$k <- as.integer(df2$k)

wireframe(z ~ x * y,
          data = df,
          aspect = c(61 / 89, 0.3),
          shade = TRUE)
```

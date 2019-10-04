import os

# ./のディレクトリ名を取得
dirs = os.listdir("./")
dirs = list(filter(os.path.isdir, dirs))

# タイトル
s = "# Statistics & Machine Learning\n"

# 目次
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir("./{0}".format(d)) if f.name.endswith(".png")]

    # png画像を含むディレクトリならREADMEに記入
    if not imgs==[]:
        s=s+"+ [{0}](#{0})\n".format(d)

# 本文
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir("./{0}".format(d)) if f.name.endswith(".png")]

    # png画像を含むディレクトリならREADMEに記入
    if not imgs==[]:
        s = s+"""
## [{0}]({0})
![{1}]({0}/{1})
""".format(d, imgs[0])

with open("./README.md", mode="w") as f:
    f.write(s)
f.close()

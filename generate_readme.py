import os

# ./のディレクトリ名を取得
dirs = os.listdir("./")
dirs = list(filter(os.path.isdir, dirs))
dirs.remove("R")
dirs.remove(".git")

# タイトル
s = "# Statistics & Machine Learning\n\n"

# 目次
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir(
        "./{0}".format(d)) if f.name.endswith(".png")]
    s = s+"+ [{0}](#{0})\n".format(d)

# 本文
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir(
        "./{0}".format(d)) if f.name.endswith(".png")]

    if not imgs == []:    # ディレクトリがpng画像を含む場合
        s = s+"""
## [{0}]({0})
![{1}]({0}/{1})
""".format(d, imgs[0])
    else:               # ディレクトリがpng画像を含む場合
        s = s+"""
## [{0}]({0})
""".format(d)

with open("./README.md", mode="w") as f:
    f.write(s)
f.close()

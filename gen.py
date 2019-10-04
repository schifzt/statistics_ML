import os

# ./のディレクトリ名を取得
dirs = os.listdir("./")
dirs = list(filter(os.path.isdir, dirs))


s = "## Statistics & Machine Learning"
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir("./{0}".format(d)) if f.name.endswith(".png")]

    # png画像があればREADMEに記入
    if not imgs==[]:
        s = s+"""
### [{0}]("/{0}")
![img]("/{0}/{1}")
""".format(d, imgs[0])

with open("./README.md", mode="w") as f:
    f.write(s)
f.close()

import os

# ./のディレクトリ名を取得
dirs = os.listdir("./")
dirs = list(filter(os.path.isdir, dirs))

# 無視するディレクトリを指定
ignore_dirs = [".git", "lib"]
for d in ignore_dirs:
    if d in dirs:
        dirs.remove(d)

# タイトル
s = "# Statistics & Machine Learning\n\n"

# 目次
for d in dirs:
    # d内のpng画像を取得
    imgs = [f.name for f in os.scandir(
        "./{0}".format(d)) if f.name.endswith(".png")]
    s = s + "- [{0}](#{0})\n".format(d)

# 本文
for d in dirs:
    # d内のpng画像を取得
    imgs = [file.name for file in os.scandir(f"./{d}") if file.name.endswith(".png")]

    if not imgs == []:    # ディレクトリがpng画像を含む場合
        s = s + f"""
## [{d}]({d})
![{imgs[0]}]({d}/{imgs[0]})
"""
    else:               # ディレクトリがpng画像を含まない場合
        s = s + f"""
## [{d}]({d})
"""

with open("./README.md", mode="w") as f:
    f.write(s)
f.close()

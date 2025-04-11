
scale = float(4/3)

# 替换脚本中坐标
if __name__ == '__main__':
    with open("哎呦.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.replace("\n", "")
            if "," in line:
                tmp = []
                for w in line.split(" "):
                    if "," in w:
                        split = w.split(",")
                        tmp.append(f"{round(int(split[0]) / scale)},{round(int(split[1]) / scale)}")
                    else:
                        tmp.append(w)
                print(" ".join(tmp))
            else:
                print(line)
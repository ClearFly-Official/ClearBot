import os, glob, re

cmnac = []
output = []
index = 0
cmndest = []
for filename in glob.glob('ClearFly_VA/users/*/*'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        lines = f.readlines()
        cmndest = cmndest+lines
def delstr2(lst):
      return [
          f"{''.join(elem.split()[2:]).rstrip()}"
          for elem in lst
      ]

if __name__ == "__main__":
    cmndest = delstr2(cmndest)
    for x in cmndest:
      x = re.sub(r'.', '', x, count = 5)
      output.append(x)
    print(output)

def most_frequent(List):
            return max(set(List), key = List.count)

if __name__ == "__main__":
    output = list(filter(None, output))
    cmndest = most_frequent(output)
    print(cmndest)
    print("e")
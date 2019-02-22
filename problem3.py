import sys

class TreeError(Exception):
    pass  # make it fancier if you want :)

class Leaf:
    def __init__(self):
        self.p = None
        self.red = False

    def __bool__(self):
        return False

class RedBlackNode:
    def __init__(self, num):
        self.num = num
        self.red = True
        self.right = Leaf()
        self.left = Leaf()
        self.p = None
        self.right.p = self
        self.left.p = self

    def __bool__(self):
        return True

    def __str__(self):
        return str(self.num)

class RedBlackTree:
    def __init__(self):
        self.root = Leaf()

    def insert(self, z):
        x = self.root
        y = None
        while x:
            y = x
            if z < x.num:
                x = x.left
            else:
                x = x.right
        x2 = RedBlackNode(num = z)
        x2.p = y
        if not y:
            self.root = x2
            self.root.red = False
            return
        elif z < y.num:
            y.left = x2
        else:
            y.right = x2
        x = x2
        y = x.p
        while x != self.root and y.red:
            pp = y.p
            if y == pp.left:
                uncle = pp.right
                if uncle.red:
                    y.red = False
                    uncle.red = False
                    pp.red = True
                    x = pp
                    y = x.p
                else:
                    if x == y.right:
                        x = y
                        self.leftRotate(x)
                        y = x.p
                    pp = y.p
                    self.rightRotate(pp)
            else:
                uncle = pp.left
                if uncle.red:
                    y.red = False
                    uncle.red = False
                    pp.red = True
                    x = pp
                    y = x.p
                else:
                    if x == y.left:
                        x = y
                        self.rightRotate(x)
                        y = x.p
                    pp = y.p
                    self.leftRotate(pp)
        self.root.red = False

    def transplant(self, u, v):
        if not u.p:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
            v.p = u.p

    def rb_delete(self, z):
        x = self.root
        if not x:
            raise ValueError
        while x:
            if z == x.num:
                z = x
                break
            elif z < x.num:
                x = x.left
            elif z > x.num:
                x = x.right
            else:
                raise ValueError
        z2 = z
        z2_color = z2.red
        if not z.right:
            z3 = z.left
            self.transplant(z, z.left)
        if not z.left:
            z3 = z.right
            self.transplant(z, z.right)
        else:
            z2 = z.right
            while z2.left:
                z2 = z2.left
            z2_color = z2.red
            z3 = z2.right
            if z2.p == z:
                z3.p = z2
            else:
                self.transplant(z2, z2.right)
                z2.right = z.right
                z2.right.p = z2
            self.transplant(z, z2)
            z2.left = z.left
            z2.left.p = z2
            z2.red = z.red
            if not z2_color:
                self.rb_delete_fixup(z3)

    def rb_delete_fixup(self, z):
        while not z.red and z != self.root:
            if z != z.p.left:
                w = z.p.left
                if w.red:
                    w.red = False
                    z.p.red = True
                    self.rightRotate(z.p)
                    w = z.p.left
                if not w.left.red:
                    w.right.red = False
                    w.red = True
                    self.leftRotate(w)
                    w = z.p.left
                elif not w.right.red and not w.left.red:
                    w.red = True
                    z = z.p
                w.red = z.p.red
                z.p.red = False
                w.left.red = False
                self.rightRotate(z.p)
                z = self.root
            else:
                w = z.p.right
                if w.red:
                    w.red = False
                    z.p.red = True
                    self.leftRotate(z.p)
                    w = z.p.right
                if not w.right.red:
                    w.left.red = False
                    w.red = True
                    self.rightRotate(w)
                    w = z.p.right
                elif not w.right.red and not w.left.red:
                    w.red = True
                    z = z.p
                w.red = z.p.red
                z.p.red = False
                w.right.red = False
                self.leftRotate(z.p)
                z = self.root
        z.red = False

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.p = x
        y.p = x.p
        if not x.p:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.left = x
        x.p = y
        y.red,x.red = False,True
        return y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.p = x
        y.p = x.p
        if not x.p:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y
        y.red,x.red = False,True
        return y

    def max(self):
        if not self.root:
            raise TreeError
        root = self.root
        while root.right:
            root = root.right
        return str(root.num)

    def min(self):
        if not self.root:
            raise TreeError
        root = self.root
        while root.left:
            root = root.left
        return str(root.num)

    def search(self, x):
        root = self.root
        while root and x != root.num:
            if x > root.num:
                root = root.right
            else:
                root = root.left
        return bool(root)

    def inprint(self,x,p):
        if not self.root:
            raise TreeError
        elif x:
            self.inprint(x.left,p)
            p.append(x.num)
            self.inprint(x.right,p)
        return p

def driver():
    T = RedBlackTree()
    with open(sys.argv[1]) as f:
        n = int(f.readline().strip())
        for _ in range(n):
            in_data = f.readline().strip().split()
            action, value_option = in_data[0], in_data[1:]
            if action == "insert":
                value = int(value_option[0])
                T.insert(value)
            elif action == "remove":
                try:
                    node = int(value_option[0])
                    T.rb_delete(node)
                except:
                    print("TreeError")
            elif action == "search":
                s = T.search(int(value_option[0]))
                if s == True:
                    print("Found")
                else:
                    print("NotFound")
            elif action == "max":
                try:
                    print(T.max())
                except:
                    print("Empty")
            elif action == "min":
                try:
                    print(T.min())
                except:
                    print("Empty")
            elif action == "inprint":
                try:
                    p = map(str, T.inprint(T.root,[]))
                    print(' '.join(p))
                except:
                    print("Empty")



if __name__ == "__main__":
    driver()

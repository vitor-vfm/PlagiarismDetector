"""
Ukkonen's Suffix Tree Construction, as per
http://www.geeksforgeeks.org/suffix-tree-application-5-longest-common-substring-2/

Beware:
Here be dragons
"""


class SuffixTreeNode:

    class NodeEnd:
        '''
        This is a hack, works as a replacement for pointers
        '''
        def __init__(self, value):
            self.value = value

    def __init__(self, start, end, tree):
        if not isinstance(end, SuffixTreeNode.NodeEnd):
            raise ValueError(end)  # Mostly for debuging, so that we don't pass in a value thats not wrapped

        self.children = dict()
        self.suffixLink = tree.root  # shortcuts 
        # Start and end show the interval which the child node stores
        self.start = start
        self.end = end
        # Leaf nodes store the index of their suffix from root to leaf
        self.suffixIndex = -1

    def edgeLength(self, tree):
        if self == tree.root:
            return 0
        else:
            return self.end.value - self.start + 1

    def walkDown(self, tree):
        """
        This makes the algorithm proportional to node count and not to character count
        when walking down the tree to the leaf
        """
        if tree.activeLength >= self.edgeLength(tree):
            tree.activeEdge += self.edgeLength(tree)
            tree.activeLength -= self.edgeLength(tree)
            tree.activeNode = self
            return True
        return False


class SuffixTree:
    def __init__(self, text1, text2):
        self.root = None
        self.text = text1 + "\0" + text2 + "\a"  # Here the NUL and the bell characters represent string seperators
        # They are such chosen as they will not appear in normal text, hence unique, ensuring text1 and text2 have 
        # no common suffix, this is as per the general suffix tree construction
        self.size1 = len(text1) + 1
        self.remainingSuffixCount = 0  # tracks how many extensions need to be performed
        self.activeLength = 0  # how many characters we need to walk down to find the activePoint for extension
        self.leafEnd = SuffixTreeNode.NodeEnd(0)  # This is where the 'hack' comes in, as many nodes are assigned this
        # quasi-pointer, for which the value can be updated easily
        pass

    def extendSuffixTree(self, pos):
        self.leafEnd.value = pos  # here is the hack again, we init the pointer here and then assign it to nodes
        self.remainingSuffixCount += 1
        self.lastNewNode = None

        while self.remainingSuffixCount > 0:
            if self.activeLength == 0:
                self.activeEdge = pos  # we are at the active point, hence current character is the extesnion

            if self.text[self.activeEdge] not in self.activeNode.children:
                #  Create a new edge if it doen't exist, with the current active character
                self.activeNode.children[self.text[self.activeEdge]] = SuffixTreeNode(pos, self.leafEnd, self)

                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None

            else:
                # Otherwise, we can keep going 
                nextNode = self.activeNode.children[self.text[self.activeEdge]]
                if nextNode.walkDown(self):
                    continue
                elif self.text[nextNode.start + self.activeLength] == self.text[pos]:
                    # Same character so we can just connect them
                    if self.lastNewNode is not None and self.activeNode != self.root:
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    self.activeLength += 1
                    break
                else:
                    # Do the extension
                    self.splitEnd = SuffixTreeNode.NodeEnd(nextNode.start + self.activeLength - 1)
                    splitNode = SuffixTreeNode(nextNode.start, self.splitEnd, self)

                    self.activeNode.children[self.text[self.activeEdge]] = splitNode
                    splitNode.children[self.text[pos]] = SuffixTreeNode(pos, self.leafEnd, self)
                    nextNode.start += self.activeLength
                    splitNode.children[self.text[nextNode.start]] = nextNode

                    if self.lastNewNode is not None:
                        self.lastNewNode.suffixLink = splitNode

                    self.lastNewNode = splitNode
            # just did one extension
            self.remainingSuffixCount -= 1

            if self.activeNode == self.root and self.activeLength > 0:
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif self.activeNode != self.root:
                self.activeNode = self.activeNode.suffixLink # follow our shortcut

    def setSuffixIndexByDFS(self, node, labelHeight):
        # Here we're just labelling the tree, that is wether a node
        # belongs to text1, text2 or both. 
        if node is None:
            return

        leaf = 1
        for n in node.children.values():
            leaf = 0
            self.setSuffixIndexByDFS(n, labelHeight + n.edgeLength(self))

        if leaf == 1:
            for i in range(node.start, node.end.value+1):
                if self.text[i] == '\0':
                    node.end = SuffixTreeNode.NodeEnd(i)
                    break

            node.suffixIndex = len(self.text) - labelHeight

    def buildSuffixTree(self):
        self.root = SuffixTreeNode(-1, SuffixTreeNode.NodeEnd(-1), self)
        self.activeNode = self.root
        for i in range(0, len(self.text)):
            self.extendSuffixTree(i)
        self.setSuffixIndexByDFS(self.root, 0)

    def doTraversal(self, node, labelHeight):
        # Traverse the tree, such that we record the path that is shared by both text1 and text2
        if node is None:
            return
        ret = -1

        if node.suffixIndex < 0:
            for n in node.children.values():
                ret = self.doTraversal(n, labelHeight+n.edgeLength(self))

                if node.suffixIndex == -1:
                    node.suffixIndex = ret
                elif (node.suffixIndex == -2 and ret == -3)\
                    or (node.suffixIndex == -3 and ret == -2)\
                        or node.suffixIndex == -4:
                            node.suffixIndex == -4
                            if self.maxHeight < labelHeight:
                                self.maxHeight = labelHeight
                                self.substringStartIndex = node.end.value - labelHeight + 1
        elif node.suffixIndex > -1 and node.suffixIndex < self.size1:
            return -2
        elif node.suffixIndex >= self.size1:
            return -3

        return node.suffixIndex

    def getLCS(self):
        self.maxHeight = 0
        self.substringStartIndex = 0
        self.doTraversal(self.root, 0)
        return self.text[self.substringStartIndex:self.substringStartIndex+self.maxHeight]

class Node:
    def __init__(self, value, left=None, right=None, node_id=None):
        self.value = value  # Stores the operation or symbol
        self.left = left    # Left child
        self.right = right  # Right child
        self.id = node_id   # Unique identifier for the node
        self.nullable = False  # Indicates if the node can derive the empty string
        self.firstpos = set()  # Set of first positions
        self.lastpos = set()   # Set of last positions

    def __repr__(self, level=0, prefix="Root: "):
        result = "\t" * level + prefix + repr(self.value) + f" (ID: {self.id})\n"
        if self.left:
            result += self.left.__repr__(level + 1, "L--- ")
        if self.right:
            result += self.right.__repr__(level + 1, "R--- ")
        return result

    def calculate_followpos(self):
        followpos = {}
        self._calculate_followpos_recursive(followpos)
        return followpos

    def _calculate_followpos_recursive(self, followpos):
        if self.left:
            self.left._calculate_followpos_recursive(followpos)
        if self.right:
            self.right._calculate_followpos_recursive(followpos)

        if self.value == '.':
            # Concatenation: add lastpos of left to firstpos of right
            for pos in self.left.lastpos:
                if pos not in followpos:
                    followpos[pos] = set()
                followpos[pos].update(self.right.firstpos)
        elif self.value == '*':
            # Star operation: add lastpos to firstpos
            for pos in self.lastpos:
                if pos not in followpos:
                    followpos[pos] = set()
                followpos[pos].update(self.firstpos)

    def get_max_node_id(self):
        max_id = self.id if self.id is not None else 0  # Start with current node's id
        if self.left:
            max_id = max(max_id, self.left.get_max_node_id())  # Check left child
        if self.right:
            max_id = max(max_id, self.right.get_max_node_id())  # Check right child
        return max_id  # Return the maximum id found


def parse_regex(expr):
    def parse_expression(i, node_id=0):
        nodes = []
        while i < len(expr):
            if expr[i] == '(':
                # Parse a subexpression
                subexpr, i = parse_expression(i + 1, node_id)
                nodes.append(subexpr)
            elif expr[i] == ')':
                # End of a subexpression
                break
            elif expr[i] == '*':
                # Apply star operation to the last node
                last_node = nodes.pop()
                node = Node('*', left=last_node)
                node.nullable = True
                node.firstpos = last_node.firstpos
                node.lastpos = last_node.lastpos
                nodes.append(node)
            elif expr[i] == '|':
                # Union operation (needs two children)
                left = Node('|', left=nodes.pop())
                subexpr, i = parse_expression(i + 1, node_id)
                left.right = subexpr
                left.nullable = left.left.nullable or left.right.nullable
                left.firstpos = left.left.firstpos.union(left.right.firstpos)
                left.lastpos = left.left.lastpos.union(left.right.lastpos)
                nodes.append(left)
            elif expr[i] == '&':
                # Append symbol (concatenation handled later)
                node = Node(expr[i])
                node.nullable = True
                node.firstpos = set()
                node.lastpos = set()
                nodes.append(node)
            else:
                # Append symbol (concatenation handled later)
                node_id += 1
                node = Node(expr[i], node_id=node_id)
                node.nullable = False
                node.firstpos = {node_id}
                node.lastpos = {node_id}
                nodes.append(node)
            i += 1
        
        # Now handle concatenation
        while len(nodes) > 1:
            left = nodes.pop(0)
            right = nodes.pop(0)
            concat_node = Node('.', left, right)
            # Update nullable, firstpos, lastpos for concatenation
            concat_node.nullable = left.nullable and right.nullable
            concat_node.firstpos = left.firstpos.union(right.firstpos) if left.nullable else left.firstpos
            concat_node.lastpos = right.lastpos.union(left.lastpos) if right.nullable else right.lastpos
            nodes.insert(0, concat_node)
        
        return nodes[0], i
   

    root, _ = parse_expression(0)

    # Calculate followpos
    followpos = root.calculate_followpos()
    
    # Add # to followpos of the last positions
    node_id = root.get_max_node_id() + 1
    for pos in root.lastpos:
        if pos not in followpos:
            followpos[pos] = set()
        followpos[pos].add(node_id)

    print("Followpos:", followpos)
    return root

# Test the code with a regular expression
regex = "aa*((b|b*)aa*b)*"
regex = "aa*"
regex = "&|a|bb*"
tree = parse_regex(regex)
print(tree)

# Test the automaton generation
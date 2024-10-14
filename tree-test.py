class Node:
    def __init__(self, value, left=None, right=None, node_id=None):
        self.value = value  # Stores the operation or symbol
        self.left = left    # Left child
        self.right = right  # Right child
        self.id = node_id   # Unique identifier for the node
        self.nullable = False  # Indicates if the node can derive the empty string
        self.firstpos = set()  # Set of first positions
        self.lastpos = set()   # Set of last positions
        self.followpos = set() # Set of follow positions

    def __repr__(self, level=0, prefix="Root: "):
        result = "\t" * level + prefix + repr(self.value) + f" (ID: {self.id})\n"
        if self.left:
            result += self.left.__repr__(level + 1, "L--- ")
        if self.right:
            result += self.right.__repr__(level + 1, "R--- ")
        return result


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
                node_id += 1
                nodes.append(Node('*', left=last_node, node_id=node_id))
            elif expr[i] == '|':
                # Union operation (needs two children)
                left = Node('|', left=nodes.pop(), node_id=node_id)
                subexpr, i = parse_expression(i + 1, node_id)
                left.right = subexpr
                nodes.append(left)
            else:
                # Append symbol (concatenation handled later)
                node_id += 1
                nodes.append(Node(expr[i], node_id=node_id))
            i += 1
        
        # Now handle concatenation
        while len(nodes) > 1:
            left = nodes.pop(0)
            right = nodes.pop(0)
            node_id += 1
            concat_node = Node('.', left, right, node_id=node_id)
            # Update nullable, firstpos, lastpos for concatenation
            concat_node.nullable = left.nullable and right.nullable
            concat_node.firstpos = left.firstpos if left.nullable else left.firstpos.union(right.firstpos)
            concat_node.lastpos = right.lastpos if right.nullable else left.lastpos.union(right.lastpos)
            nodes.insert(0, concat_node)
        
        return nodes[0], i

    root, _ = parse_expression(0)
    return root

# Test the code with a regular expression
regex = "aa*((b|b*)aa*b)*"
regex = "aa*"
tree = parse_regex(regex)
print(tree)

# Test the automaton generation


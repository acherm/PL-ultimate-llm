MODULE BinaryTree;
IMPORT Out;

TYPE
  Tree = POINTER TO Node;
  Node = RECORD
    data: INTEGER;
    left, right: Tree;
  END;

VAR
  root: Tree;

PROCEDURE NewNode(data: INTEGER): Tree;
VAR
  node: Tree;
BEGIN
  NEW(node);
  node.data := data;
  node.left := NIL;
  node.right := NIL;
  RETURN node;
END NewNode;

PROCEDURE Insert(VAR tree: Tree; data: INTEGER);
BEGIN
  IF tree = NIL THEN
    tree := NewNode(data);
  ELSIF data < tree.data THEN
    Insert(tree.left, data);
  ELSIF data > tree.data THEN
    Insert(tree.right, data);
  END;
END Insert;

PROCEDURE Search(tree: Tree; data: INTEGER): BOOLEAN;
BEGIN
  IF tree = NIL THEN
    RETURN FALSE;
  ELSIF data = tree.data THEN
    RETURN TRUE;
  ELSIF data < tree.data THEN
    RETURN Search(tree.left, data);
  ELSE
    RETURN Search(tree.right, data);
  END;
END Search;

PROCEDURE InOrder(tree: Tree);
BEGIN
  IF tree # NIL THEN
    InOrder(tree.left);
    Out.Int(tree.data, 4);
    InOrder(tree.right);
  END;
END InOrder;

BEGIN
  root := NIL;
  Insert(root, 5);
  Insert(root, 3);
  Insert(root, 7);
  Insert(root, 1);
  Insert(root, 4);
  Insert(root, 6);
  Insert(root, 9);
  
  Out.String("In-order traversal: ");
  InOrder(root);
  Out.Ln;
  
  IF Search(root, 4) THEN
    Out.String("Found 4");
  ELSE
    Out.String("Not found 4");
  END;
  Out.Ln;
  
  IF Search(root, 8) THEN
    Out.String("Found 8");
  ELSE
    Out.String("Not found 8");
  END;
  Out.Ln;
END BinaryTree.
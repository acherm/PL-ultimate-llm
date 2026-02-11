MODULE BinaryTree;
IMPORT Out;

TYPE
  Tree = POINTER TO Node;
  Node = RECORD
    data: INTEGER;
    left, right: Tree
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
  RETURN node
END NewNode;

PROCEDURE Insert(VAR t: Tree; data: INTEGER);
BEGIN
  IF t = NIL THEN
    t := NewNode(data)
  ELSIF data < t.data THEN
    Insert(t.left, data)
  ELSIF data > t.data THEN
    Insert(t.right, data)
  END
END Insert;

PROCEDURE Search(t: Tree; data: INTEGER): BOOLEAN;
BEGIN
  IF t = NIL THEN
    RETURN FALSE
  ELSIF data = t.data THEN
    RETURN TRUE
  ELSIF data < t.data THEN
    RETURN Search(t.left, data)
  ELSE
    RETURN Search(t.right, data)
  END
END Search;

PROCEDURE InOrder(t: Tree);
BEGIN
  IF t # NIL THEN
    InOrder(t.left);
    Out.Int(t.data, 4);
    InOrder(t.right)
  END
END InOrder;

PROCEDURE PreOrder(t: Tree);
BEGIN
  IF t # NIL THEN
    Out.Int(t.data, 4);
    PreOrder(t.left);
    PreOrder(t.right)
  END
END PreOrder;

PROCEDURE PostOrder(t: Tree);
BEGIN
  IF t # NIL THEN
    PostOrder(t.left);
    PostOrder(t.right);
    Out.Int(t.data, 4)
  END
END PostOrder;

BEGIN
  root := NIL;
  Insert(root, 5);
  Insert(root, 3);
  Insert(root, 7);
  Insert(root, 1);
  Insert(root, 4);
  Insert(root, 6);
  Insert(root, 9);
  
  Out.String("In-order: "); Out.Ln;
  InOrder(root); Out.Ln;
  
  Out.String("Pre-order: "); Out.Ln;
  PreOrder(root); Out.Ln;
  
  Out.String("Post-order: "); Out.Ln;
  PostOrder(root); Out.Ln;
  
  IF Search(root, 4) THEN
    Out.String("Found 4"); Out.Ln
  END;
  
  IF ~Search(root, 8) THEN
    Out.String("8 not found"); Out.Ln
  END
END BinaryTree.
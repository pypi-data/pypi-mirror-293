import ast
def sparta_3b6f39d7a2(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_b7976c2f87(script_text):return sparta_3b6f39d7a2(script_text)
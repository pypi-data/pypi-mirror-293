import ast
def sparta_3f62c84a93(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_d6aa712234(script_text):return sparta_3f62c84a93(script_text)
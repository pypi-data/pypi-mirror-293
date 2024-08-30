import ast
def sparta_1b368f3232(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_1f5bf743d8(script_text):return sparta_1b368f3232(script_text)
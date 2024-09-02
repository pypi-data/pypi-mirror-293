import ast
def sparta_46a820ec1d(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_da3002080e(script_text):return sparta_46a820ec1d(script_text)
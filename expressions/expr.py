# Solves an expression type problem from Trapez
# Slightly inefficient
# Usage: inputs, target and numberofops
# Python 2
import math
import itertools

class Expr:
	def __init__(self,args):
		self.args = args
		self.depth = max(a.depth for a in args)
		self.vars = sum(a.vars for a in args)
	def eval(self,vlist):
		return None
	def printf(self,vlist=None):
		return ''

class Variable(Expr):
	def __init__(self,n):
		self.args = None
		self.depth = 0
		self.vars = n
	def eval(self,vlist):
		return sum(vlist[self.vars-k-1]*10**k for k in range(self.vars))
	def printf(self,vlist):
		return 'v'*self.vars if vlist is None else ''.join(str(v) for v in vlist)

class Expr1(Expr):
	def eval(self,vlist):
		lhs = self.args[0].eval(vlist)
		if lhs is not None:
			return self.fun(lhs)
		else:
			return None

class Expr1Prefix(Expr1):
	def printf(self,vlist):
		return self.oper+'('+self.args[0].printf(vlist)+')'

class Expr1Postfix(Expr1):
	def printf(self,vlist):
		return self.args[0].printf(vlist)+self.oper

class Expr2(Expr):
	def printf(self,vlist):
		if vlist:
			return '('+self.args[0].printf(vlist[:self.args[0].vars])+self.oper+self.args[1].printf(vlist[self.args[0].vars:])+')'
		else:
			return '('+self.args[0].printf(None)+self.oper+self.args[1].printf(None)+')'
	def eval(self, vlist):
		lhs = self.args[0].eval(vlist[:self.args[0].vars])
		rhs = self.args[1].eval(vlist[self.args[0].vars:])
		if lhs is not None and rhs is not None:
			return self.fun(lhs, rhs)
		else:
			return None

class Plus(Expr2):
	def __init__(self, args):
		self.oper = '+'
		self.fun = lambda x,y: x+y
		Expr.__init__(self, args)

class Minus(Expr2):
	def __init__(self, args):
		self.oper = '-'
		self.fun = lambda x,y: x-y
		Expr.__init__(self, args)

class Mul(Expr2):
	def __init__(self, args):
		self.oper = '*'
		self.fun = lambda x,y: x*y
		Expr.__init__(self, args)

class Div(Expr2):
	@staticmethod
	def div(x, y):
		try:
			return (1.0*x)/(1.0*y)
		except:
			return None

	def __init__(self, args):
		self.oper = '/'
		self.fun = self.div
		Expr.__init__(self, args)

class Factorial(Expr1Postfix):
	@staticmethod
	def factorial(x):
		if x<0 or x>10: return None
		try:
			return math.factorial(x)
		except:
			return None

	def __init__(self, args):
		self.oper = '!'
		self.fun = self.factorial
		Expr.__init__(self, args)

class Sqrt(Expr1Prefix):
	@staticmethod
	def sqrt(x):
		if x<0: return None
		try:
			return math.sqrt(x)
		except:
			return None
			
	def __init__(self, args):
		self.oper = 'sqrt'
		self.fun = self.sqrt
		Expr.__init__(self, args)

class MinusUnary(Expr1Prefix):
	def __init__(self, args):
		self.oper = '-'
		self.fun = lambda x: -x
		Expr.__init__(self, args)


def generate(nops, varnum, unary, binary):
	ex = { (0,v): [Variable(v)] for v in range(1, varnum+1) } 

	for d in range(1, nops+1):
		for v in range(1, varnum+1):
			ex[(d,v)] = [ ex1([e]) for e in ex[(d-1,v)] 
		    	                   for ex1 in unary ] + \
		    	        [ ex2([e1,e2]) for ex2 in binary
		    	        			   for d2 in range(0,d)
		    	        			   for v1 in range(1,v)
		    	        			   for e1 in ex[(d-1-d2,v1)]
		    	        			   for e2 in ex[(d2,v-v1)] ]

	return ex

def solve(inputs, target, nops, threads, unary, binary):
	ex = generate(nops,len(inputs),unary,binary)
	print sum(len(ex[ew]) for ew in ex)

	for i in range(nops+1):
		for p in itertools.permutations(inputs):
			print i, p
			for e in ex[(i,len(inputs))]:
				val = e.eval(p)
				if val and math.fabs(val-target)<1e-6:
					print e.printf(p)

#solve([1,5,4], 27, 2, 0, [Sqrt, Factorial], [Minus, Plus, Mul, Div] ) 
#solve([0,4,5,6], 43, 4, 0, [Sqrt, Factorial], [Minus, Plus, Mul, Div] ) #923
#ex = solve([1,1,3,6], 44, 4, 0, [Sqrt, Factorial], [Minus, Plus, Mul, Div] ) #924
solve([0,2,3,7], 139, 6, 0, [Sqrt, Factorial], [Minus, Plus, Mul, Div] ) #925
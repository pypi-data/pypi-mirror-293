"""
This is a small utility/helper module containing one function to traverse 
and print lists that may or may not be nested lists.
"""
def print_lol(anyList, indent=False, level=0):
	"""
	Iterate through each item in the list and check if the retrieved 
	item is a list. If the item is a list, then recursively call the same
	function again, else print the item
	"""
	for listItem in anyList:
			if isinstance(listItem,list):
				print_lol(listItem, indent, level+1)
			else:
				if indent:
					for i in range(level):
						print("\t",end="")
				print(listItem)

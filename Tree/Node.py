from .NodeMix import NodeMixin


def _repr(node, args=None, nameblacklist=None):
	classname = node.__class__.__name__
	args = args or []
	nameblacklist = nameblacklist or []
	for key, value in filter(lambda item: not item[0].startswith("_") and item[0] not in nameblacklist, sorted(node.__dict__.items(), key=lambda item: item[0])):
		args.append("%s=%r" % (key, value))
	return "%s(%s)" % (classname, ", ".join(args))


class Node(NodeMixin):
	def __init__(self, name, parent=None, children=None, **kwargs):
		self.__dict__.update(kwargs)
		self.name = name
		self.parent = parent
		#self.children = children
		if children:
			self.children = children
		#super(Node, self).__init__(**kwargs)
		#print(self.name, self.parent, self.children)

	def __repr__(self):
		args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
		return _repr(self, args=args, nameblacklist=["name"])

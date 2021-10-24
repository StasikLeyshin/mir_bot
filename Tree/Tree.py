

from command_ls import command_ls_dictionary, command_ls_list
from .Node import Node


class Tree(dict):
	def __init__(self, *args, **kwargs):
		self.parent = kwargs.get("parent")
		flag = False
		if self.parent:
			flag = True
			pa = self.parent
			print(pa)
		#else:
		super(Tree, self).__init__(*args, **kwargs)
		#self.parent = kwargs.get("parent")
		print(1, self.parent)
		print(2, self.__dict__, self, self.parent)
		if flag:
			del self["parent"]
			name = self["name"]
			del self["name"]
			pa[name] = self
			print(pa)
			#print(self.parent)
			self.__dict__ = pa
		else:
			self.__dict__ = self
		#print(2, self.__dict__, self, self.parent)
		#self.parent = self
		#if flag:
			#self.__dict__ = self.__dict__
			#self.parent = 1
		#self.__dict__ = self
		print(3, self.__dict__)


# class Node:
#
# 	def __init__(self, name, parent=None, children=None, **kwargs):
#
# 		self.name = name
# 		self.parent = parent
# 		self.children = children
# 		if children:
# 			self.children = children
# 		#super(Node, self).__init__(**kwargs)
# 		print(self.name, self.parent)




# class NodeMix:
# 	separator = "/"
#
# 	@property
# 	def parent(self):
# 		try:
# 			return self.__parent
# 		except AttributeError:
# 			return None
#
# 	@parent.setter
# 	def parent(self, value):
# 		if value is not None and not isinstance(value, NodeMix):
# 			msg = "Parent node %r is not of type 'NodeMixin'." % (value,)
# 			#raise TreeError(msg)
# 		try:
# 			parent = self.__parent
# 		except AttributeError:
# 			parent = None
# 		if parent is not value:
# 			self.__check_loop(value)
# 			self.__detach(parent)
# 			self.__attach(value)
#
# 	def __check_loop(self, node):
# 		if node is not None:
# 			if node is self:
# 				msg = "Cannot set parent. %r cannot be parent of itself."
# 				#raise LoopError(msg % (self,))
# 			#if any(child is self for child in node.iter_path_reverse()):
# 				msg = "Cannot set parent. %r is parent of %r."
# 				#raise LoopError(msg % (self, node))
#
# 	def __detach(self, parent):
# 		if parent is not None:
# 			self._pre_detach(parent)
# 			parentchildren = parent.__children_or_empty
# 			assert any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
# 			# ATOMIC START
# 			parent.__children = [child for child in parentchildren if child is not self]
# 			self.__parent = None
# 			# ATOMIC END
# 			self._post_detach(parent)
#
# 	def __attach(self, parent):
# 		if parent is not None:
# 			self._pre_attach(parent)
# 			parentchildren = parent.__children_or_empty
# 			assert not any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
# 			# ATOMIC START
# 			parentchildren.append(self)
# 			self.__parent = parent
# 			# ATOMIC END
# 			self._post_attach(parent)
#
# 	@property
# 	def __children_or_empty(self):
# 		try:
# 			return self.__children
# 		except AttributeError:
# 			self.__children = []
# 			return self.__children
#
# 	@property
# 	def children(self):
# 		return tuple(self.__children_or_empty)
#
# 	def _pre_detach(self, parent):
# 		"""Method call before detaching from `parent`."""
# 		pass
#
# 	def _post_detach(self, parent):
# 		"""Method call after detaching from `parent`."""
# 		pass
#
# 	def _pre_attach(self, parent):
# 		"""Method call before attaching to `parent`."""
# 		pass
#
# 	def _post_attach(self, parent):
# 		"""Method call after attaching to `parent`."""
# 		pass

# def _repr(node, args=None, nameblacklist=None):
# 	classname = node.__class__.__name__
# 	args = args or []
# 	nameblacklist = nameblacklist or []
# 	for key, value in filter(lambda item: not item[0].startswith("_") and item[0] not in nameblacklist, sorted(node.__dict__.items(), key=lambda item: item[0])):
# 		args.append("%s=%r" % (key, value))
# 	return "%s(%s)" % (classname, ", ".join(args))


# class Node(NodeMixin):
#
# 	def __init__(self, name, parent=None, children=None, **kwargs):
# 		self.__dict__.update(kwargs)
# 		self.name = name
# 		self.parent = parent
# 		#self.children = children
# 		if children:
# 			self.children = children
# 		#super(Node, self).__init__(**kwargs)
# 		#print(self.name, self.parent, self.children)
#
# 	def __repr__(self):
# 		args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
# 		return _repr(self, args=args, nameblacklist=["name"])

# class Te:
# 	def __init__(self, test):
# 		self.test = test


def tree_distribution_root():
	root = Node('help', process=command_ls_dictionary['help'])
	command_ls_dictionary['help'].append(root)


	question = Node('question', parent=root, process=command_ls_dictionary['question'])
	command_ls_dictionary['question'].append(question)

	want_university = Node('want_university', parent=question, process=command_ls_dictionary['want_university'])
	command_ls_dictionary['want_university'].append(want_university)

	bachelors_specialty = Node('bachelors_specialty', parent=want_university,
							   process=command_ls_dictionary['bachelors_specialty'])
	command_ls_dictionary['bachelors_specialty'].append(bachelors_specialty)

	magistracy = Node('magistracy', parent=want_university, process=command_ls_dictionary['magistracy'])
	command_ls_dictionary['magistracy'].append(magistracy)

	want_college = Node('want_college', parent=question, process=command_ls_dictionary['want_college'])
	command_ls_dictionary['want_college'].append(want_college)

	studying_university_college = Node('studying_university_college', parent=question,
									   process=command_ls_dictionary['studying_university_college'])
	command_ls_dictionary['studying_university_college'].append(studying_university_college)


	choose_direction = Node('choose_direction', parent=root, process=command_ls_dictionary['choose_direction'])
	command_ls_dictionary['choose_direction'].append(choose_direction)

	select_exam = Node('select_exam', parent=choose_direction, process=command_ls_dictionary['select_exam'])
	command_ls_dictionary['select_exam'].append(select_exam)

	select_interests = Node('select_interests', parent=choose_direction, process=command_ls_dictionary['select_interests'])
	command_ls_dictionary['select_interests'].append(select_interests)

	interest = Node('interest', parent=select_interests, process=command_ls_dictionary['interest'])
	command_ls_dictionary['interest'].append(interest)

	scores = Node('scores', parent=select_exam, process=command_ls_dictionary['scores'])
	command_ls_dictionary['scores'].append(scores)


	choose_event = Node('choose_event', parent=root, process=command_ls_dictionary['choose_event'])
	command_ls_dictionary['choose_event'].append(choose_event)

	select_interest_event = Node('select_interest_event', parent=choose_event, process=command_ls_dictionary['select_interest_event'])
	command_ls_dictionary['select_interest_event'].append(select_interest_event)

	interest_event = Node('interest_event', parent=select_interest_event, process=command_ls_dictionary['interest_event'])
	command_ls_dictionary['interest_event'].append(interest_event)

	offline_event = Node('offline_event', parent=choose_event, process=command_ls_dictionary['offline_event'])
	command_ls_dictionary['offline_event'].append(offline_event)

	online_event = Node('online_event', parent=choose_event, process=command_ls_dictionary['online_event'])
	command_ls_dictionary['online_event'].append(online_event)

	type_event = Node('type_event', parent=choose_event, process=command_ls_dictionary['type_event'])
	command_ls_dictionary['type_event'].append(type_event)

	format_type_event = Node('format_type_event', parent=type_event, process=command_ls_dictionary['format_type_event'])
	command_ls_dictionary['format_type_event'].append(format_type_event)


	open_day = Node('open_day', parent=root, process=command_ls_dictionary['open_day'])
	command_ls_dictionary['open_day'].append(open_day)


	# answer = Node('answer', process=command_ls_dictionary['answer'])
	# command_ls_dictionary['answer'].append(answer)


	# right = Node("B", parent=left, red="bar")
	#
	# rig = Node("C", parent=root, test=Te)
	return root



# def Tree_distribution():
#
# 	root = Node("root")
#
# 	return root



# if __name__ == "__main__":
#
#
#
# 	root = Node("root")
#
# 	left = Node("A", parent=root, bar="res")
#
# 	right = Node("B", parent=left, red="bar")
#
# 	rig = Node("C", parent=root, test=Te)
#
# 	print(root.children)

	#t = Tree(left=Tree(test="test", left="a", right="b"), right=Tree(left="c"))

	#root = Tree(name="root", red="red")

	#left = Tree(name="test", bar="ger", parent=root)

	#right = Tree(name="test1", bar="ger", parent=left)

	# udo = Tree("Udo")
	# marc = Tree("Marc", parent=udo)
	# lian = Tree("Lian", parent=marc)
	# dan = Tree("Dan", parent=udo)
	# jet = Tree("Jet", parent=dan)
	# jan = Tree("Jan", parent=dan)
	# joe = Tree("Joe", parent=dan)



	#print(t.left, t.right)

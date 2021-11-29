# -*- coding: utf-8 -*-

import warnings

#from anytree.iterators import PreOrderIter
from .preorderiter import PreOrderIter

#from .exceptions import LoopError
#from .exceptions import TreeError


class NodeMixin(object):

    separator = "/"

    @property
    def parent(self):

        try:
            return self.__parent
        except AttributeError:
            return None

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, NodeMixin):
            msg = "Parent node %r is not of type 'NodeMixin'." % (value, )
            raise Exception(msg)
        try:
            parent = self.__parent
        except AttributeError:
            parent = None
        if parent is not value:
            self.__check_loop(value)
            self.__detach(parent)
            self.__attach(value)

    def __check_loop(self, node):
        if node is not None:
            if node is self:
                msg = "Cannot set parent. %r cannot be parent of itself."
                raise Exception(msg % (self, ))
            if any(child is self for child in node.iter_path_reverse()):
                msg = "Cannot set parent. %r is parent of %r."
                raise Exception(msg % (self, node))

    def __detach(self, parent):
        if parent is not None:
            self._pre_detach(parent)
            parentchildren = parent.__children_or_empty
            assert any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parent.__children = [child for child in parentchildren if child is not self]
            self.__parent = None
            # ATOMIC END
            self._post_detach(parent)

    def __attach(self, parent):
        if parent is not None:
            self._pre_attach(parent)
            parentchildren = parent.__children_or_empty
            assert not any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parentchildren.append(self)
            self.__parent = parent
            # ATOMIC END
            self._post_attach(parent)

    @property
    def __children_or_empty(self):
        try:
            return self.__children
        except AttributeError:
            self.__children = []
            return self.__children

    @property
    def children(self):

        return tuple(self.__children_or_empty)

    @staticmethod
    def __check_children(children):
        seen = set()
        for child in children:
            if not isinstance(child, NodeMixin):
                msg = "Cannot add non-node object %r. It is not a subclass of 'NodeMixin'." % (child, )
                raise Exception(msg)
            childid = id(child)
            if childid not in seen:
                seen.add(childid)
            else:
                msg = "Cannot add node %r multiple times as child." % (child, )
                raise Exception(msg)

    @children.setter
    def children(self, children):
        # convert iterable to tuple
        children = tuple(children)
        NodeMixin.__check_children(children)
        # ATOMIC start
        old_children = self.children
        del self.children
        try:
            self._pre_attach_children(children)
            for child in children:
                child.parent = self
            self._post_attach_children(children)
            assert len(self.children) == len(children)
        except Exception:
            self.children = old_children
            raise
        # ATOMIC end

    @children.deleter
    def children(self):
        children = self.children
        self._pre_detach_children(children)
        for child in self.children:
            child.parent = None
        assert len(self.children) == 0
        self._post_detach_children(children)

    def _pre_detach_children(self, children):
        """Method call before detaching `children`."""
        pass

    def _post_detach_children(self, children):
        """Method call after detaching `children`."""
        pass

    def _pre_attach_children(self, children):
        """Method call before attaching `children`."""
        pass

    def _post_attach_children(self, children):
        """Method call after attaching `children`."""
        pass

    @property
    def path(self):

        return self._path

    def iter_path_reverse(self):

        node = self
        while node is not None:
            yield node
            node = node.parent

    @property
    def _path(self):
        return tuple(reversed(list(self.iter_path_reverse())))

    @property
    def ancestors(self):

        if self.parent is None:
            return tuple()
        return self.parent.path

    @property
    def anchestors(self):
        """
        All parent nodes and their parent nodes - see :any:`ancestors`.
        The attribute `anchestors` is just a typo of `ancestors`. Please use `ancestors`.
        This attribute will be removed in the 3.0.0 release.
        """
        warnings.warn(".anchestors was a typo and will be removed in version 3.0.0", DeprecationWarning)
        return self.ancestors

    @property
    def descendants(self):

        return tuple(PreOrderIter(self))[1:]

    @property
    def root(self):

        node = self
        while node.parent is not None:
            node = node.parent
        return node

    @property
    def siblings(self):

        parent = self.parent
        if parent is None:
            return tuple()
        else:
            return tuple(node for node in parent.children if node is not self)

    @property
    def leaves(self):

        return tuple(PreOrderIter(self, filter_=lambda node: node.is_leaf))

    @property
    def is_leaf(self):

        return len(self.__children_or_empty) == 0

    @property
    def is_root(self):

        return self.parent is None

    @property
    def height(self):

        children = self.__children_or_empty
        if children:
            return max(child.height for child in children) + 1
        else:
            return 0

    @property
    def depth(self):

        # count without storing the entire path
        for i, _ in enumerate(self.iter_path_reverse()):
            continue
        return i

    def _pre_detach(self, parent):
        """Method call before detaching from `parent`."""
        pass

    def _post_detach(self, parent):
        """Method call after detaching from `parent`."""
        pass

    def _pre_attach(self, parent):
        """Method call before attaching to `parent`."""
        pass

    def _post_attach(self, parent):
        """Method call after attaching to `parent`."""
        pass
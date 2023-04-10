# An implementation of ADT Map that uses a binary search tree as the
# underlying data structure.

__author__ = 'Erik Caldwell'


class BSTMap:

    class _Node:
        def __init__(self, key: any, value: any, left: '_Node' = None, right: '_Node' = None) -> None:
            """
            Initialize a node containing a key, the value associated with
            the key, and links to the node's left and right children.
            """
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __iter__(self):
            """
            Return an iterator that performs an inorder traversal of the
            tree rooted at this node, returning the keys.
            """
            if self.left is not None:
                for elem in self.left:
                    yield elem

            yield self.key

            if self.right is not None:
                for elem in self.right:
                    yield elem

    def __init__(self, iterable=[]) -> None:
        """
        Initialize this BSTMap.

        If no iterable is provided, the map is empty.
        Otherwise, initialize the map by inserting the key/value pairs
        provided by the iterable.

        Precondition: the iterable is a sequence of tuples, with each tuple
        containing one (key, value) pair.

        >>> map = BSTMap()
        >>> map
        {}

        # In this example each key/value pair is a tuple containing a
        # 6-digit student number (an int) and that student's letter grade
        # (a str).

        >>> grades = BSTMap([(111537, 'A+'), (101156, 'A+'), (127118, 'B')])
        >>> grades
        {101156: 'A+', 111537: 'A+', 127118: 'B', }
        """
        self._root = None

        # Number of entries in the map; i.e., the number of key/value pairs.
        self._num_entries = 0

        for key, value in iterable:
            self[key] = value  # updates self._num_entries

    def __str__(self) -> str:
        """
        Return a string representation of this BSTMap (inorder traversal of
        the nodes), using the format: "{key_1: value_1, key_2: value_2, ...}"

        >>> grades = BSTMap([(111537, 'A+'), (101156, 'A+'), (127118, 'B')])
        >>> str(grades)
        "{101156: 'A+', 111537: 'A+', 127118: 'B'}"
        """
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "{{{0}}}".format(", ".join([repr(key) + ': ' + repr(self[key]) for key in self]))

    __repr__ = __str__

    def __iter__(self):
        """
        Return an iterator that performs an inorder traversal of the nodes
        in this BSTMap, returning the keys.
        """
        if self._root is not None:
            return self._root.__iter__()
        else:
            # The tree is empty, so use an empty list's iterator
            # as the tree's iterator.
            return iter([])

    def __setitem__(self, key: any, newvalue: any):
        """ 
        Create the key or overwrite the preexisting key with the new value.
        """
        def _set_item(node: 'BSTMap._Node', key: any, newvalue: any) -> 'BSTMap._Node':
            """
            Insert x into the Map at the given key rooted at node and
            return the reference to tree's root node.
            """
            if node is None:
                # The tree is empty, so create the root node of a new tree.
                self._num_entries += 1
                return BSTMap._Node(key, newvalue)

            if node.key == key:
                # Found the key, set the value
                node.value = newvalue
                return node

            if key < node.key:
                # Insert x in node's left subtree.
                node.left = _set_item(node.left, key, newvalue)
            else:
                # Insert x in node's right subtree.
                node.right = _set_item(node.right, key, newvalue)

            return node

        self._root = _set_item(self._root, key, newvalue)

    def __getitem__(self, key: any) -> any:
        """ 
        Return the value at the given key.
        Raises a KeyError if the key does not exist.
        """
        def _get_item(node: 'BSTMap._Node', key: any) -> any:
            """ 
            Return the value at the given key rooted to a map at the give node.
            """
            if node is None:
                # Key not in tree, raise KeyError
                raise KeyError(f'{key}')

            if node.key == key:
                # Found the key, return the value
                return node.value

            if key < node.key:
                # Look through the node's left subtree.
                return _get_item(node.left, key)
            else:
                # Look through the node's right subtree.
                return _get_item(node.right, key)

        return _get_item(self._root, key)

    def get(self, key: any, default_value=None) -> any:
        """ 
        Get the value at the given key. 
        Returns the default value if the key doesn't exist.
        """
        def _get(node: 'BSTMap._Node', key: any) -> any:
            """ 
            Get the value at the given key rooted at the given node.
            Returns a default value if the key doesn't exist.
            """
            if node is None:
                # Key not in tree, raise KeyError
                return default_value

            if node.key == key:
                # Found the key, return the value
                return node.value

            if key < node.key:
                # Look through the node's left subtree.
                return _get(node.left, key)
            else:
                # Look through the node's right subtree.
                return _get(node.right, key)

        return _get(self._root, key)

    def __len__(self):
        """ 
        Get the number of key/value pairs in the Map.
        """
        return self._num_entries

    def __contains__(self, key: any) -> bool:
        """ 
        Returns True if the given key is in the Map.
        """
        def _contains(node: 'BSTMap._Node', key: any) -> bool:
            """ 
            Search for the given key in the Map rooted at the given node.
            """
            if node is None:
                # Got to a leaf without finding the key
                return False

            if node.key == key:
                # Found the key
                return True

            if key < node.key:
                # Look through the node's left subtree.
                return _contains(node.left, key)
            else:
                # Look through the node's right subtree.
                return _contains(node.right, key)

        return _contains(self._root, key)

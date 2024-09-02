class NestedDictionary:
    def __init__(self, initial_data=None, separator='/'):
        self._data = initial_data or {}
        self._current_path = ''
        self._separator = separator

    def __getattr__(self, item):
        # Build the new path by appending the current item
        new_path = self._current_path + self._separator + item if self._current_path else item

        # If the constructed path is in the dictionary, return the value
        if new_path in self._data:
            return self._data[new_path]

        # If the path is not found, return a new instance with the updated path
        return NestedDictionary(self._data, separator=self._separator)._update_path(new_path)

    def _update_path(self, new_path):
        # Update the current path with the new path and return the instance
        self._current_path = new_path
        return self

    def __setitem__(self, key, value):
        # Set the value for the specified key in the dictionary
        self._data[key] = value

    def __getitem__(self, key):
        # Retrieve the value for the specified key from the dictionary
        return self._data[key]

    def __repr__(self):
        return f"NestedDictionary({self._data})"

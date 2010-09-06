class CSSable(object):
    """A abstract class for converting a less object to css."""

    def __init__(self):
        """Initialize a `CSSable`:class object. All of less object must
        implement this method. 

        """
        raise NotImplementedError("You must implement initializer")
    

    def to_css(self):
        """Performs converting a object to printable string."""
        raise NotImplementedError("You must implement to_css method")


class String(CSSable):
    """Just a string object."""

    def __init__(self, string):
        self.val = string

    def to_css(self):
        return '"' + self.val + '"'

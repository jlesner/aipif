
class Segment: # pylint: disable=too-few-public-methods
    """A segment of a story.

    A segment is a piece of a story, like a chapter or a scene. It has a
    title, a body, and a list of tags. The title and body are both strings.
    The tags are a list of strings.

    Attributes:
        title (str): The title of the segment.
        body (str): The body of the segment.
        tags (list): The tags of the segment.
    """

    def __init__(self, title, body, tags, parent=None):
        """Constructs a segment.

        Args:
            title (str): The title of the segment.
            body (str): The body of the segment.
            tags (list): The tags of the segment.
        """
        self.parent = parent
        self.title = title
        self.body = body
        self.tags = tags

    def __str__(self):
        """Returns a string representation of the segment.

        Returns:
            str: A string representation of the segment.
        """
        return self.title + '\n' + self.body + '\n' + str(self.tags) + '\n'

    def __repr__(self):
        """Returns a string representation of the segment.

        Returns:
            str: A string representation of the segment.
        """
        return self.title + '\n' + self.body + '\n' + str(self.tags) + '\n'

    def __eq__(self, other):
        """Checks if two segments are equal.

        Args:
            other (Segment): The other segment to compare to.

        Returns:
            bool: True if the segments are equal, False otherwise.
        """
        return (self.title == other.title and self.body == other.body and
                self.tags == other.tags)

    def __ne__(self, other):
        """Checks if two segments are not equal.

        Args:
            other (Segment): The other segment to compare to.

        Returns:
            bool: True if the segments are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """Returns a hash of the segment.

        Returns:
            int: A hash of the segment.
        """
        return hash((self.title, self.body, tuple(self.tags)))

    def to_dict(self):
        """Returns a dictionary representation of the segment.
        
        Returns:
            dict: A dictionary 
        """
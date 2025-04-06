class CollectionExistsException(Exception):
    """Exception raised when attempting to create a vector store collection that already exists.

    Attributes:
        collection_name: Name of the existing collection.
        message: Explanation of the error.
    """

    def __init__(self, collection_name: str) -> None:
        """Initialize the exception.

        Args:
            collection_name: Name of the collection that already exists.
        """
        self.collection_name = collection_name
        self.message = f"Collection with name {collection_name} already exists"
        super().__init__(self.message)

class CollectionExistsException(Exception):
    """Exception raised when attempting to create a vector store collection that already exists.

    This exception helps prevent accidental overwriting of existing collections
    and provides clear error messaging about the conflicting collection name.
    """

    def __init__(self, collection_name: str) -> None:
        """Initialize the CollectionExistsException with the conflicting collection name.

        Args:
            collection_name: Name of the collection that already exists in the vector store.
                            This name caused the creation attempt to fail.
        """
        self.collection_name = collection_name
        self.message = f"Collection with name {collection_name} already exists"
        super().__init__(self.message)

from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Category():
    title: str
    parent: Category
    children: list = field(default_factory=lambda: [])
    
    data: list = field(init=False) #This gets filled with [None] during folderInitialization, then filled with useful data when the category is reached
    """1 = Found in photo,
    \n 0 = Not found in photo,
    \n None = Not answered yet,
    \n 'skip' = Parent category not found in photo"""


    def initializeData(self):
        """initializes the category based on the data of the parent category."""
        if self.parent == None:
            return
        if None in self.parent.data:
            raise ValueError(self.parent.data, 'parent\'s data is not filled.')
        
        self.data = [None if x == 1 else 'skip' for x in self.parent.data]

    def getPhotoCounter(self, photoIndex) -> str:
        """Returns the string for the Photo Counter in the UI, ignoring skips."""
        return (
            str(self._countPhotosSorted(photoIndex) + 1)
            + '/' + 
            str(self.countPhotos())
        )

    def countPhotos(self):
        """Ignores pictures that will be skipped."""
        return len(self.data) - self.data.count('skip')

    def _countPhotosSorted(self, photoIndex):
        """Ignores pictures that were skipped. Counts how many pictures the user has sorted for this category."""
        slicedData = self.data[0:photoIndex]
        return len(slicedData) - slicedData.count('skip')
    
    def countAncestors(self) -> int:
        if self.parent == None:
            return 0
        else:
            return 1 + self.parent.countAncestors()

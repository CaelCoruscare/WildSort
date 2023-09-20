from DataHandling.Category import Category

class FlipValue():
    """
    Flips the value of a category for the current photo.

    \nHandles adjusting other values upstream and downstream.
    """
    def __init__(self, targetCategory: Category, photoIndex):
        self._photoIndex = photoIndex
        value = targetCategory.data[photoIndex]
        self.DoIt(value, targetCategory)

    def DoIt(self, value, category: Category):
        if value == 1:
            #Parents: No changes

            #Target:
            category.data[self._photoIndex] = 0

            #Children:
            for child in category.children:
                self.setChildAndGrandchildren_ToSkip(child)
            
        elif value == 0: #(if 0 or 'skip' or None)
            #Parents: no changes

            #Target:
            category.data[self._photoIndex] = 1

            #Children:
            for child in category.children:
                self.setChildAndGrandchildren_ToSkip(child)

        elif value == 'skip':
            #Parents:
            self.setParentAndGrandparents_ToOne(category.parent)

            #Target
            category.data[self._photoIndex] = 1

            #Children:
            for child in category.children:
                self.set_ToZero(child)

        elif value == None:
            raise ValueError(value, "UI should prevent flipping a None value.")

    def setParentAndGrandparents_ToOne(self, parent: Category):
        if parent == None:
            return
        parent.data[self._photoIndex] = 1
        self.setParentAndGrandparents_ToOne(parent=parent.parent)

    def set_ToZero(self, category: Category):
        if category.data[self._photoIndex] == None:
            return
        category.data[self._photoIndex] = 0
        
        #Below a 0 is always 'skips' until the Nones start
        for child in category.children:
            self.setChildAndGrandchildren_ToSkip(child=child)

    def setChildAndGrandchildren_ToSkip(self, child: Category):
        if child.data[self._photoIndex] == None:
            return
        child.data[self._photoIndex] = 'skip'
        for grandchild in child.children:
            self.setChildAndGrandchildren_ToSkip(child=grandchild)

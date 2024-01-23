import copy
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtGui import QMouseEvent, QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF

class Block:
    def __init__(self, name, width, height) -> None:
        self.name = name
        self.width = width
        self.height = height
        self.position = (0,0)
        self.rect = None

class Board:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.blocks = []
        self.selected_block = None

    def add_block(self, block:Block, x, y) -> bool:
        """add a block to this board"""
        #check if the block can be in thes board
        if ((self.width < block.width + x) or self.height < block.height + y):
            raise ValueError(f"Block {block.name} doesn't fit this board!")
        #check if there are any colitions
        block.position = (x, y)
        for current_block in self.blocks:
            if not(current_block.position[0] >= block.position[0] + block.width or 
                   current_block.position[0] + current_block.width <= block.position[0] or 
                   current_block.position[1] >= block.position[1] + block.height or 
                   current_block.position[1] + current_block.height <= block.position[1]):
                raise ValueError(f"Block {current_block.name} collides with block {block.name}!")
        #add the block to this board     
        self.blocks.append(block)

    def select_block_index(self, x, y):
        """select a block according to the coordination"""
        selected_block = None
        for i, block in enumerate(self.blocks):
            if (block.position[0] <= x and
                block.position[0] + block.width > x and
                block.position[1] <= y and
                block.position[1] + block.height > y):
                selected_block = i
                break
        return selected_block
    
    def select_block(self, index):
        # Deselect the currently selected block, if any
        for block in self.blocks:
            block.rect.setPen(QPen(Qt.NoPen))
        if self.selected_block is not None:
            self.blocks[self.selected_block].rect.setPen(QPen(Qt.NoPen))

        # Select the new block
        self.selected_block = index
        
        if index is not None:
            print(f"selected block {board.blocks[index].name}")
            self.blocks[index].rect.setPen(QPen(Qt.black, 2))

    def move_block(self, x, y):
        if self.selected_block is not None:
            # Calculate the new position of the block
            self.blocks[self.selected_block]
            new_x = min(max(0, x - self.blocks[self.selected_block].width // 2), self.width - self.blocks[self.selected_block].width)
            new_y = min(max(0, y - self.blocks[self.selected_block].height // 2), self.height - self.blocks[self.selected_block].height)

            # Initialize the minimum distance to a large number
            min_distance = float('inf')
            nearest_block = None

            # Traverse all possible destination blocks
            for i in range(self.width - self.blocks[self.selected_block].width + 1):
                for j in range(self.height - self.blocks[self.selected_block].height + 1):
                    # Create a copy of the selected block and move it to the new position
                    new_block = Block(self.blocks[self.selected_block].name, self.blocks[self.selected_block].width, self.blocks[self.selected_block].height)
                    new_block.position = (i, j)

                    # Check if the new block contains the point (x, y)
                    if i <= x < i + new_block.width and j <= y < j + new_block.height:
                        # Check if the new block does not collide with any other block
                        collision = False
                        for current_block in self.blocks:
                            if current_block == self.blocks[self.selected_block]:
                                continue
                            if not(current_block.position[0] >= i + self.blocks[self.selected_block].width or 
                                    current_block.position[0] + current_block.width <= i or 
                                    current_block.position[1] >= j + self.blocks[self.selected_block].height or 
                                    current_block.position[1] + current_block.height <= j):
                                print(f"Block {current_block.name} collides with block {self.blocks[self.selected_block].name}!")
                                collision = True
                                break

                        if not collision:
                            # Calculate the distance from the center of the new block to the center of the original block
                            distance = ((i + new_block.width / 2 - self.blocks[self.selected_block].position[0] - self.blocks[self.selected_block].width / 2) ** 2 +
                                        (j + new_block.height / 2 - self.blocks[self.selected_block].position[1] - self.blocks[self.selected_block].height / 2) ** 2) ** 0.5
                            # Update the nearest block
                            if distance < min_distance:
                                min_distance = distance
                                nearest_block = new_block

            # Move the selected block to the new position
            if nearest_block is not None:
                self.blocks[self.selected_block].position = nearest_block.position
                print(f"Moved block {self.blocks[self.selected_block].name} to {nearest_block.position}!")
                self.selected_block = None
            else:
                print("No valid position found!")
            

    # def move_block(self, x, y):
    #     if self.selected_block is not None:
    #         # Calculate the new position of the block
    #         self.blocks[self.selected_block]
    #         new_x = min(max(0, x - self.blocks[self.selected_block].width // 2), self.width - self.blocks[self.selected_block].width)
    #         new_y = min(max(0, y - self.blocks[self.selected_block].height // 2), self.height - self.blocks[self.selected_block].height)

    #         # Check if the new position is not occupied by other blocks
    #         for i, current_block in enumerate(self.blocks):
    #             if i == self.selected_block:
    #                 continue
    #             if not(current_block.position[0] >= new_x + self.blocks[self.selected_block].width or 
    #                 current_block.position[0] + current_block.width <= new_x or 
    #                 current_block.position[1] >= new_y + self.blocks[self.selected_block].height or 
    #                 current_block.position[1] + current_block.height <= new_y):
    #                 print(f"Block {current_block.name} collides with block {self.blocks[self.selected_block].name}!")
    #                 return

    #         # Move the selected block to the new position
    #         self.blocks[self.selected_block].position = (new_x, new_y)
    #         print(f"Moved block {self.blocks[self.selected_block].name} to {(new_x, new_y)}!")
    #         self.selected_block = None
   
class GameWindow(QMainWindow):
    def __init__(self, board:Board):
        super().__init__()
        self.board = board
        self.initUI()

    def initUI(self):
        cell_size = 100  # Change the size of each grid cell
        self.setGeometry(500, 500, self.board.width * cell_size + 20, self.board.height * cell_size + 20)
        self.setWindowTitle('卑女华容道')

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, self.board.width * cell_size + 20, self.board.height * cell_size + 20)

        # Draw the grid
        for i in range(self.board.width):
            for j in range(self.board.height):
                rect = self.scene.addRect(i*cell_size, j*cell_size, cell_size, cell_size)
                rect.setPen(QPen(Qt.black))

        # Draw the blocks
        for block in self.board.blocks:
            x, y = block.position
            filename = block.name + ".jpg"
            pixmap = QPixmap(filename)  # Load the image
            pixmap = pixmap.scaled(block.width*cell_size, block.height*cell_size, Qt.KeepAspectRatio)  # Resize the image
            pixmap_item = QGraphicsPixmapItem(pixmap)  # Create a pixmap item
            pixmap_item.setPos(x*cell_size, y*cell_size)  # Set the position
            self.scene.addItem(pixmap_item)  # Add the pixmap item to the scene
            rect = self.scene.addRect(x*cell_size, y*cell_size, block.width*cell_size, block.height*cell_size)
            block.rect = rect
        self.show()

    def updateUI(self):
        cell_size = 100  # Change the size of each grid cell
        self.scene.clear()
        # Draw the grid
        for i in range(self.board.width):
            for j in range(self.board.height):
                rect = self.scene.addRect(i*cell_size, j*cell_size, cell_size, cell_size)
                rect.setPen(QPen(Qt.black))
        # Draw the blocks
        for block in self.board.blocks:
            x, y = block.position
            filename = block.name + ".jpg"
            pixmap = QPixmap(filename)  # Load the image
            pixmap = pixmap.scaled(block.width*cell_size, block.height*cell_size, Qt.KeepAspectRatio)  # Resize the image
            pixmap_item = QGraphicsPixmapItem(pixmap)  # Create a pixmap item
            pixmap_item.setPos(x*cell_size, y*cell_size)  # Set the position
            self.scene.addItem(pixmap_item)  # Add the pixmap item to the scene
            rect = self.scene.addRect(x*cell_size, y*cell_size, block.width*cell_size, block.height*cell_size)
            block.rect = rect
        self.show()      

    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            board.select_block(None)
        if event.button() == Qt.MouseButton.LeftButton:
            window_x, window_y = event.x(), event.y()
            view_x, view_y = window_x-10, window_y-10
            board_x, board_y = view_x // 100, view_y // 100
            print(f"{board_x},{board_y}")
            selected_block_index = board.select_block_index(board_x, board_y)
            if board.selected_block is None:
                board.select_block(selected_block_index)
            else:
                if board.selected_block != selected_block_index:
                    board.move_block(board_x, board_y)
                    self.updateUI()


producer = Block("producer", 2, 2)
suzuki = Block("suzuki", 1, 2)
rinze = Block("rinze", 1, 2)
amana = Block("amana", 1, 2)
huyuko = Block("huyuko", 1, 2)
chiyoko = Block("chiyoko", 2, 1)
kaho = Block("kaho", 1, 1)
madoka = Block("madoka", 1, 1)
mano = Block("mano", 1, 1)
tenka = Block("tenka", 1, 1)


board = Board(4, 5)
board.add_block(suzuki, 0, 0)
board.add_block(producer, 1, 0)
board.add_block(rinze, 3, 0)
board.add_block(amana, 0, 2)
board.add_block(chiyoko, 1, 2)
board.add_block(huyuko, 3, 2)
board.add_block(kaho, 1, 3)
board.add_block(madoka, 2, 3)
board.add_block(mano, 0, 4)
board.add_block(tenka, 3, 4)



app = QApplication([])
window = GameWindow(board)
app.exec_()
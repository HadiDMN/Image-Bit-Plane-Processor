import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QFileDialog, QLabel, QMessageBox, QComboBox)
from PyQt5.QtGui import QPalette, QColor
from PIL import Image

# Image Processing Functions
def decompose_image_to_bit_planes(image):
    """Converts image to grayscale and decomposes into 8 bit planes."""
    image = image.convert('L')
    pixels = image.load()
    width, height = image.size
    planes = [Image.new('1', (width, height)) for _ in range(8)]
    plane_pixels = [plane.load() for plane in planes]
    for i in range(width):
        for j in range(height):
            pixel_value = pixels[i, j]
            for k in range(8):
                plane_pixels[k][i, j] = (pixel_value >> k) & 1
    return planes

def add_logo_to_layer(layer, logo_path, target_size, alpha=0.5):
    """Adds a resized logo to the specified bit plane with alpha blending."""
    logo = Image.open(logo_path)
    logo = logo.convert('L')
    logo = logo.resize(target_size)

    # Create a mask with alpha values for blending
    mask = Image.new('L', target_size)
    mask_pixels = mask.load()
    logo_pixels = logo.load()
    for i in range(target_size[0]):
        for j in range(target_size[1]):
            mask_pixels[i, j] = int(logo_pixels[i, j] * alpha)

    layer.paste(logo, (0, 0), mask=mask)
    return layer

def combine_planes_to_image(planes):
    """Combines bit planes back into a single grayscale image."""
    combined_image = Image.new('L', planes[0].size)
    combined_pixels = combined_image.load()
    for k in range(8):
        plane_pixels = planes[k].load()
        for i in range(combined_image.width):
            for j in range(combined_image.height):
                combined_pixels[i, j] |= (plane_pixels[i, j] << k)
    return combined_image

def open_image(image_path):
    """Opens the image using platform-specific commands."""
    if sys.platform == "win32":
        os.startfile(image_path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        os.system(f"{opener} '{image_path}'")

# GUI Application
class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.image = None
        self.logo_path = None
        self.planes = []
        
    def init_ui(self):
        # Set dark theme palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(142, 45, 197))
        dark_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(dark_palette)
        
        # Set Default Size
        self.resize(1280, 720)
        self.layout = QVBoxLayout()
        
        self.titleLabel = QLabel('8-Bit Layer Image Processor V:1.0     Developed by: Hadi DaMaN')
        self.layout.addWidget(self.titleLabel)
        self.planeComboBox = QComboBox()
        self.planeComboBox.addItems([' Plane 1', 'Plane 2', 'Plane 3', 'Plane 4', 'Plane 5', 'Plane 6', 'Plane 7', 'Plane 8'])
        
        # Apply dark palette to the combo box
        self.planeComboBox.setStyleSheet("QComboBox { background-color: rgb(25, 25, 25); color: rgb(255, 255, 255); }"
                                         "QComboBox::drop-down { background-color: rgb(25, 25, 25); color: rgb(255, 255, 255); }")  
        
        self.layout.addWidget(self.planeComboBox)
        self.selectImageButton = QPushButton('Select Image')
        self.selectImageButton.clicked.connect(self.select_image)
        self.layout.addWidget(self.selectImageButton)
        self.addLogoButton = QPushButton('Add Logo to Selected Layer')
        self.addLogoButton.clicked.connect(self.add_logo)
        self.layout.addWidget(self.addLogoButton)
        self.processButton = QPushButton('Process and Save Images')
        self.processButton.clicked.connect(self.process_images)
        self.layout.addWidget(self.processButton)
        
        # About me Button
        self.aboutMeButton = QPushButton('About Me')
        self.aboutMeButton.clicked.connect(self.show_about_me)
        self.layout.addWidget(self.aboutMeButton)

        self.setLayout(self.layout)
        self.setWindowTitle('Image Bit Plane Processor')
    def select_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image files (*.png *.jpg *.jpeg *.bmp)')
        if image_path:
            self.image = Image.open(image_path)
            QMessageBox.information(self, 'Image Loaded', 'Image has been loaded successfully.')

    def add_logo(self):
        if self.image is None:
            QMessageBox.warning(self, 'No Image', 'Please load an image first.')
            return
        self.logo_path, _ = QFileDialog.getOpenFileName(self, 'Select Logo', '', 'Image files (*.png *.jpg *.jpeg *.bmp)')
        if self.logo_path:
            QMessageBox.information(self, 'Logo Loaded', 'Logo has been loaded successfully.')
            
            # Resize the logo to match the size of the loaded image
            target_size = (self.image.width, self.image.height)
            if not self.planes:
                self.planes = decompose_image_to_bit_planes(self.image)

            # Get the selected plane index
            selected_plane_index = self.planeComboBox.currentIndex()

            # Clear the selected plane
            self.planes[selected_plane_index] = Image.new('1', (self.image.width, self.image.height))  
            
            # Add the logo to the selected plane
            self.planes[selected_plane_index] = add_logo_to_layer(self.planes[selected_plane_index], self.logo_path, target_size)

    def process_images(self):
        if self.image is None:
            QMessageBox.warning(self, 'No Image', 'Please load an image first.')
            return
        if not self.planes:
            QMessageBox.warning(self, 'No Processing', 'The image has not been processed yet.')
            return
        
        # Save all planes into one image
        combined_planes_image = Image.new('1', (self.image.width * 8, self.image.height))
        for i, plane in enumerate(self.planes):
            combined_planes_image.paste(plane, (i * self.image.width, 0))
        combined_planes_image_path = 'combined_planes.png'
        combined_planes_image.save(combined_planes_image_path)
        
        # Save all planes with logo into one image
        combined_logo_planes_image_path = 'combined_logo_planes.png'
        self.planes[0].save(combined_logo_planes_image_path)
        
        # Save the final composite image
        final_image = combine_planes_to_image(self.planes)
        final_image_path = 'final_image.png'
        final_image.save(final_image_path)
        
        # Open all the images
        open_image(combined_planes_image_path)
        open_image(combined_logo_planes_image_path)
        open_image(final_image_path)
        QMessageBox.information(self, 'Process Complete', 'Images have been processed and saved.')

    def show_about_me(self):
        about_me_url = "https://imhadi.ir"
        os.system(f"start {about_me_url}")

def main():
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# Developed By: MohammadHadi Daman

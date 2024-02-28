# Image Bit Plane Processor

## Overview

The Image Bit Plane Processor is a Python-based graphical user interface (GUI) application designed to process and manipulate images in an 8-bit layer format. Developed by Hadi Daman, this tool allows users to perform various image processing tasks, such as decomposing images into bit planes, adding logos to images, and combining processed layers into a final composite image.

## Main Purpose

The main purpose of the Image Bit Plane Processor is to provide a user-friendly interface for performing intricate operations on images. The software primarily focuses on three key functionalities:

### 1. Decompose Image to Bit Planes

The application can decompose an input image into its 8-bit binary representation by splitting it into individual bit planes. Each bit plane represents a specific bit (0 to 7) of the pixel values, allowing users to analyze and manipulate the image at different levels of granularity.

### 2. Add Logo to First Layer

Users can add a logo to the first bit plane of the image. The software allows the selection of a logo image, which is then resized to match the dimensions of the loaded image. The logo is added to the first layer, providing a way to watermark or customize the original image.

### 3. Combine Planes to Final Image

The processed bit planes, whether modified or not, can be combined to generate a final composite image. This image represents the culmination of the processing steps, showcasing the effects of adding a logo or other manipulations to the original image.

## Features

- **User-friendly Interface:** Intuitive GUI for easy interaction.
- **Image Loading:** Load images in various formats (PNG, JPG, JPEG, BMP).
- **Bit Plane Decomposition:** Break down images into 8-bit binary planes.
- **Logo Addition:** Add a logo to the first bit plane of the image.
- **Image Combination:** Combine processed bit planes into a final composite image.
- **Interactive Notifications:** Informative pop-up messages for user guidance.

## Getting Started

### Prerequisites

- Python 3.x
- PyQt5
- Pillow (PIL)
- (Other dependencies are mentioned in the code comments)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/image-bit-plane-processor.git
    ```

2. Install the required dependencies:

    ```bash
    pip install PyQt5 Pillow
    ```

### Usage

1. Run the program:

    ```bash
    python main.py
    ```

2. Follow the on-screen instructions to perform image processing tasks.

## Screenshots

(Include screenshots showcasing the application's interface and image processing results.)

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About the Developer

- **Hadi Daman**
  - Website: [imhadi.ir](https://imhadi.ir)

Enjoy processing your images with the Image Bit Plane Processor!

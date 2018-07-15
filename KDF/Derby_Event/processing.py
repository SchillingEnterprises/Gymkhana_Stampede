import argparse
import io
import os

from PIL import Image, ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'images_gallopalooza.com/*.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)


def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """

    # Creates the Service Object
    client = vision.ImageAnnotatorClient()

    # Sends a face detection request
    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations


# Processes the request
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)


# Puts it all together
def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)


def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)


def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)


def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print ('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))


if __name__ == '__main__':
    """Runs the Web Detect application."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))

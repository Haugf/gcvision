# I followed this link : https://cloud.google.com/vision/docs/fulltext-annotations

# The intention of this file is to box any image GCV processes with the JSON output.
# This would let us create configuratoins for different documents quicker.
import argparse
from enum import Enum
import io
import json

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
from google.protobuf import json_format
from PIL import Image, ImageDraw


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
        # font = ImageFont.truetype("sans-serif.ttf", 10)
        draw.text((bound.vertices[0].x, bound.vertices[0].y,),bound,(255,255,255),font=font)
    return image


def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    # client = vision.ImageAnnotatorClient()

    bounds = []


# No need for this .... 
    # with io.open(image_file, 'rb') as image_file:
    #     content = image_file.read()

    # image = types.Image(content=content)

    # response = client.document_text_detection(image=image)
    # document = response.full_text_annotation

    # with open('8130processed.json', 'w') as outfile:
    #     outfile.write(MessageToJson(response))


# We already have the document bounds of the image inside of 8130processed.json no

    f = open ('processed_8130-1output-1-to-1.json', "r")
    data = json.load(f)
    datas=json.dumps(data)
    # print(data)

    response = json_format.Parse(datas, vision.types.AnnotateFileResponse())
    # print(response)
    document = response.inputConfig
    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds = get_document_bounds(filein, FeatureType.BLOCK)
    draw_boxes(image, bounds, 'blue')
    bounds = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'red')

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    render_doc_text(args.detect_file, args.out_file)
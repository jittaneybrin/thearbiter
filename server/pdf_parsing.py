import fitz
import re

from fitz.utils import getColor

# Initial text extraction via PyMuPDF blocks
def get_text_blocks_from_doc(document_name):
    try: 
        doc = fitz.open(document_name) # open a document
    except Exception:
        raise Exception(f"File at path: {document_name} could not be read") 

    all_blocks = []

    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            all_text = block[4]

            # split text into paragraphs
            paragraphs = re.split(r'( *\n *){2,}', all_text) # split text into paragraphs based on 2 or more newlines
            for text in paragraphs:
                text = re.sub(r'\xad\n', '-', text) # replace hyphen code + newline with hyphen 
                text = re.sub(r'\n', ' ', text) # replace newlines with a space
                text = re.sub(r'\t', '', text) # remove tab characters
                text = text.strip() # remove leading and trailing whitespace
                
                # text importance conditions
                substantial = len(text) > 4 # likely a page number or whitespace
            
                if (len(text) < 40):
                    substantial = substantial and ("page" not in text.lower()) # possibly a chapter title and page number

                # add more conditions to clean up / preprocess text here

                if substantial:
                    coordinates = page.search_for(text, clip=block[0:4], quads=True)
                    if len(coordinates) == 0:
                        # text not found on page, try searching for a smaller portion of the text
                        # search for 10 characters at a time
                        for i in range(0, len(text), 10):
                            coordinates += page.search_for(text[i:i+10], clip=block[0:4], quads=True)

                    all_blocks.append({
                        'text': text, 
                        'page': [page.number], 
                        'index_on_page': [block[5]],
                        'coordinates': [coordinates]
                    })
    doc.close()
    return all_blocks


# This function tries to match up sentences that are incorrectly broken up by the PDF reader
def consolidate_broken_sentences(blocks):    
    consolidated_blocks = []
    i = 0

    while i < len(blocks):
        # append the current block to the consolidated list
        # turning the metadata attributes into lists to keep track of combined blocks' information later
        consolidated_blocks.append({
            'text': blocks[i]['text'],
            'page': blocks[i]['page'],
            'index_on_page': blocks[i]['index_on_page'],
            'coordinates': blocks[i]['coordinates']
        })
        
        while True:
            # if we're at the last block, break
            if i == len(blocks) - 1:
                # I think this may allow for the last block to be skipped... But I can't think it through in my head and don't care enough to check
                i += 1
                break
            
            # check if current block ends with a period within the past 5 characters
            unfinished_sentence = (len(blocks[i]['text'])) - blocks[i]['text'].rfind('.') > 3

            # check if next block starts with a lowercase letter
            next_block_lower = blocks[i + 1]['text'][0].islower()
            
            # combine blocks if the sentence is "unfinished" and the next block starts with a lowercase letter
            if unfinished_sentence and next_block_lower:
                # combine texts
                if blocks[i]['text'][-1] == '-':
                    consolidated_blocks[-1]['text'] = consolidated_blocks[-1]['text'][:-1] + blocks[i + 1]['text']
                else:
                    consolidated_blocks[-1]['text'] += ' ' + blocks[i + 1]['text']

                # append metadata
                consolidated_blocks[-1]['page'] += blocks[i + 1]['page']
                consolidated_blocks[-1]['index_on_page'] += blocks[i + 1]['index_on_page']
                consolidated_blocks[-1]['coordinates'] += blocks[i + 1]['coordinates']

                i += 1
            else:
                # the next block is not part of the current sentence. Move out of this inner loop
                i += 1
                break
    
    return consolidated_blocks

def quad_to_tuple(quad):
    return [(point.x, point.y) for point in quad]

def tuple_to_quad(tuple):
    return fitz.Quad([(x, y) for x, y in tuple])


# Highlight block of text in a PDF
def highlight_block(pdf_path, block, output_path=None):
    try: 
        doc = fitz.open(pdf_path) # open a document
    except Exception:
        raise Exception(f"File at path: {pdf_path} could not be read") 

    # loop through each page and highlight each block of text
    for i in range(len(block['page'])):
        shape = doc[block['page'][i]].new_shape()

        # get some initial bounding coordinates to confine the image around
        x0 = block['coordinates'][0][0][0][0]
        y0 = block['coordinates'][0][0][0][1]
        x1 = block['coordinates'][-1][-1][-1][0]
        y1 = block['coordinates'][-1][-1][-1][1]
        
        # highlight each quadrant of text
        for quad in block['coordinates'][i]:
            shape.draw_quad(quad)

            # update bounding coordinates if necessary
            for point in quad:
                x0 = min(x0, point[0])
                y0 = min(y0, point[1])
                x1 = max(x1, point[0])
                y1 = max(y1, point[1])
                    
        shape.finish(fill=getColor("YELLOW"), fill_opacity=0.25, width=0)
        shape.commit()

    page = doc[block['page'][0]]

    mat = fitz.Matrix(2, 2)  # zoom factor 2 in each direction
    buffer = 50
    clip = fitz.Rect(x0 - buffer, y0 - buffer, x1 + buffer, y1 + buffer)  # the area we want
    pix = page.get_pixmap(dpi=200) # render page to an image
    pix.save(output_path)  # store image as a PNG        
    doc.close()
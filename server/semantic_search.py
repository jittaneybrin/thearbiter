from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import embs



def group_by_semantic_similarity(blocks):

    # group blocks of text by page
    text_by_page = []
    for global_index, block in enumerate(blocks):
        # add empty list for each page
        while len(text_by_page) <= block['page'][0]:
            text_by_page.append([])
        # add this block's text to the list for the page
        text_by_page[block['page'][0]].append({'text': block['text'], 'global_index': global_index})


    # add previous and next text blocks to each block 
    text_by_page = [combine_text(page, buffer_size=1) for page in text_by_page]


    # get embeddings for each block of combined_text
    embeddings = embs.get_embeddings()
    combined_text_embeddings = []
    for page in text_by_page:
        combined_text_embeddings.append(embeddings.embed_documents([x['combined_text'] for x in page]))

    # add embeddings to each block
    for i, page in enumerate(text_by_page):
        for j, block in enumerate(page):
            block['combined_text_embedding'] = combined_text_embeddings[i][j]


    # calculate cosine distances between sequential blocks, for each page
    distances_by_page = []
    for page in text_by_page:
        page_distances = calculate_cosine_distances(page)
        distances_by_page.append(page_distances)


    # determine the threshold for grouping blocks
    indices_by_page = []
    for distances in distances_by_page:
        # We need to get the distance threshold that we'll consider an outlier
        # We'll use numpy .percentile() for this
        breakpoint_percentile_threshold = 75
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold) # If you want more chunks, lower the percentile cutoff

        # Then we'll get the index of the distances that are above the threshold. This will tell us where we should split our text
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold] # The indices of those breakpoints on your list

        indices_by_page.append(indices_above_thresh)


    # group blocks by semantic similarity
    grouped_blocks = []
    for i, page in enumerate(text_by_page):
        original_blocks = [block for i, block in enumerate(blocks) if i in [b['global_index'] for b in page]]
        grouped_blocks += group_by_semantic_threshold_indices(indices_by_page[i], original_blocks, buffer_size=2, max_length=1000) 
   
    # Add the text embeddings to the combined blocks
    for combined_block in grouped_blocks:
        combined_block['full_text_embedding'] = embeddings.embed_documents([combined_block['text']])[0]
    
    return grouped_blocks



# Adds a combined_text attribute to each block of text, which is the text of the block combined with the text of the blocks before and after it
def combine_text(all_text, buffer_size=1):
    # Go through each text block
    for i in range(len(all_text)):

        # Create a string that will hold the sentences which are joined
        combined_text = ''

        # Add sentences before the current one, based on the buffer size.
        for j in range(i - buffer_size, i):
            # Check if the index j is not negative (to avoid index out of range like on the first one)
            if j >= 0:
                # Add the sentence at index j to the combined_sentence string
                combined_text += all_text[j]['text'] + ' '

        # Add the current sentence
        combined_text += all_text[i]['text']

        # Add sentences after the current one, based on the buffer size
        for j in range(i + 1, i + 1 + buffer_size):
            # Check if the index j is within the range of the sentences list
            if j < len(all_text):
                # Add the sentence at index j to the combined_sentence string
                combined_text += ' ' + all_text[j]['text']

        # Then add the whole thing to your dict
        # Store the combined sentence in the current sentence dict
        all_text[i]['combined_text'] = combined_text

    return all_text


# Calculate cosine distances between sequential blocks
def calculate_cosine_distances(blocks):
    distances = []
    for i in range(len(blocks) - 1):
        embedding_current = blocks[i]['combined_text_embedding']
        embedding_next = blocks[i + 1]['combined_text_embedding']
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
        
        # Convert to cosine distance
        distance = 1 - similarity

        # Append cosine distance to the list
        distances.append(distance)
        
    return distances


def group_by_semantic_threshold_indices(indices_above_thresh, blocks, buffer_size=3, max_length=1000):
    # Initialize the start index
    start_index = 0

    # Create a list to hold the grouped sentences
    grouped_blocks = []

    # Iterate through the breakpoints to slice the sentences
    for index in indices_above_thresh:
        # The end index is the current breakpoint
        end_index = index

        # Add a buffer to the start index if possible
        start_index, end_index = dynamic_buffer(blocks, buffer_size, max_length, start_index, end_index)

        # Slice the sentence_dicts from the current start index to the end index
        group = blocks[start_index:end_index + 1]
        combined_block = group[0]
        for block in group[1:]:
            combined_block['text'] += ' ' + block['text']
            combined_block['page'] += block['page']
            combined_block['index_on_page'] += block['index_on_page']
            combined_block['coordinates'] += block['coordinates']
        
        # Append the combined block to the grouped blocks
        grouped_blocks.append(combined_block)
        
        # Update the start index for the next group
        start_index = index + 1

    # The last group, if any sentences remain
    if start_index < len(blocks):

        # Add a buffer to the start index if possible
        start_index, end_index = dynamic_buffer(blocks, buffer_size, max_length, start_index, end_index)

        group = blocks[start_index:]
        combined_block = group[0]
        for block in group[1:]:
            combined_block['text'] += ' ' + block['text']
            combined_block['page'] += block['page']
            combined_block['index_on_page'] += block['index_on_page']
            combined_block['coordinates'] += block['coordinates']
        
        # Append the last group to the grouped blocks
        grouped_blocks.append(combined_block)

    return grouped_blocks


# expands the buffer window if the group is under the max length
def dynamic_buffer(blocks, buffer_size, max_length, start_index, end_index):
    # Check if the length of the group is less than the max length
    if group_length(blocks, start_index, end_index) > max_length:
        # the group is already over the max length, return current indices
        return start_index, end_index
    
    # progresively expand the buffer window until the group is over the max length or we reach the buffer size limit
    for i in range(buffer_size):
        # Check if the length of the group is less than the max length
        if start_index - 1 >= 0 and group_length(blocks, start_index - 1, end_index) <= max_length:
            start_index -= 1
        if end_index + 1 < len(blocks) and group_length(blocks, start_index, end_index + 1) <= max_length:
            end_index += 1

    return start_index, end_index

def group_length(blocks, start_index, end_index):
    # Check if the length of the group is less than the max length
    return sum([len(block['text']) for block in blocks[start_index:end_index + 1]])
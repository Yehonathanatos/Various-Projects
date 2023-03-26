import spacy

# Load the medium-sized language model
nlp = spacy.load("en_core_web_md")

# Read in the movies.txt file
with open("movies.txt") as f:
    movie_descs = [line.strip() for line in f]

# Convert the movie descriptions to Doc objects
movie_docs = [nlp(desc) for desc in movie_descs]

# Define a function to return the title of the most similar movie
def get_similar_movie(input_desc):
    # Convert the input description to a Doc object
    input_doc = nlp(input_desc)
    
    # Calculate similarity scores between the input doc and all movie docs
    similarity_scores = [input_doc.similarity(movie_doc) for movie_doc in movie_docs]
    
    # Find the index of the movie with the highest similarity score
    max_index = similarity_scores.index(max(similarity_scores))
    
    # Return the title of the most similar movie
    return f"Next movie to watch: {movie_descs[max_index]}"

# Example usage:
input_desc = "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery and trained as a gladiator."
print(get_similar_movie(input_desc))

import tiktoken



enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hey I am learning genAI"

tokens = enc.encode(text)
print("Here is tokenized form of Prompt: ", tokens)

# Here is tokenized form of Prompt:  [25216, 357, 939, 7524, 3645, 17527]

decoded = enc.decode(tokens)
print("Here is decoded form of Prompt: ", decoded)
#Here is decoded form of Prompt:  Hey I am learning genAI

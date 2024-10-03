import sys
import enchant

# Create an English dictionary object for spell checking
dictionary = enchant.Dict("en_US")

for line in sys.stdin:
    try:
        # Decode the line properly, ignoring invalid characters
        line = line.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

        words = line.strip().split()

        for word in words:
            # Check if the word is not in the English dictionary
            if not dictionary.check(word):
                print(f"{word}\t1")
    except Exception as e:
        sys.stderr.write(f"Error processing line: {line}. Error: {str(e)}\n")

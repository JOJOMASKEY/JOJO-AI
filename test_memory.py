import sys
import os
sys.path.append(os.path.abspath("src"))

import memory

# Add some memories
memory.add_memory("favorite_color", "teal")
memory.add_memory("birth_city", "Kathmandu")

# Retrieve a memory
print("Favorite Color:", memory.get_memory("favorite_color"))

# Update a memory
print(memory.update_memory("favorite_color", "midnight blue"))

# List all memories
print("All Memories:", memory.list_all_memory())

# Delete a memory
print(memory.delete_memory("birth_city"))
print("After Deletion:", memory.list_all_memory())

from prodigy.components.db import connect

db = connect()
dataset = db.get_dataset("climatemind_onto")

print(dataset)

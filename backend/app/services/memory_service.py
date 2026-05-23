from database import SessionLocal
from models import Memory


def save_memory(key, value):

    db = SessionLocal()

    existing = db.query(Memory).filter(Memory.memory_key == key).first()

    if existing:

        existing.memory_value = str(value)

    else:

        memory = Memory(memory_key=key, memory_value=str(value))

        db.add(memory)

    db.commit()

    db.close()


def get_memory(key):

    db = SessionLocal()

    memory = db.query(Memory).filter(Memory.memory_key == key).first()

    db.close()

    if memory:
        return memory.memory_value

    return None


def get_all_memory():

    db = SessionLocal()

    memories = db.query(Memory).all()

    db.close()

    result = {}

    for memory in memories:

        result[memory.memory_key] = memory.memory_value

    return result


def clear_memory():

    db = SessionLocal()

    db.query(Memory).delete()

    db.commit()

    db.close()

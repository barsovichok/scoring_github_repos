import uuid
import config


def create_redis_base():
    redis_storage = config.REDIS_STORAGE
    return redis_storage


def generate_token(redis_storage):
    user_email = input('Введите почту разработчика\n')
    token = str(uuid.uuid4())
    redis_data = redis_storage.set(token, user_email)
    print(redis_data)
    print(token, user_email)


if __name__ == "__main__":
    redis_storage = create_redis_base()
    generate_token(redis_storage)

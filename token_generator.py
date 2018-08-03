import uuid
import config


def generate_token():
    user_email = input('Введите почту разработчика\n')
    token = str(uuid.uuid4())
    redis_storage = config.REDIS_STORAGE
    redis_data = redis_storage.set(token, user_email)
    print(redis_data)
    print(token, user_email)


if __name__ == "__main__":
    generate_token()

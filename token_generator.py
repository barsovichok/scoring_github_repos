import redis
import uuid


def create_redis_base():
    redis_storage = redis.Redis(host='localhost', port=6379, db=0)
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

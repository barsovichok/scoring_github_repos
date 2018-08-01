import redis
import uuid


def create_redis_base():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r


def generate_token(r):
    user_email = input('Введите почту разработчика\n')
    token = str(uuid.uuid4())
    redis_data = r.set(token, user_email)
    print(redis_data)
    print(token, user_email)


if __name__ == "__main__":
    r = create_redis_base()
    generate_token(r)

import uuid
import config
import redis


def create_redis_base():
    redis_storage = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB
    )
    return redis_storage


def generate_token(redis_storage):
    user_email = input('Введите почту разработчика\n')
    token = str(uuid.uuid4())
    redis_data = redis_storage.set(token, user_email)
    print(redis_data)
    print(token, user_email)


def delete_all_keys(redis_storage):
    user_input = input('Удалить все данные в базе? Y/N\n')
    if user_input == 'Y':
        delete_all_keys = redis_storage.flushall()
        if delete_all_keys is True:
            print("Теперь в базе ничего нет!")
    else:
        print('Ok, bye!')


def user_input():
    user_input = int(input('''
        1 - создать новый ключ,
        2 - удалить  все данные из базы\n'''))
    if user_input == 1:
        generate_token(redis_storage)
    else:
        delete_all_keys(redis_storage)


if __name__ == "__main__":
    redis_storage = create_redis_base()
    user_input()

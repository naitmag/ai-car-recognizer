from environs import Env

env = Env()
env.read_env()

SECRET_TOKEN= env.str('SECRET_TOKEN')

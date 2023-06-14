import os


class Env:
    env = os.environ.get('ENVIRONMENT', default=None)

    @staticmethod
    def all_envs_keys():
        return ",".join([i for i in os.environ.keys()])

    @staticmethod
    def is_local():
        return Env.env == "local"

    @staticmethod
    def development():
        return Env.env == "development"

    @staticmethod
    def test():
        return Env.env == "test"

    @staticmethod
    def production():
        return not (Env.development() or Env.test())

    @staticmethod
    def discord_channel_url():
        return os.environ.get('DISCORD_WEBHOOK_URL', default=None)

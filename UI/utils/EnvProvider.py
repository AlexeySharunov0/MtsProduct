import os


class EnvProvider:
    debug = os.getenv("IS_DEBUG") or 'FALSE'
    env = os.getenv("ENV") or "stage"
    is_debug = debug == 'TRUE'
    isDev = env == 'dev'
    isStage = env == 'stage'
    isProd = env == 'prod'
    isLocal = env == 'local'

    @staticmethod
    def getBaseUrl():
        override = os.getenv("BASE_URL")
        if override:
            return override.rstrip('/')
        if EnvProvider.isDev:
            return 'https://dev.prodboard.example.com'
        if EnvProvider.isStage:
            return 'https://stage.prodboard.example.com'
        if EnvProvider.isProd:
            return 'https://product.example.com'
        if EnvProvider.isLocal:
            return 'http://localhost'

        raise ValueError('Undefined env: {}'.format(EnvProvider.env))

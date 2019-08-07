# __author__ = 'wilsonLwx'
# __date__ = '2019/08/07'

# set the DATABASES of test environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'NAME': 'django_dev',
        'HOST': 'mariadb',
        'PORT': 3306,
        'PASSWORD': 'p@ssw0rd123',
    }
}
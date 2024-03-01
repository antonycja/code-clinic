import subprocess
def install_dependencies():
    """
    Installs all the required dependencies (package modules)
    """

    dependencies = ['click', 'tabulate', 'pycryptodome', 'pycryptodomex',
                    'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'ics']

    for depend in dependencies:
        try:
            __import__(depend)
        except ModuleNotFoundError:
            if 'google' in depend:
                subprocess.run(
                    f'pip install --upgrade {depend} > /tmp/ignore.txt', shell=True)
            else:
                subprocess.run(
                    f'pip install {depend} > /tmp/ignore.txt', shell=True)


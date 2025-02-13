import nox

PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
DJANGO_VERSIONS = ["django>=3.2", "django>=4.2,<4.3", "django>=5.1,<5.2"]


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session, django):
    session.install(django)
    session.install("orjson", "ujson")
    session.install("-e", ".")
    session.run("python", "runtests.py")

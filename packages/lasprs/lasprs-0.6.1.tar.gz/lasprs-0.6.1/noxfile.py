import nox

@nox.session
def tests(session):
    session.install('pytest')
    session.install('numpy')
    session.install('maturin')
    session.run('maturin','dev')
    session.run('pytest')

#@nox.session
#def lint(session):
#    session.install('flake8')
#    session.run('flake8', '--import-order-style', 'google')

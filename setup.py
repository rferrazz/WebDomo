from distutils.core import setup

setup(
    name = 'WebDomo',
    version = '0.6.3',
    
    author = 'Riccardo Ferrazzo',
    description = 'Web server that rappresent the core of What is Automation',
    license = 'GNU LGPL',
    
    packages = ['WHIA', 'WHIA.WebDomo', 'WHIA.plugins']
)

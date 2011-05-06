from distutils.core import setup
setup(	name='battleNet',
		version='0.1',
		url='not.yet',
		author='Irving Leonard',
		author_email='irvingleonard@ymail.com',
		packages=['battleNet','battleNet.net','battleNet.servers',],
		package_dir={	'battleNet':'bin',
					},
		scripts=['bin/battleNet_server.py'],
		data_files=[('doc',['doc/bnetdocs.txt']),
					]
      )

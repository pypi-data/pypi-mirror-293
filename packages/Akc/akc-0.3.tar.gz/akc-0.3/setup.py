try:
    from setuptools import setup, find_packages
except ImportError:
    raise Exception("Bize böyle bir bilgi gelmedi. Lütfen ---> pip install setuptools")

setup(
    name="Akc",
    version="0.3",  
    author="Hasan AKÇAKOCA",
    author_email="hasanakcakoca@gmail.com",
    description="Akc.base deneme.",  
    packages=find_packages(),  
    install_requires=[
        # Bağımlılıkları buraya ekleyin
    ],
    python_requires='>=3',   
)


#paket oluşturma
#python setup.py sdist 
#python setup.py sdist bdist_wheel

#https://pypi.org ye yükleme
#twine upload dist/*

#https://medium.com/bili%C5%9Fim-hareketi/python-dosya-da%C4%9F%C4%B1t%C4%B1m%C4%B1-olu%C5%9Fturmak-93009925bd19
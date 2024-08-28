from setuptools import setup, find_packages

setup(
    name='maptrDH',                      # 库的名称
    version='0.1.0',                        # 版本号
    author='Feng XY',                     # 作者            
    author_email='feng452141@163.com',  # 作者邮箱                  
    description='A library for data handling with various utilities.',  # 简短描述                  
    long_description=open('README.md').read(),  # 从 README.md 中读取详细描述           
    long_description_content_type='text/markdown',  # README 文件的格式                 
    url='https://github.com/wisdom1python/maptr_dataHandle', # 项目主页             
    packages=find_packages(),               # 自动找到项目中的所有包                                
    install_requires=[                      # 依赖包                        
        'geopandas==0.13.2',
        'laspy==2.5.4',
        'matplotlib==3.5.2',
        'numpy==1.22.2',
        'open3d==0.18.0',
        'pandas==1.4.4',
        'pypcd==0.1.1',
        'pyshp==2.3.1',
        'scipy==1.10.1',                            
        'Shapely==1.8.5.post1',                             
        'tqdm==4.66.1'
    ],
    classifiers=[                           # 分类器，帮助用户了解你的库                
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',                # 支持的 Python 版本                    
)
from setuptools import Command, find_packages, setup

__lib_name__ = "GraphCVAE"
__lib_version__ = "1.0.1"
__description__ = "GraphCVAE: Uncovering Cell Heterogeneity and Therapeutic Target Discovery through Residual and Contrastive Learning"
__url__ = "https://github.com/ZhiWeiZhang0336/GraphCVAE"
__author__ = "Zhiwei Zhang"
__author_email__ = "2023520218@bipt.eud.cn"
__license__ = "MIT"
__keywords__ = ["Spatial Transcriptomics", "Variational Graph Autoencoder",  "Contrastive Learning", "Spatial Clustering","Deep Learning","Gene Expression",]
__requires__ = ["requests",]

with open("README.rst", "r", encoding="utf-8") as f:
    __long_description__ = f.read()

setup(
    name = __lib_name__,
    version = __lib_version__,
    description = __description__,
    url = __url__,
    author = __author__,
    author_email = __author_email__,
    license = __license__,
    packages = ["GraphCVAE"],
    install_requires = __requires__,
    zip_safe = False,
    include_package_data = True,
    long_description = """Integration of multiple data modalities in a spatially informed manner remains an unmet need for exploiting spatial multi-omics data. Here, we introduce SpatialGlue, a novel graph neural network with dual-attention mechanism, to decipher spatial domains by intra-omics integration of spatial location and omics measurement followed by cross-omics integration. We demonstrate that SpatialGlue can more accurately resolve spatial domains at a higher resolution across different tissue types and technology platforms, to enable biological insights into cross-modality spatial correlations. SpatialGlue is computation resource efficient and can be applied for data from various spatial multi-omics technological platforms, including Spatial-epigenome-transcriptome, Stereo-CITE-seq, SPOTS, and 10x Visium. Next, we will extend SpatialGlue to more platforms, such as 10x Genomics Xenium and Nanostring CosMx. """,
    long_description_content_type="text/markdown"
)
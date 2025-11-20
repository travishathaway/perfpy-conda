FROM continuumio/miniconda3:latest

WORKDIR /app/
COPY profiles/ .
COPY scripts/ .

RUN conda install conda-canary/label/dev::conda-libmamba-solver  --yes --quiet
RUN pip install git+https://github.com/travishathaway/perfpy.git
RUN mkdir data

ENTRYPOINT ["perfpy"]

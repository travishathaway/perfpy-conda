FROM continuumio/miniconda3:latest

RUN apt update && apt upgrade -y

WORKDIR /app/
COPY profiles/ .
COPY scripts/ .

RUN conda install conda-canary/label/dev::conda-libmamba-solver  --yes --quiet
RUN conda install conda-forge::py-rattler --yes --quiet
RUN pip install git+https://github.com/travishathaway/perfpy.git
RUN mkdir data

ENTRYPOINT ["perfpy"]

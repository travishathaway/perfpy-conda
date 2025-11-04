FROM continuumio/miniconda3:latest

WORKDIR /app/
COPY to_profile.json .

RUN conda install conda-canary/label/dev::conda-libmamba-solver  --yes --quiet
RUN pip install git+https://github.com/travishathaway/perfpy.git
RUN mkdir data

CMD ["perfpy", "to_profile.json", "--output", "data/report.csv"]

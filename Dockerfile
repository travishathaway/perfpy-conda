FROM continuumio/miniconda3:latest

WORKDIR /app/
COPY to_profile.json .

RUN pip install git+https://github.com/travishathaway/perfpy.git
RUN mkdir data

CMD ["perfpy", "to_profile.json", "--output", "data/report.csv"]

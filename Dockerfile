# Use continuumio/miniconda3 as the base image
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/opt/conda/bin:$PATH

# Copy environment file first for better caching
COPY environment.yml ./

# Create conda environment using the environment file
# Note: SSL verification is disabled temporarily to avoid certificate issues in Docker
RUN conda config --set ssl_verify false && \
    conda env create -f environment.yml && \
    conda config --set ssl_verify true && \
    conda clean -afy && \
    echo "conda activate perfpy-conda" >> ~/.bashrc

# Make sure conda environment is activated by default
SHELL ["conda", "run", "-n", "perfpy-conda", "/bin/bash", "-c"]

# Copy the rest of the application code
COPY . .

# Install any additional requirements if requirements.txt exists
RUN if [ -f requirements.txt ]; then \
        conda run -n perfpy-conda pip install --no-deps -r requirements.txt; \
    fi

# Activate the conda environment and set it as default
ENV CONDA_DEFAULT_ENV=perfpy-conda
ENV PATH=/opt/conda/envs/perfpy-conda/bin:$PATH

# Default command - run the example application
CMD ["conda", "run", "--no-capture-output", "-n", "perfpy-conda", "python", "app.py"]
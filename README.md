# perfpy-conda

A Docker application repository using continuumio/miniconda3:latest as the base image. This repository provides a customizable Docker container for Python applications with conda package management.

## 🐳 Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and run the container
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Execute commands in the running container
docker-compose exec perfpy-conda bash
```

### Using Docker directly

```bash
# Build the Docker image
docker build -t perfpy-conda .

# Run the container
docker run --rm perfpy-conda

# Run interactively
docker run --rm -it perfpy-conda bash

# Mount current directory for development
docker run --rm -it -v $(pwd):/app perfpy-conda bash
```

## 📁 Repository Structure

```
.
├── Dockerfile              # Main Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Files to exclude from Docker build
├── environment.yml         # Conda environment specification
├── app.py                  # Example Python application
└── README.md              # This file
```

## 🔧 Customization

### Modifying the Conda Environment

Edit `environment.yml` to customize your conda environment:

```yaml
name: perfpy-conda
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy
  - pandas
  - your-package-here
  - pip
  - pip:
    - your-pip-package-here
```

### Customizing the Dockerfile

The Dockerfile is designed to be easily customizable:

1. **Change Python version**: Modify the `environment.yml` file
2. **Add system packages**: Add RUN commands with `apt-get install`
3. **Change working directory**: Modify the `WORKDIR` instruction
4. **Add custom commands**: Modify the `CMD` instruction

### Adding Your Application

Replace or modify `app.py` with your own Python application. The container will automatically use your code.

## 🚀 Running Your Application

### Default Application

The container runs `app.py` by default, which demonstrates that the environment is working correctly.

### Custom Commands

```bash
# Run a specific Python script
docker-compose run perfpy-conda conda run -n perfpy-conda python your_script.py

# Start a Jupyter notebook (uncomment ports in docker-compose.yml)
docker-compose run -p 8888:8888 perfpy-conda conda run -n perfpy-conda jupyter notebook --ip=0.0.0.0 --allow-root

# Run Python interactively
docker-compose run perfpy-conda conda run -n perfpy-conda python -i

# Install additional packages
docker-compose run perfpy-conda conda run -n perfpy-conda pip install your-package
```

## 🛠️ Development

### Building and Testing

```bash
# Build the image
docker build -t perfpy-conda .

# Test the build
docker run --rm perfpy-conda

# Get a shell in the container
docker run --rm -it perfpy-conda bash

# Check conda environment
docker run --rm perfpy-conda conda info --envs
```

### Debugging

```bash
# View container logs
docker-compose logs perfpy-conda

# Access running container
docker-compose exec perfpy-conda bash

# Check conda packages
docker-compose exec perfpy-conda conda list
```

## 📦 Features

- ✅ **continuumio/miniconda3:latest** base image
- ✅ **Customizable conda environment** via environment.yml
- ✅ **Docker Compose** support for easy management
- ✅ **Development-friendly** volume mounting
- ✅ **Optimized build context** with .dockerignore
- ✅ **Example application** to verify functionality
- ✅ **Flexible configuration** for different use cases

## 🤝 Contributing

Feel free to customize this repository for your specific needs. The Docker setup is designed to be flexible and adaptable to various Python/conda workflows.

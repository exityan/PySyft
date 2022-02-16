#### INSTRUCTIONS
# BUILD the syft base image first

# RUN
# $ docker build -f docker/notebook.Dockerfile -t openmined/syft-notebook:latest -t openmined/syft-notebook:`python VERSION` .
# $ docker run -it --rm -v "`pwd`:/notebook" -p 8888:8888 openmined/syft-notebook

ARG VERSION=latest
FROM wicrep/syft:$VERSION

RUN pip install matplotlib jupyterlab ipywidgets

WORKDIR /notebook

CMD ["bash", "-c", "jupyter lab --allow-root --ip=0.0.0.0"]

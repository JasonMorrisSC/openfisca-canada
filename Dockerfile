FROM python:3.7
COPY ./ /openfisca-canada
RUN pip install /openfisca-canada
ENTRYPOINT openfisca serve --bind 0.0.0.0:80
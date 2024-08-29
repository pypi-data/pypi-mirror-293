FROM registry.gitlab.com/empaia/integration/ci-docker-images/test-runner:0.2.8@sha256:0c20dd487c2bb040fd78991bf54f396cb1fd9ab314a7a55bee0ad4909748797d AS build0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /plugin_build

WORKDIR /plugin_build/utils
RUN poetry build

WORKDIR /plugin_build/isyntax
RUN poetry build

FROM ubuntu:18.04@sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-pip python3-wheel python3-setuptools unzip

COPY /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip

WORKDIR /isyntax

RUN unzip philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip \
    && cd philips-pathologysdk-2.0-ubuntu18_04_py36_research \
    && chmod 777 InstallPathologySDK.sh \
    && ./InstallPathologySDK.sh py3 -y \
    && cd .. \
    && rm -r philips-pathologysdk-2.0-ubuntu18_04_py36_research

COPY --from=build0 /plugin_build/utils/dist/ /plugin_build/utils/dist/
COPY --from=build0 /plugin_build/isyntax/dist/*.whl /tmp

RUN pip3 install Pillow==6.2.2

RUN pip3 install /plugin_build/utils/dist/*.whl
RUN pip3 install /tmp/*.whl

CMD ["python3", "-m", "cds_plugin_isyntax"]

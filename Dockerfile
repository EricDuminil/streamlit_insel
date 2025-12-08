FROM ghcr.io/astral-sh/uv:bookworm-slim

# TODO: Multi-stage, without uv
# TODO: Non root

################################################################################
#                              INSEL, without GUI                              #
################################################################################
ARG INSEL_VERSION=8.3.2.0b
ARG DEBIAN_FRONTEND=noninteractive

ARG INSEL_DEB="insel_${INSEL_VERSION}_x64.deb"
ARG INSEL_URL=https://insel.eu/download/${INSEL_DEB}

RUN apt-get update && \
    apt-get install curl \
      gnuplot \
      --no-install-recommends -y && \
    curl ${INSEL_URL} -o /tmp/${INSEL_DEB} -k && \
    apt-get install /tmp/${INSEL_DEB} --no-install-recommends -y && \
    apt-get remove curl -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm /tmp/${INSEL_DEB}

################################################################################
#                                     App                                      #
################################################################################

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

CMD ["uv", "run", "streamlit", "run", "main.py"]

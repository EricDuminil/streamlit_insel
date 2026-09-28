################################################################################
#                 Multi stage docker, for Streamlit INSEL App                  #
################################################################################

################################################################################
#                         Stage 1 : UV + dependencies                          #
################################################################################

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
COPY . /app
RUN uv sync --locked --no-dev

################################################################################
#                                 INSEL + App                                  #
################################################################################

# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.
FROM python:3.12-slim-bookworm

########################
#  INSEL, without GUI  #
########################
ARG INSEL_VERSION=8.3.3.9b
ARG DEBIAN_FRONTEND=noninteractive

ARG INSEL_DEB="insel_${INSEL_VERSION}_x64_mini.deb"
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

########################
#         App          #
########################

# Setup a non-root user
RUN groupadd --system --gid 1234 nonroot \
 && useradd --system --gid 1234 --uid 1234 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER nonroot

# Use `/app` as the working directory
WORKDIR /app

CMD ["streamlit", "run", "insel_web_app.py", "--browser.gatherUsageStats", "false"]

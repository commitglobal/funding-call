ARG NODE_VERSION=24.13.1
ARG PYTHON_VERSION=3.13.12
ARG ALPINE_VERSION=3.23

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS frontend

RUN apk upgrade --no-cache

WORKDIR /var/www/funding_call/frontend

COPY ./frontend/ .

ARG VERSION
ARG REVISION

ENV VITE_VERSION=${VERSION}
ENV VITE_REVISION=${REVISION}

# install the frontend libraries:
RUN npm ci --no-audit --ignore-scripts && \
    npm run prod


FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS backend

RUN apk --no-cache add \
    curl \
    ca-certificates \
    build-base \
    linux-headers \
    icu-dev \
    gettext \
    gettext-dev \
    gcc \
    musl-dev \
    libffi-dev

ENV PYTHONUNBUFFERED=1

# Make sure scripts in .local are usable:
ENV PATH="/root/.local/bin:${PATH}"

# Download the latest UV installer
ADD ./docker/third-party/uv/installer.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Python virtualenv paths
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

WORKDIR /build
COPY ./backend/pyproject.toml ./backend/uv.lock ./
RUN uv sync --no-dev --active --locked --compile-bytecode && \
    uv pip uninstall pip setuptools


FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ENV PYTHONUNBUFFERED=1

ENV DEBUG=False
ENV ENVIRONMENT=production

ENV RUN_MIGRATIONS=True
ENV RUN_COMPILE_MESSAGES=True
ENV RUN_COLLECT_STATIC=True
ENV RUN_CREATE_ADMIN=True
ENV RUN_SEED_GROUPS=True
ENV ENABLE_DJANGO_ADMIN=False

ENV IS_CONTAINERIZED=True

RUN apk update && \
    apk upgrade && \
    apk --no-cache add \
    icu \
    gettext \
    nginx

# configure process manager
ARG S6_OVERLAY_VERSION=3.2.2.0
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

COPY ./docker/nginx/nginx.conf /etc/nginx/http.d/default.conf

COPY ./docker/s6-rc.d /etc/s6-overlay/s6-rc.d


# Uninstall pip and setuptools from the container
RUN pip uninstall -y pip setuptools && \
    rm -rf \
        /root/.cache/ \
        /usr/local/bin/pip \
        /usr/local/lib/pip

# Python virtualenv paths
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# copy the backend and frontend source code and libraries from the build stage:
COPY --from=backend "${VIRTUAL_ENV}" "${VIRTUAL_ENV}"

# copy the backend and frontend source code:
COPY ./backend/ /var/www/funding_call/backend/
COPY --from=frontend /var/www/funding_call/frontend/dist/ /var/www/funding_call/frontend/dist/


ARG VERSION
ARG REVISION

RUN touch /var/www/funding_call/.version && \
    echo "$VERSION+$(echo ${REVISION} | cut -c 1-7)" > /var/www/funding_call/.version


# specify a certificate store for the runtime
ARG CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV CURL_CA_BUNDLE=${CURL_CA_BUNDLE}


ENTRYPOINT ["/init"]

WORKDIR /var/www/funding_call/

EXPOSE 80

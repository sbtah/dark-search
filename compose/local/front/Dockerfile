FROM node:lts-alpine

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY /front/package.json  /front/package-lock.json* .
COPY ./compose/local/front/start /start
RUN chmod +x /start

RUN npm ci
COPY /front .

# Next.js collects completely anonymous telemetry data about general usage. Learn more here: https://nextjs.org/telemetry
# Uncomment the following line to disable telemetry at run time
ENV NEXT_TELEMETRY_DISABLED 1

FROM node:16-alpine3.17
#ARG PUBLIC_API_URL
#ARG NODE_ENV

ENV PUBLIC_API_URL ${PUBLIC_API_URL}
ENV NODE_ENV ${NODE_ENV}


RUN apk add git
RUN apk add npm

COPY . /app
WORKDIR /app
RUN npm install -g pnpm
RUN pnpm i
RUN npm run build
RUN npm run generate

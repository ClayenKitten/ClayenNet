FROM oven/bun:1.2-alpine
WORKDIR /app
ENV NODE_ENV=production

COPY package.json .
COPY bun.lock .
RUN bun install --frozen-lockfile --production

COPY . .

CMD ["bun", "start"]

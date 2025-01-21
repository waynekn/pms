FROM  node:22.13-alpine

WORKDIR /code/frontend/

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run watch-tailwind

EXPOSE 5173

CMD ["npm","run","dev"]
FROM node:24 as builder
# Étape 1 : build de l'application
WORKDIR /app
COPY . .
RUN npm install && npm run build
# Étape 2 : image finale légère
FROM node:alpine
COPY --from=builder /app/dist /usr/share/node/html
EXPOSE 3000   
ENV NODE_ENV=production
CMD ["node","src/index.js"]
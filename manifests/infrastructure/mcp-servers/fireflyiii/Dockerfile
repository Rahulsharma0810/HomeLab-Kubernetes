# Multi-stage build for Firefly III MCP Server
FROM node:lts-alpine3.22 AS production

# Install dumb-init for proper signal handling and update packages
RUN apk update && apk upgrade && apk add --no-cache dumb-init

# Create app user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S firefly -u 1001 -G nodejs

# Set working directory
WORKDIR /app

# Install the published npm package
RUN npm install -g @firefly-iii-mcp/server

# Copy the package binary to our app directory
RUN cp -r /usr/local/lib/node_modules/@firefly-iii-mcp/server/* .

# Switch to non-root user
USER firefly

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "http.get('http://localhost:3000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) }).on('error', () => process.exit(1))"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application using the global binary
CMD ["firefly-iii-mcp-server"]

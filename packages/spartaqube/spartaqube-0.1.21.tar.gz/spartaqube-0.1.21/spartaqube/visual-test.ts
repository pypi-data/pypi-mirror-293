(async () => {
  const { startServer } = await import('cypress-image-diff-html-report');
  await startServer({
    configFile: 'cypress-image-diff.config.js',
    serverPort: 6868
  });
})();

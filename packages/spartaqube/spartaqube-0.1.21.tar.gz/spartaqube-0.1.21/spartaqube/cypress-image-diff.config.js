// cypress-image-diff.config.js
const config = {
    ROOT_DIR: './cypress/visual-tests', // Store all visual test artifacts in this directory
    JSON_REPORT: { 
        FILENAME: 'cypress_visual_report',
        OVERWRITE: true,
    },
    REPORT_DIR: 'html-report',
    reportJsonDir: './cypress/visual-tests/html-report',
};
  
module.exports = config;
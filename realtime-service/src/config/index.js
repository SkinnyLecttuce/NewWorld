require('dotenv').config();

module.exports = {
    port: process.env.PORT || 4000,
    corsOrigin: process.env.CORS_ORIGIN || 'http://localhost:5173',
    nodeEnv: process.env.NODE_ENV || 'development', 
};
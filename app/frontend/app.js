const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();
const port = 3000;

// Serve static files from the public directory
app.use(express.static('public'));

// Proxy endpoint for GitHub webhook events
app.get('/webhook/events', async (req, res) => {
    try {
        // Replace with your Flask backend URL
        const response = await axios.get('http://localhost:3000/webhook/events/');
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching events:', error);
        // res.status(500).json({ error: 'Failed to fetch events' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
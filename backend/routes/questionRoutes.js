const express = require("express");
const axios = require("axios");

const router = express.Router();

const AI_SERVICE_URL = "http://127.0.0.1:8000";

router.post("/generate", async (req, res) => {
  try {
    const response = await axios.post(
      `${AI_SERVICE_URL}/generate-questions`,
      req.body
    );

    res.json(response.data);
  } catch (error) {
    console.error("Question generation error:", error.message);

    res.status(500).json({
      message: "Failed to generate interview questions",
      error: error.response?.data || error.message,
    });
  }
});

module.exports = router;
const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");
const resumeRoutes = require("./routes/resumeRoutes");
const questionRoutes = require("./routes/questionRoutes");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.use("/api/resume", resumeRoutes);
app.use("/api/questions", questionRoutes);

app.get("/", (req, res) => {
  res.send("AI Interview Backend is running!");
});

connectDB();

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
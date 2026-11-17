const express = require("express");
const multer = require("multer");
const { PDFParse } = require("pdf-parse");
const mammoth = require("mammoth");
const path = require("path");
const axios = require("axios");

const Resume = require("../models/Resume");
const Job = require("../models/Job");

const router = express.Router();

const upload = multer({
    storage: multer.memoryStorage(),
    limits: {
        fileSize: 5 * 1024 * 1024,
    },
});

router.post("/upload", upload.single("resume"), async (req, res) => {

    try {

        if (!req.file) {

            return res.status(400).json({
                message: "Please upload a PDF or DOCX resume",
            });
        }

        const {
            jobTitle,
            jobDescription,
            difficulty,
            numberOfQuestions,
            questionType,
        } = req.body;


        // =====================================================
        // EXTRACT RESUME TEXT
        // =====================================================

        const extension = path
            .extname(req.file.originalname)
            .toLowerCase();

        let resumeText = "";


        if (extension === ".pdf") {

            const parser = new PDFParse({
                data: req.file.buffer,
            });

            const result = await parser.getText();

            resumeText = result.text;

            await parser.destroy();

        } else if (extension === ".docx") {

            const result = await mammoth.extractRawText({
                buffer: req.file.buffer,
            });

            resumeText = result.value;

        } else {

            return res.status(400).json({
                message: "Only PDF and DOCX files are allowed",
            });
        }


        // =====================================================
        // ANALYZE RESUME
        // =====================================================

        const aiResponse = await axios.post(
            "http://127.0.0.1:8000/analyze",
            {
                resumeText,
            }
        );


        // =====================================================
        // SAVE RESUME
        // =====================================================

        const resume = await Resume.create({

            resumeText,

            skills: aiResponse.data.skills,

            education: aiResponse.data.education,

            experience: aiResponse.data.experience,

            projects: aiResponse.data.projects,
        });


        // =====================================================
        // SAVE JOB
        // =====================================================

        let job = null;

        if (jobTitle || jobDescription) {

            job = await Job.create({

                title: jobTitle,

                description: jobDescription,
            });
        }


        // =====================================================
        // GENERATE QUESTIONS
        // =====================================================

        const questionResponse = await axios.post(

            "http://127.0.0.1:8000/generate-questions",

            {

                skills: aiResponse.data.skills,

                education: aiResponse.data.education,

                experience: aiResponse.data.experience,

                projects: aiResponse.data.projects,

                name: aiResponse.data.name,

                jobRole: jobTitle || "",

                jobDescription: jobDescription || "",

                difficulty: difficulty || "Medium",

                numberOfQuestions:
                    Number(numberOfQuestions) || 5,

                questionType:
                    questionType || "technical",
            }
        );


        // =====================================================
        // RESPONSE
        // =====================================================

        res.json({

            message:
                "Resume uploaded and interview questions generated successfully",

            resumeId: resume._id,

            jobId: job ? job._id : null,

            fileName: req.file.originalname,

            skills: aiResponse.data.skills,

            education: aiResponse.data.education,

            experience: aiResponse.data.experience,

            projects: aiResponse.data.projects,

            questionType:
                questionResponse.data.questionType,

            questions:
                questionResponse.data.questions,
        });


    } catch (error) {

        console.error(
            "Resume processing error:",
            error.message
        );

        res.status(500).json({

            message: "Failed to process resume",

            error:
                error.response?.data ||
                error.message,
        });
    }
});


module.exports = router;
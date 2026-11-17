
import { useState } from "react";
import axios from "axios";

function App() {
  const [resume, setResume] = useState(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [difficulty, setDifficulty] = useState("Medium");
  const [numberOfQuestions, setNumberOfQuestions] = useState(5);
  const [questionType, setQuestionType] = useState("technical");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setResume(file);
    }
  };

  const uploadResume = async () => {
    if (!resume) {
      alert("Please select a resume");
      return;
    }

    if (!jobTitle.trim()) {
      alert("Please enter a job role");
      return;
    }

    const formData = new FormData();

    formData.append("resume", resume);
    formData.append("jobTitle", jobTitle);
    formData.append("jobDescription", jobDescription);
    formData.append("difficulty", difficulty);
    formData.append("numberOfQuestions", numberOfQuestions);
    formData.append("questionType", questionType);

    try {
      setLoading(true);
      setResult(null);

      const response = await axios.post(
        "http://localhost:5000/api/resume/upload",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      const message =
        error.response?.data?.message ||
        "Resume processing failed. Please try again.";

      alert(message);
    } finally {
      setLoading(false);
    }
  };

  const questionTypeLabel = {
    technical: "Technical",
    experience: "Experience",
    hr: "HR",
  };

  const questionTypeDescription = {
    technical:
      "Tests technical knowledge based on the candidate's skills, job role and job description.",
    experience:
      "Focuses on technical questions related to the candidate's projects, internships and work experience.",
    hr: "Generates behavioral, personal and job-related HR questions for the candidate.",
  };

  const inputClass =
    "w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 text-slate-800 placeholder-slate-400 shadow-sm outline-none transition-all duration-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-50 hover:border-slate-300";

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900">

      {/* Subtle background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-blue-100/40 blur-[100px] rounded-full" />
      </div>

      {/* Navbar */}
      <nav className="relative z-10 bg-white/90 backdrop-blur-xl border-b border-slate-200/80">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center shadow-md">
              <span className="text-white font-bold text-sm">AI</span>
            </div>

            <div>
              <h1 className="font-bold text-lg tracking-tight text-slate-900">
                AI Interview
              </h1>

              <p className="text-xs text-slate-400">
                Intelligent Recruitment Platform
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-100">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-xs font-medium text-emerald-700">
              AI System Online
            </span>
          </div>

        </div>
      </nav>

      {/* Main */}
      <main className="relative z-10 max-w-6xl mx-auto px-5 py-14">

        {/* Hero */}
        <section className="text-center max-w-3xl mx-auto mb-11">

          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-100 text-blue-600 text-xs font-semibold mb-5">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
            AI-POWERED INTERVIEW INTELLIGENCE
          </div>

          <h2 className="text-4xl md:text-5xl font-bold tracking-tight leading-tight text-slate-950">
            Turn Resumes Into
            <span className="block text-blue-600 mt-1">
              Smarter Interviews
            </span>
          </h2>

          <p className="mt-5 text-slate-500 text-base md:text-lg leading-relaxed max-w-2xl mx-auto">
            Upload a candidate's resume and generate personalized interview
            questions based on their skills, experience and target role.
          </p>

        </section>

        {/* Main Card */}
        <section className="bg-white border border-slate-200 rounded-3xl shadow-[0_20px_60px_rgba(15,23,42,0.07)] overflow-hidden">

          {/* Card Header */}
          <div className="px-7 md:px-10 py-7 border-b border-slate-100">

            <div className="flex items-center gap-4">

              <div className="w-11 h-11 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center">
                <span className="text-blue-600 text-xl">+</span>
              </div>

              <div>
                <h3 className="font-bold text-lg text-slate-900">
                  Create New Interview
                </h3>

                <p className="text-sm text-slate-400 mt-1">
                  Configure the interview and analyze your candidate.
                </p>
              </div>

            </div>

          </div>

          {/* Form */}
          <div className="p-7 md:p-10">

            {/* Resume Upload */}
            <div>

              <div className="flex items-center justify-between mb-3">

                <label className="text-sm font-semibold text-slate-800">
                  Candidate Resume
                </label>

                <span className="text-xs text-slate-400">
                  PDF / DOCX • 5MB max
                </span>

              </div>

              <label
                htmlFor="resumeInput"
                className={`group relative flex flex-col items-center justify-center min-h-[220px] rounded-2xl border-2 border-dashed cursor-pointer transition-all duration-300 ${
                  resume
                    ? "border-emerald-300 bg-emerald-50/60"
                    : "border-slate-200 bg-slate-50/70 hover:bg-blue-50/50 hover:border-blue-300"
                }`}
              >

                <div className="absolute top-4 right-4 text-xs font-medium text-slate-400">
                  {resume ? "READY" : "UPLOAD"}
                </div>

                <div
                  className={`w-16 h-16 rounded-2xl flex items-center justify-center shadow-sm transition-all duration-300 group-hover:-translate-y-1 ${
                    resume
                      ? "bg-emerald-100 text-emerald-600"
                      : "bg-white border border-slate-200 text-blue-600"
                  }`}
                >
                  <span className="text-3xl">
                    {resume ? "✓" : "↑"}
                  </span>
                </div>

                <p className="mt-5 font-semibold text-slate-800">
                  {resume
                    ? "Resume selected"
                    : "Upload candidate resume"}
                </p>

                <p className="text-sm text-slate-400 mt-1 max-w-md text-center truncate px-5">
                  {resume
                    ? resume.name
                    : "Click to browse PDF or DOCX"}
                </p>

                {resume && (
                  <div className="mt-4 px-3 py-1.5 rounded-full bg-emerald-100 text-emerald-700 text-xs font-medium">
                    ✓ Ready for analysis
                  </div>
                )}

                <input
                  id="resumeInput"
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  className="hidden"
                />

              </label>

            </div>

            {/* Divider */}
            <div className="flex items-center gap-4 my-9">

              <div className="h-px bg-slate-200 flex-1" />

              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-[0.15em]">
                Interview Setup
              </span>

              <div className="h-px bg-slate-200 flex-1" />

            </div>

            {/* Configuration */}
            <div className="grid md:grid-cols-2 gap-6">

              {/* Job Role */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Job Role
                  <span className="text-red-500 ml-1">*</span>
                </label>

                <input
                  type="text"
                  placeholder="e.g. Full Stack Developer"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                  className={inputClass}
                />
              </div>

              {/* Question Type */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Question Type
                </label>

                <select
                  value={questionType}
                  onChange={(e) =>
                    setQuestionType(e.target.value)
                  }
                  className={inputClass}
                >
                  <option value="technical">
                    Technical Questions
                  </option>

                  <option value="experience">
                    Experience Questions
                  </option>

                  <option value="hr">
                    HR Questions
                  </option>
                </select>
              </div>

              {/* Difficulty */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Difficulty Level
                </label>

                <select
                  value={difficulty}
                  onChange={(e) =>
                    setDifficulty(e.target.value)
                  }
                  className={inputClass}
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              {/* Number */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Number of Questions
                </label>

                <select
                  value={numberOfQuestions}
                  onChange={(e) =>
                    setNumberOfQuestions(Number(e.target.value))
                  }
                  className={inputClass}
                >
                  <option value={5}>5 Questions</option>
                  <option value={10}>10 Questions</option>
                  <option value={15}>15 Questions</option>
                  <option value={20}>20 Questions</option>
                </select>
              </div>

              {/* Job Description */}
              <div className="md:col-span-2">

                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Job Description

                  <span className="text-slate-400 font-normal ml-1">
                    (Optional)
                  </span>
                </label>

                <textarea
                  placeholder="Add responsibilities, requirements or specific technologies..."
                  value={jobDescription}
                  onChange={(e) =>
                    setJobDescription(e.target.value)
                  }
                  rows="4"
                  className={`${inputClass} resize-none`}
                />

              </div>

            </div>

            {/* Question Type Info */}
            <div className="mt-7 rounded-xl border border-blue-100 bg-gradient-to-r from-blue-50/70 to-slate-50 overflow-hidden">

              <div className="flex">

                <div className="w-1 bg-blue-500" />

                <div className="p-4 flex items-start gap-3">

                  <div className="w-8 h-8 rounded-lg bg-white border border-blue-100 text-blue-600 flex items-center justify-center shadow-sm">
                    i
                  </div>

                  <div>

                    <p className="text-sm font-semibold text-slate-800">
                      {questionTypeLabel[questionType]} Interview
                    </p>

                    <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                      {questionTypeDescription[questionType]}
                    </p>

                  </div>

                </div>

              </div>

            </div>

            {/* Generate Button */}
            <button
              onClick={uploadResume}
              disabled={loading}
              className="group relative w-full mt-8 py-4 rounded-xl bg-slate-900 hover:bg-blue-600 disabled:bg-slate-400 text-white font-semibold shadow-lg shadow-slate-900/10 hover:shadow-blue-500/20 transition-all duration-300 overflow-hidden"
            >

              <span className="relative flex items-center justify-center gap-3">

                {loading ? (
                  <>
                    <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />

                    <span>
                      AI is analyzing the resume...
                    </span>
                  </>
                ) : (
                  <>
                    <span>
                      Generate Interview Questions
                    </span>

                    <span className="group-hover:translate-x-1 transition-transform">
                      →
                    </span>
                  </>
                )}

              </span>

            </button>

            <p className="text-center text-xs text-slate-400 mt-4">
              AI analyzes the resume and creates personalized questions.
            </p>

          </div>

        </section>

        {/* Results */}
        {result && (
          <section className="mt-10 space-y-6">

            {/* Candidate Profile */}
            <div className="bg-white border border-slate-200 rounded-2xl shadow-[0_12px_40px_rgba(15,23,42,0.05)] overflow-hidden">

              <div className="px-7 md:px-9 py-6 border-b border-slate-100">

                <div className="flex items-center justify-between">

                  <div className="flex items-center gap-4">

                    <div className="w-11 h-11 rounded-xl bg-slate-900 text-white flex items-center justify-center">
                      🔎
                    </div>

                    <div>

                      <h2 className="text-xl font-bold text-slate-900">
                        Candidate Profile
                      </h2>

                      <p className="text-sm text-slate-400 mt-1">
                        Skills identified from the resume
                      </p>

                    </div>

                  </div>

                  <span className="hidden sm:block px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-600 text-[11px] font-semibold">
                    ANALYSIS COMPLETE
                  </span>

                </div>

              </div>

              <div className="p-7 md:p-9">

                <div className="flex flex-wrap gap-2">

                  {result.skills?.map((skill) => (
                    <span
                      key={skill}
                      className="px-3.5 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-700 text-sm transition hover:bg-blue-50 hover:border-blue-200 hover:text-blue-700"
                    >
                      {skill}
                    </span>
                  ))}

                </div>

              </div>

            </div>

            {/* Questions */}
            <div className="bg-white border border-slate-200 rounded-2xl shadow-[0_12px_40px_rgba(15,23,42,0.05)] overflow-hidden">

              {/* Question Header */}
              <div className="p-7 md:p-9 border-b border-slate-100">

                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-5">

                  <div className="flex items-center gap-4">

                    <div className="w-11 h-11 rounded-xl bg-blue-600 text-white flex items-center justify-center text-lg font-bold">
                      ?
                    </div>

                    <div>

                      <h2 className="text-xl font-bold text-slate-900">
                        Generated Questions
                      </h2>

                      <p className="text-sm text-slate-400 mt-1">
                        Personalized for {jobTitle}
                      </p>

                    </div>

                  </div>

                  <div className="flex flex-wrap gap-2">

                    <span className="px-3 py-1.5 rounded-lg bg-blue-50 border border-blue-100 text-blue-700 text-xs font-semibold">
                      {questionTypeLabel[result.questionType] ||
                        questionTypeLabel[questionType]}
                    </span>

                    <span className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-600 text-xs">
                      {difficulty}
                    </span>

                    <span className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-600 text-xs">
                      {numberOfQuestions} Questions
                    </span>

                  </div>

                </div>

              </div>

              {/* Questions Body */}
              <div className="p-7 md:p-9">

                <div className="relative bg-slate-50 border border-slate-200 rounded-xl overflow-hidden">

                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500" />

                  <div className="p-6 md:p-7">

                    <pre className="whitespace-pre-wrap font-sans text-slate-700 leading-8 text-sm md:text-base">
                      {result.questions}
                    </pre>

                  </div>

                </div>

              </div>

            </div>

          </section>
        )}

        {/* Footer */}
        <footer className="text-center mt-10 pb-5">

          <div className="flex items-center justify-center gap-2 text-xs text-slate-400">

            <span>✦</span>

            <span>
              AI Interview Question Generator
            </span>

            <span>•</span>

            <span>
              Powered by Gemini AI
            </span>

          </div>

        </footer>

      </main>
    </div>
  );
}

export default App;

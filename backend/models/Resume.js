const mongoose = require("mongoose");

const resumeSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      default: ""
    },

    email: {
      type: String,
      default: ""
    },

    phone: {
      type: String,
      default: ""
    },

    skills: {
      type: [String],
      default: []
    },

    education: {
      type: [String],
      default: []
    },

    experience: {
      type: [String],
      default: []
    },

    projects: [
      {
        name: {
          type: String,
          default: ""
        },

        description: {
          type: String,
          default: ""
        }
      }
    ],

    resumeText: {
      type: String,
      default: ""
    }
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model("Resume", resumeSchema);
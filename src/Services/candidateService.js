const candidateProfile = {
  id: "candidate-1",
  name: "",
  email: "",
  phone: "",
  location: "",

  skills: [],

  resumeName: "",

  overallMatchScore: 0,
};

const applications = [
  {
    id: "application-1",
    jobId: "1",
    title: "Frontend Developer",
    company: "TechNova",
    location: "Hyderabad",
    matchScore: 92,
    status: "Interviewed",
  },
  {
    id: "application-2",
    jobId: "2",
    title: "AI/ML Engineer",
    company: "DataSphere",
    location: "Bengaluru",
    matchScore: 84,
    status: "Screened",
  },
  {
    id: "application-3",
    jobId: "3",
    title: "Full Stack Developer",
    company: "CloudWorks",
    location: "Pune",
    matchScore: 78,
    status: "Applied",
  },
];

export async function getCandidateProfile() {
  return candidateProfile;
}

export async function getCandidateApplications() {
  return applications;
}

export async function updateCandidateProfile(updatedProfile) {
  Object.assign(candidateProfile, updatedProfile);

  return candidateProfile;
}
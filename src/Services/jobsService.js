export const mockJobs = [
  {
    id: "1",
    title: "Frontend Developer",
    company: "TechNova",
    location: "Hyderabad",
    skills: ["React", "JavaScript", "CSS", "Tailwind"],
    matchScore: 92,
    description:
      "Build responsive web applications and reusable UI components for our recruitment platform.",
    requirements: [
      "Strong React and JavaScript fundamentals",
      "Experience with responsive UI development",
      "Knowledge of REST APIs and Git",
    ],
  },

  {
    id: "2",
    title: "AI/ML Engineer",
    company: "DataSphere",
    location: "Bengaluru",
    skills: ["Python", "Machine Learning", "TensorFlow", "SQL"],
    matchScore: 84,
    description:
      "Develop and integrate machine learning solutions for candidate matching and recruitment analytics.",
    requirements: [
      "Strong Python programming skills",
      "Understanding of machine learning concepts",
      "Experience with model APIs and data pipelines",
    ],
  },

  {
    id: "3",
    title: "Full Stack Developer",
    company: "CloudWorks",
    location: "Pune",
    skills: ["React", "Node.js", "MongoDB", "JavaScript"],
    matchScore: 78,
    description:
      "Work across frontend and backend services to deliver scalable recruitment workflows.",
    requirements: [
      "Experience with React and Node.js",
      "Working knowledge of databases",
      "Ability to build and consume REST APIs",
    ],
  },

  {
    id: "4",
    title: "Backend Developer",
    company: "InnovateLabs",
    location: "Hyderabad",
    skills: ["Node.js", "Python", "SQL", "REST API"],
    matchScore: 71,
    description:
      "Build reliable backend services that support recruitment, evaluation, and reporting workflows.",
    requirements: [
      "Strong backend development fundamentals",
      "Experience with REST APIs",
      "SQL/database knowledge",
    ],
  },
];

export async function getJobs() {
  /*
    Note: The backend endpoint is not yet implemented, so we are using mock data for now.

    Once the backend is ready, you can replace this with a fetch call to the API endpoint.
    const response = await fetch("/api/jobs");

    if (!response.ok) {
      throw new Error("Failed to load jobs");
    }

    return response.json();
  */

  return mockJobs;
}

export async function getJobById(id) {
  const jobs = await getJobs();

  return (
    jobs.find((job) => String(job.id) === String(id)) || null
  );
}
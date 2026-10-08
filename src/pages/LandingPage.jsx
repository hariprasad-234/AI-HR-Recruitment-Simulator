import { Link } from "react-router-dom"
import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  FileSearch,
  MessageSquareText,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
  Zap,
} from "lucide-react"
import "./LandingPage.css"

const features = [
  {
    icon: FileSearch,
    title: "AI Resume Analysis",
    text: "Turn resumes into structured candidate insights with faster, consistent screening.",
  },
  {
    icon: Target,
    title: "Smart Job Matching",
    text: "Match candidates to roles using skills, experience, location, and relevant signals.",
  },
  {
    icon: Users,
    title: "Candidate Ranking",
    text: "Compare applicants at a glance and focus your attention on the strongest matches.",
  },
  {
    icon: MessageSquareText,
    title: "HR Copilot",
    text: "Ask natural-language questions and quickly explore your recruitment pipeline.",
  },
]

const steps = [
  ["01", "Upload resumes", "Bring candidate resumes into one simple workflow."],
  ["02", "Let AI evaluate", "Analyze skills and candidate-job relevance in seconds."],
  ["03", "Shortlist smarter", "Review rankings and move the right candidates forward."],
]

export default function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-nav">
        <div className="landing-container landing-nav-inner">
          <Link to="/" className="landing-logo" aria-label="AI-HR-Recruitment-Simulator home">
            <span className="landing-logo-mark"><BrainCircuit size={19} /></span>
            <span>AI-HR-Recruitment-Simulator</span>
          </Link>

          <nav className="landing-links" aria-label="Landing page navigation">
            <a href="#features">Features</a>
            <a href="#how-it-works">How it works</a>
            <a href="#about">About</a>
          </nav>

          <div className="landing-actions">
            <Link to="/login" className="landing-login">Log in</Link>
            <Link to="/signup" className="landing-nav-cta">Get started <ArrowRight size={16} /></Link>
          </div>
        </div>
      </header>

      <main>
        <section className="landing-hero">
          <div className="landing-hero-glow landing-hero-glow-one" />
          <div className="landing-hero-glow landing-hero-glow-two" />
          <div className="landing-container landing-hero-grid">
            <div className="landing-hero-copy">
              <div className="landing-eyebrow"><Sparkles size={15} /> AI-powered recruitment</div>
              <h1>Hire smarter.<br /><span>Move faster.</span></h1>
              <p>
                An intelligent recruitment platform that helps HR teams analyze resumes,
                match candidates to jobs, rank talent, and make better hiring decisions.
              </p>
              <div className="landing-hero-actions">
                <Link to="/signup" className="landing-primary-btn">Start hiring smarter <ArrowRight size={18} /></Link>
                <a href="#features" className="landing-secondary-btn">Explore features</a>
              </div>
              <div className="landing-trust-row">
                <span><CheckCircle2 size={16} /> Faster screening</span>
                <span><CheckCircle2 size={16} /> Data-driven insights</span>
                <span><CheckCircle2 size={16} /> Recruiter focused</span>
              </div>
            </div>

            <div className="landing-product-wrap" aria-label="Recruitment dashboard preview">
              <div className="landing-product-card">
                <div className="product-topbar">
                  <div>
                    <p className="product-kicker">Recruiter workspace</p>
                    <h3>Candidate insights</h3>
                  </div>
                  <div className="product-ai"><Sparkles size={14} /> AI active</div>
                </div>
                <div className="product-stats">
                  <div><strong>248</strong><span>Applications</span></div>
                  <div><strong>86</strong><span>Shortlisted</span></div>
                  <div><strong>34</strong><span>Top matches</span></div>
                </div>
                <div className="product-match-head"><span>Top candidate matches</span><span>Match</span></div>
                {[
                  ["GS", "Sanvitha", "Senior React Developer", "94%"],
                  ["AL", "Lahari", "ML Engineer", "91%"],
                  ["PB", "Bindhu", "Full Stack Developer", "88%"],
                  ["GG","Gopi Nath","Software Developer","72%"],
                ].map(([initials, name, role, score]) => (
                  <div className="product-candidate" key={name}>
                    <div className="candidate-avatar">{initials}</div>
                    <div className="candidate-info"><strong>{name}</strong><span>{role}</span></div>
                    <div className="candidate-score">{score}</div>
                  </div>
                ))}
                <div className="product-insight"><Zap size={16} /><span><strong>AI insight:</strong> 12 candidates closely match the role requirements.</span></div>
              </div>
              <div className="floating-card floating-card-one"><div className="floating-icon"><ShieldCheck size={17} /></div><div><strong>Consistent screening</strong><span>AI-assisted evaluation</span></div></div>
              <div className="floating-card floating-card-two"><div className="floating-icon"><Target size={17} /></div><div><strong>94% match</strong><span>Strong role fit detected</span></div></div>
            </div>
          </div>
        </section>

        <section className="landing-section landing-features" id="features">
          <div className="landing-container">
            <div className="section-heading">
              <div className="landing-eyebrow">Built for modern HR teams</div>
              <h2>Everything you need to recruit with confidence.</h2>
              <p>Bring screening, matching, ranking, and recruiter assistance into one focused workspace.</p>
            </div>
            <div className="feature-grid">
              {features.map(({ icon: Icon, title, text }) => (
                <article className="feature-card" key={title}>
                  <div className="feature-icon"><Icon size={22} /></div>
                  <h3>{title}</h3>
                  <p>{text}</p>
                  <span className="feature-arrow"><ArrowRight size={17} /></span>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="landing-section landing-work" id="how-it-works">
          <div className="landing-container work-grid">
            <div className="work-copy">
              <div className="landing-eyebrow">Simple workflow</div>
              <h2>From resume to shortlist in three steps.</h2>
              <p>Spend less time sorting through applications and more time having meaningful conversations with candidates.</p>
              <Link to="/signup" className="landing-text-link">Try the simulator <ArrowRight size={17} /></Link>
            </div>
            <div className="steps-list">
              {steps.map(([number, title, text]) => (
                <div className="step" key={number}>
                  <span className="step-number">{number}</span>
                  <div><h3>{title}</h3><p>{text}</p></div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="landing-about" id="about">
          <div className="landing-container about-card">
            <div>
              <div className="landing-eyebrow">The mission</div>
              <h2>Make hiring smarter, faster, and more human.</h2>
            </div>
            <p>AI-HR-Recruitment-Simulator combines practical recruitment workflows with AI-assisted insights so recruiters can focus on the people behind every application.</p>
          </div>
        </section>

        <section className="landing-cta">
          <div className="landing-container cta-inner">
            <div><div className="landing-eyebrow">Ready to get started?</div><h2>Build your smarter hiring workflow.</h2></div>
            <Link to="/signup" className="landing-primary-btn">Create your account <ArrowRight size={18} /></Link>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="landing-container footer-inner">
          <Link to="/" className="landing-logo"><span className="landing-logo-mark"><BrainCircuit size={18} /></span><span>AI-HR-Recruitment-Simulator</span></Link>
          <p>AI-HR Recruitment Simulator</p>
          <span>© 2026 AI-HR-Recruitment-Simulator</span>
        </div>
      </footer>
    </div>
  )
}

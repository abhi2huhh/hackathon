import { Suspense, lazy } from "react";
import { Link } from "react-router-dom";
import { motion } from "motion/react";
import { Button } from "../components/ui/Button";
import { fadeUp, stagger } from "../lib/animations";

const KnowledgeCore = lazy(() =>
  import("../components/3d/KnowledgeCore").then((m) => ({ default: m.KnowledgeCore })),
);

const modules = [
  { title: "ATS atelier", body: "Estimate role compatibility and surface missing skills from a real resume parse." },
  { title: "Line-limited summaries", body: "TF-IDF extractive compression, with optional abstractive generation when a key is set." },
  { title: "Document Q&A", body: "Chunk, retrieve, and ground answers in the files you upload." },
  { title: "Roadmaps", body: "Beginner to advanced sequences with progress you can actually save." },
  { title: "Resource library", body: "Curated official docs, papers, and courses — searchable and bookmarkable." },
];

export default function LandingPage() {
  return (
    <div>
      <motion.section variants={stagger} initial="hidden" animate="show" className="grid gap-12 lg:grid-cols-[1.1fr_0.9fr]">
        <div>
          <motion.p variants={fadeUp} className="text-xs uppercase tracking-[0.28em] text-bronze">
            One atelier. Four crafts.
          </motion.p>
          <motion.h1 variants={fadeUp} className="mt-4 font-display text-5xl leading-[1.05] md:text-7xl">
            Learn, research, and prepare for work in a single intelligent room.
          </motion.h1>
          <motion.p variants={fadeUp} className="mt-6 max-w-xl text-lg text-mute">
            InnoLearn unifies resume analysis, document intelligence, structured roadmaps, and a technical library —
            so study and career preparation stop living in five disconnected tabs.
          </motion.p>
          <motion.div variants={fadeUp} className="mt-8 flex flex-wrap gap-3">
            <Link to="/register"><Button>Explore the platform</Button></Link>
            <Link to="/ats"><Button variant="line">Analyze your resume</Button></Link>
            <Link to="/rag"><Button variant="ghost">Ask your documents</Button></Link>
          </motion.div>
        </div>
        <Suspense fallback={<div className="h-[380px] rounded-[2rem] bg-panel" />}>
          <KnowledgeCore />
        </Suspense>
      </motion.section>

      <section className="mt-24 grid gap-6 md:grid-cols-2">
        {modules.map((item) => (
          <article key={item.title} className="rounded-[1.75rem] border border-line bg-panel/80 p-8">
            <h2 className="font-display text-3xl">{item.title}</h2>
            <p className="mt-3 text-mute">{item.body}</p>
          </article>
        ))}
      </section>

      <section className="mt-24 rounded-[2rem] border border-accent/30 bg-accent text-ink px-8 py-14">
        <h2 className="font-display text-4xl md:text-5xl">A workflow with a spine</h2>
        <ol className="mt-8 grid gap-4 md:grid-cols-4">
          {["Choose a craft", "Bring a document", "Let models retrieve and score", "Track the path you keep"].map((step, i) => (
            <li key={step} className="text-lg">
              <span className="block text-xs uppercase tracking-[0.2em] opacity-70">0{i + 1}</span>
              {step}
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}

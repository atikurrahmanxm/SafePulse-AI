import React, { useCallback, useEffect, useState } from "react";
import { Award, BookOpen, CheckCircle2, FlaskConical, XCircle } from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError } from "../lib/api";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  Skeleton,
} from "../components/ui/Primitives";

interface AwarenessData {
  lessons: Array<{
    id: string;
    topic: string;
    title: string;
    duration_min: number;
    summary: string;
    tips: string[];
  }>;
  simulations: Array<{
    id: string;
    is_training_simulation: boolean;
    simulation_badge: string;
    channel: string;
    title: string;
    sample_text: string;
    red_flags: string[];
  }>;
  quizzes: Array<{
    slug: string;
    title: string;
    topic: string;
    difficulty: string;
    questions: Array<{
      id: string;
      prompt: string;
      options: string[];
    }>;
  }>;
  progress: {
    completed_quizzes: number;
    total_quizzes: number;
    completion_percent: number;
    average_score: number;
    best_by_slug: Record<string, number>;
  };
}

interface QuizResult {
  quiz_slug: string;
  quiz_title: string;
  score: number;
  total_questions: number;
  percentage: number;
  answers_summary: Array<{
    question_id: string;
    prompt: string;
    chosen_index: number;
    correct_index: number;
    is_correct: boolean;
    explanation: string;
  }>;
}

export function AwarenessPage() {
  const { language, t } = useLanguage();
  const [data, setData] = useState<AwarenessData | null>(null);
  const [activeQuizSlug, setActiveQuizSlug] = useState<string>("phishing-defense-essentials");
  const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({});
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchOverview = useCallback(() => {
    setLoading(true);
    apiRequest<AwarenessData>(`/api/awareness/overview?language=${language}`)
      .then((res) => {
        setData(res);
        setError(null);
      })
      .catch((err) => setError(err.message || "Failed to load awareness content."))
      .finally(() => setLoading(false));
  }, [language]);

  useEffect(() => {
    fetchOverview();
  }, [fetchOverview]);

  const activeQuiz = data?.quizzes.find((q) => q.slug === activeQuizSlug) || data?.quizzes[0];

  const handleSubmitQuiz = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeQuiz) return;
    setError(null);
    setSubmitting(true);
    try {
      const res = await apiRequest<QuizResult>(
        `/api/awareness/quizzes/${activeQuiz.slug}/submit?language=${language}`,
        {
          method: "POST",
          body: JSON.stringify({ answers: quizAnswers }),
        }
      );
      setQuizResult(res);
      fetchOverview();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not grade quiz.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading && !data) {
    return <Skeleton className="h-96" />;
  }

  if (!data) {
    return <ErrorBanner message={error || "Awareness content unavailable."} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-50">{t.awareness.title}</h2>
          <p className="mt-1 text-sm text-slate-400">{t.awareness.subtitle}</p>
        </div>
        <div className="flex items-center gap-3 rounded-xl border border-slate-800 bg-[#141F35] px-4 py-2.5 text-xs">
          <Award className="h-5 w-5 text-[#06B6D4]" aria-hidden="true" />
          <div>
            <div className="font-semibold text-slate-100">
              Progress: {data.progress.completed_quizzes}/{data.progress.total_quizzes} Quizzes (
              {data.progress.completion_percent}%)
            </div>
            <div className="text-slate-400">Average Best Score: {data.progress.average_score}%</div>
          </div>
        </div>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {/* Micro-Lessons */}
      <div className="grid gap-4 md:grid-cols-2">
        {data.lessons.map((lesson) => (
          <Card key={lesson.id}>
            <CardHeader>
              <div className="flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
                <span className="text-xs font-semibold text-[#06B6D4]">{lesson.topic}</span>
              </div>
              <span className="text-[11px] text-slate-400">{lesson.duration_min} min read</span>
            </CardHeader>
            <CardContent className="space-y-2.5">
              <h3 className="text-sm font-semibold text-slate-100">{lesson.title}</h3>
              <p className="text-xs leading-relaxed text-slate-400">{lesson.summary}</p>
              <ul className="space-y-1.5 pt-1 text-xs text-slate-200">
                {lesson.tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-400" aria-hidden="true" />
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Clearly Labeled Simulated Phishing Examples */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <FlaskConical className="h-4 w-4 text-amber-400" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-slate-100">
              Simulated Phishing Training Examples
            </h3>
          </div>
        </CardHeader>
        <CardContent className="grid gap-4 lg:grid-cols-3">
          {data.simulations.map((sim) => (
            <div
              key={sim.id}
              className="flex flex-col justify-between rounded-xl border border-amber-500/30 bg-[#10182B] p-4"
            >
              <div>
                <span className="inline-block rounded-full border border-amber-500/40 bg-amber-500/15 px-2.5 py-0.5 text-[10px] font-semibold text-amber-300">
                  {t.awareness.simBadge}
                </span>
                <h4 className="mt-2.5 text-xs font-semibold text-slate-100">
                  {sim.title} ({sim.channel})
                </h4>
                <blockquote className="mt-2 rounded-lg border border-slate-800 bg-[#080D1B] p-2.5 font-mono text-[11px] text-slate-300">
                  "{sim.sample_text}"
                </blockquote>
                <ul className="mt-3 space-y-1 text-xs text-slate-400">
                  {sim.red_flags.map((rf, i) => (
                    <li key={i}>• {rf}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Interactive Quizzes */}
      {activeQuiz && (
        <Card>
          <CardHeader>
            <div className="flex flex-wrap items-center gap-2">
              {data.quizzes.map((q) => (
                <button
                  key={q.slug}
                  type="button"
                  onClick={() => {
                    setActiveQuizSlug(q.slug);
                    setQuizAnswers({});
                    setQuizResult(null);
                  }}
                  className={`rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
                    activeQuiz.slug === q.slug
                      ? "bg-[#6366F1] text-white"
                      : "bg-[#10182B] text-slate-300 hover:text-white"
                  }`}
                >
                  {q.title}
                  {data.progress.best_by_slug[q.slug] !== undefined &&
                    ` (${data.progress.best_by_slug[q.slug]}%)`}
                </button>
              ))}
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmitQuiz} className="space-y-4">
              {activeQuiz.questions.map((qq, idx) => (
                <fieldset
                  key={qq.id}
                  className="rounded-xl border border-slate-800 bg-[#10182B] p-4"
                >
                  <legend className="px-1 text-xs font-semibold text-[#06B6D4]">
                    Question {idx + 1}
                  </legend>
                  <p className="mt-1 text-sm font-medium text-slate-100">{qq.prompt}</p>
                  <div className="mt-3 space-y-2">
                    {qq.options.map((opt, optIdx) => (
                      <label
                        key={optIdx}
                        className={`flex cursor-pointer items-center gap-2.5 rounded-lg border px-3 py-2 text-xs transition-colors ${
                          quizAnswers[qq.id] === optIdx
                            ? "border-[#6366F1] bg-[#6366F1]/20 text-white"
                            : "border-slate-800 bg-[#080D1B] text-slate-300 hover:border-slate-700"
                        }`}
                      >
                        <input
                          type="radio"
                          name={`quiz-${qq.id}`}
                          checked={quizAnswers[qq.id] === optIdx}
                          onChange={() =>
                            setQuizAnswers((prev) => ({ ...prev, [qq.id]: optIdx }))
                          }
                          required
                          className="accent-[#6366F1]"
                        />
                        <span>{opt}</span>
                      </label>
                    ))}
                  </div>
                </fieldset>
              ))}

              <Button type="submit" size="lg" disabled={submitting}>
                {submitting ? "Grading..." : "Submit Quiz Answers"}
              </Button>
            </form>

            {quizResult && (
              <div className="mt-6 space-y-3 rounded-xl border border-indigo-500/35 bg-[#10182B] p-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-bold text-slate-50">
                    Result: {quizResult.score}/{quizResult.total_questions} ({quizResult.percentage}%)
                  </div>
                </div>
                {quizResult.answers_summary.map((ans) => (
                  <div
                    key={ans.question_id}
                    className="rounded-lg border border-slate-800 bg-[#080D1B] p-3 text-xs"
                  >
                    <div className="flex items-center gap-2 font-semibold">
                      {ans.is_correct ? (
                        <CheckCircle2 className="h-4 w-4 text-emerald-400" aria-hidden="true" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-400" aria-hidden="true" />
                      )}
                      <span className={ans.is_correct ? "text-emerald-300" : "text-red-300"}>
                        {ans.is_correct ? "Correct" : "Needs Review"}
                      </span>
                    </div>
                    <p className="mt-1 text-slate-300">{ans.explanation}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}


import React, { useCallback, useEffect, useState } from "react";
import {
  CheckSquare,
  Clock,
  Download,
  ExternalLink,
  FileWarning,
  Info,
  MessageSquarePlus,
  PhoneCall,
  Plus,
  Save,
  Square,
  UserCheck,
} from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import { formatTimestamp } from "../lib/utils";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  RiskBadge,
  Skeleton,
} from "../components/ui/Primitives";

interface ScenarioOption {
  key: string;
  title: string;
  severity: string;
  summary: string;
  steps_count: number;
}

interface ChecklistItem {
  id: number;
  phase: string;
  title: string;
  guidance: string;
  is_completed: boolean;
  sort_order: number;
}

interface TimelineNote {
  id: number;
  author_name: string;
  event_type: string;
  content: string;
  created_at: string;
}

interface IncidentRecord {
  id: number;
  scenario_key: string;
  title: string;
  severity: string;
  status: string;
  assigned_to?: string | null;
  resolution_summary?: string | null;
  notes?: string | null;
  progress_percent: number;
  completed_count: number;
  total_count: number;
  is_demo_sample: boolean;
  created_at: string;
  updated_at: string;
  checklist_items: ChecklistItem[];
  timeline_notes?: TimelineNote[];
}

export function IncidentsPage() {
  const { language, t } = useLanguage();
  const [scenarios, setScenarios] = useState<ScenarioOption[]>([]);
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [newScenarioKey, setNewScenarioKey] = useState("phishing_link_clicked");
  const [assignedToInput, setAssignedToInput] = useState("");
  const [notes, setNotes] = useState("");
  const [editStatus, setEditStatus] = useState("in_progress");
  const [editSeverity, setEditSeverity] = useState("High");
  const [editAssignedTo, setEditAssignedTo] = useState("");
  const [editResolution, setEditResolution] = useState("");
  const [savingWorkflow, setSavingWorkflow] = useState(false);
  const [noteInput, setNoteInput] = useState("");
  const [addingNote, setAddingNote] = useState(false);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [scenRes, incRes] = await Promise.all([
        apiRequest<{ scenarios: ScenarioOption[] }>(`/api/incidents/scenarios?language=${language}`),
        apiRequest<IncidentRecord[]>("/api/incidents"),
      ]);
      setScenarios(scenRes.scenarios);
      setIncidents(incRes);
      if (incRes.length > 0) {
        setSelectedId((prev) => (prev && incRes.some((i) => i.id === prev) ? prev : incRes[0].id));
      }
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load incidents.");
    } finally {
      setLoading(false);
    }
  }, [language]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setCreating(true);
    try {
      const created = await apiRequest<IncidentRecord>("/api/incidents", {
        method: "POST",
        body: JSON.stringify({
          scenario_key: newScenarioKey,
          assigned_to: assignedToInput.trim() || null,
          notes: notes.trim() || null,
          language,
        }),
      });
      setIncidents((prev) => [created, ...prev]);
      setSelectedId(created.id);
      setAssignedToInput("");
      setNotes("");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not open incident playbook.");
    } finally {
      setCreating(false);
    }
  };

  const handleToggleItem = async (incidentId: number, item: ChecklistItem) => {
    try {
      const updated = await apiRequest<IncidentRecord>(
        `/api/incidents/${incidentId}/items/${item.id}`,
        {
          method: "PATCH",
          body: JSON.stringify({ is_completed: !item.is_completed }),
        }
      );
      setIncidents((prev) => prev.map((inc) => (inc.id === updated.id ? updated : inc)));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not update checklist item.");
    }
  };

  const selectedIncident = incidents.find((i) => i.id === selectedId) || null;

  useEffect(() => {
    if (selectedIncident) {
      setEditStatus(selectedIncident.status);
      setEditSeverity(selectedIncident.severity);
      setEditAssignedTo(selectedIncident.assigned_to || "");
      setEditResolution(selectedIncident.resolution_summary || "");
    }
  }, [selectedIncident?.id, selectedIncident?.status, selectedIncident?.severity, selectedIncident?.assigned_to, selectedIncident?.resolution_summary]);

  const handleSaveWorkflow = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIncident) return;
    setSavingWorkflow(true);
    setError(null);
    try {
      const updated = await apiRequest<IncidentRecord>(`/api/incidents/${selectedIncident.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          status: editStatus,
          severity: editSeverity,
          assigned_to: editAssignedTo.trim() || null,
          resolution_summary: editResolution.trim() || null,
        }),
      });
      setIncidents((prev) => prev.map((inc) => (inc.id === updated.id ? updated : inc)));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not update incident workflow.");
    } finally {
      setSavingWorkflow(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedIncident || noteInput.trim().length < 3) return;
    setAddingNote(true);
    setError(null);
    try {
      const updated = await apiRequest<IncidentRecord>(`/api/incidents/${selectedIncident.id}/notes`, {
        method: "POST",
        body: JSON.stringify({ content: noteInput.trim() }),
      });
      setIncidents((prev) => prev.map((inc) => (inc.id === updated.id ? updated : inc)));
      setNoteInput("");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not append timeline note.");
    } finally {
      setAddingNote(false);
    }
  };

  if (loading) {
    return <Skeleton className="h-96" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-slate-50">{t.incidents.title}</h2>
        <p className="mt-1 text-sm text-slate-400">{t.incidents.subtitle}</p>
      </div>

      <div className="flex items-start gap-2.5 rounded-xl border border-amber-500/35 bg-amber-500/10 p-3.5 text-xs text-amber-200">
        <Info className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" aria-hidden="true" />
        <span>{t.incidents.disclaimer}</span>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      <div className="grid gap-6 lg:grid-cols-12">
        {/* Left: Start Playbook + Active Incident List */}
        <div className="space-y-5 lg:col-span-5">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <FileWarning className="h-4 w-4 text-red-400" aria-hidden="true" />
                <h3 className="text-sm font-semibold text-slate-100">Start Guided Response</h3>
              </div>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreate} className="space-y-3.5">
                <div>
                  <label htmlFor="inc-scenario" className="block text-xs font-medium text-slate-300">
                    Select Incident Scenario
                  </label>
                  <select
                    id="inc-scenario"
                    value={newScenarioKey}
                    onChange={(e) => setNewScenarioKey(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  >
                    {scenarios.map((s) => (
                      <option key={s.key} value={s.key}>
                        [{s.severity}] {s.title}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="inc-assignee" className="block text-xs font-medium text-slate-300">
                    Assigned Responder (Optional)
                  </label>
                  <input
                    id="inc-assignee"
                    type="text"
                    value={assignedToInput}
                    onChange={(e) => setAssignedToInput(e.target.value)}
                    placeholder="e.g., Rahul Sharma (Manager)"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                  />
                </div>

                <div>
                  <label htmlFor="inc-notes" className="block text-xs font-medium text-slate-300">
                    What Happened? (Optional Context)
                  </label>
                  <textarea
                    id="inc-notes"
                    rows={3}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="e.g., Counter staff clicked an SMS KYC link on the billing browser..."
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] p-2.5 text-xs text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                  />
                </div>

                <Button type="submit" className="w-full" disabled={creating}>
                  <Plus className="h-4 w-4" aria-hidden="true" />
                  <span>{creating ? "Opening..." : t.incidents.startBtn}</span>
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Your Incident Playbooks ({incidents.length})</h3>
            </CardHeader>
            <CardContent className="space-y-2.5">
              {incidents.length === 0 ? (
                <p className="text-xs text-slate-400">No incident playbooks opened yet.</p>
              ) : (
                incidents.map((inc) => (
                  <button
                    key={inc.id}
                    type="button"
                    onClick={() => setSelectedId(inc.id)}
                    className={`w-full rounded-xl border p-3.5 text-left transition-colors ${
                      selectedId === inc.id
                        ? "border-[#6366F1] bg-[#6366F1]/15"
                        : "border-slate-800 bg-[#10182B] hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-semibold text-slate-100">{inc.title}</span>
                      <RiskBadge category={inc.severity} />
                    </div>
                    <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-full bg-[#06B6D4] transition-all"
                        style={{ width: `${inc.progress_percent}%` }}
                      />
                    </div>
                    <div className="mt-1.5 flex items-center justify-between text-[11px] text-slate-400">
                      <span>
                        {inc.completed_count}/{inc.total_count} steps ({inc.progress_percent}%)
                      </span>
                      <span className="capitalize">{inc.status.replace("_", " ")}</span>
                    </div>
                  </button>
                ))
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right: Active Checklist */}
        <Card className="lg:col-span-7">
          <CardHeader>
            <div>
              <h3 className="text-sm font-semibold text-slate-100">
                {selectedIncident ? selectedIncident.title : "Interactive Response Checklist"}
              </h3>
              {selectedIncident && (
                <p className="mt-0.5 text-xs text-slate-400">
                  Opened {formatTimestamp(selectedIncident.created_at)} • Progress{" "}
                  {selectedIncident.progress_percent}%
                </p>
              )}
            </div>
            {selectedIncident && (
              <Button
                size="sm"
                variant="secondary"
                onClick={async () => {
                  try {
                    await downloadPdfReport(
                      `/api/incidents/${selectedIncident.id}/report.pdf`,
                      `cybershield-incident-${selectedIncident.id}.pdf`
                    );
                  } catch (err) {
                    setError(
                      err instanceof ApiError
                        ? err.message
                        : "Could not download incident PDF checklist."
                    );
                  }
                }}
              >
                <Download className="h-3.5 w-3.5" aria-hidden="true" />
                <span>PDF Checklist</span>
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {!selectedIncident ? (
              <p className="py-12 text-center text-xs text-slate-400">
                Select or start an incident scenario on the left to view your 6-phase guided checklist.
              </p>
            ) : (
              <div className="space-y-3">
                {["High", "Critical"].includes(selectedIncident.severity) && (
                  <div className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-red-500/35 bg-red-500/10 p-3.5 text-xs text-red-100">
                    <div className="flex items-start gap-2.5">
                      <PhoneCall className="mt-0.5 h-4 w-4 shrink-0 text-red-400" aria-hidden="true" />
                      <div>
                        <span className="font-semibold">Urgent India Financial/Cyber Escalation:</span>{" "}
                        {language === "bn"
                          ? "টাকা বা UPI প্রতারণা হলে অবিলম্বে ১৯৩০ নম্বরে কল করুন এবং cybercrime.gov.in-এ রিপোর্ট করুন।"
                          : "For financial or UPI fraud, call India Helpline 1930 immediately (Golden Hour) and file a report at cybercrime.gov.in."}
                      </div>
                    </div>
                    <a
                      href="https://cybercrime.gov.in"
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 rounded-lg border border-red-400/40 bg-red-500/20 px-2.5 py-1 font-medium text-red-100 hover:bg-red-500/30"
                    >
                      <span>cybercrime.gov.in</span>
                      <ExternalLink className="h-3 w-3" aria-hidden="true" />
                    </a>
                  </div>
                )}
                {selectedIncident.notes && (
                  <div className="rounded-lg border border-slate-800 bg-[#10182B] p-3 text-xs text-slate-300">
                    <span className="font-semibold text-slate-100">Initial Notes:</span> {selectedIncident.notes}
                  </div>
                )}

                {/* Workflow Assignment, Status & Resolution Panel */}
                <form
                  onSubmit={handleSaveWorkflow}
                  className="rounded-xl border border-slate-800 bg-[#10182B] p-3.5 space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-200">
                      <UserCheck className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
                      <span>Response Ownership & Containment Status</span>
                    </div>
                    <Button type="submit" size="sm" variant="secondary" disabled={savingWorkflow}>
                      <Save className="h-3.5 w-3.5" aria-hidden="true" />
                      <span>{savingWorkflow ? "Saving..." : "Save Status"}</span>
                    </Button>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-3">
                    <div>
                      <label htmlFor="wf-status" className="block text-[11px] text-slate-400">
                        Status
                      </label>
                      <select
                        id="wf-status"
                        value={editStatus}
                        onChange={(e) => setEditStatus(e.target.value)}
                        className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-1.5 text-xs text-white"
                      >
                        <option value="in_progress">In Progress</option>
                        <option value="contained">Contained</option>
                        <option value="resolved">Resolved</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="wf-severity" className="block text-[11px] text-slate-400">
                        Severity
                      </label>
                      <select
                        id="wf-severity"
                        value={editSeverity}
                        onChange={(e) => setEditSeverity(e.target.value)}
                        className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-1.5 text-xs text-white"
                      >
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Critical">Critical</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="wf-assignee" className="block text-[11px] text-slate-400">
                        Assigned Person
                      </label>
                      <input
                        id="wf-assignee"
                        type="text"
                        value={editAssignedTo}
                        onChange={(e) => setEditAssignedTo(e.target.value)}
                        placeholder="Assign responder..."
                        className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-1.5 text-xs text-white"
                      />
                    </div>
                  </div>
                  <div>
                    <label htmlFor="wf-resolution" className="block text-[11px] text-slate-400">
                      Resolution / Containment Summary
                    </label>
                    <input
                      id="wf-resolution"
                      type="text"
                      value={editResolution}
                      onChange={(e) => setEditResolution(e.target.value)}
                      placeholder="e.g., Passwords rotated, active sessions revoked, 1930 reference logged..."
                      className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-1.5 text-xs text-white"
                    />
                  </div>
                </form>

                {selectedIncident.checklist_items.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => handleToggleItem(selectedIncident.id, item)}
                    className={`flex w-full items-start gap-3 rounded-xl border p-4 text-left transition-colors ${
                      item.is_completed
                        ? "border-emerald-500/35 bg-emerald-500/10"
                        : "border-slate-800 bg-[#10182B] hover:border-slate-700"
                    }`}
                  >
                    {item.is_completed ? (
                      <CheckSquare className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" aria-hidden="true" />
                    ) : (
                      <Square className="mt-0.5 h-5 w-5 shrink-0 text-slate-400" aria-hidden="true" />
                    )}
                    <div className="min-w-0 flex-1">
                      <div className="font-mono text-[11px] uppercase tracking-wider text-[#06B6D4]">
                        {item.phase}
                      </div>
                      <div
                        className={`mt-0.5 text-sm font-semibold ${
                          item.is_completed ? "line-through text-slate-400" : "text-slate-100"
                        }`}
                      >
                        {item.title}
                      </div>
                      <p className="mt-1 text-xs leading-relaxed text-slate-300">{item.guidance}</p>
                    </div>
                  </button>
                ))}

                {/* Evidence & Activity Timeline */}
                <div className="rounded-xl border border-slate-800 bg-[#10182B] p-4 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-semibold text-slate-200">
                    <Clock className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
                    <span>Evidence & Incident Activity Timeline</span>
                  </div>
                  <form onSubmit={handleAddNote} className="flex flex-wrap gap-2">
                    <input
                      type="text"
                      value={noteInput}
                      onChange={(e) => setNoteInput(e.target.value)}
                      placeholder="Log evidence note, transaction ref, or action taken (min 3 chars)..."
                      className="flex-1 min-w-[200px] rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-1.5 text-xs text-white placeholder:text-slate-500"
                    />
                    <Button type="submit" size="sm" disabled={addingNote || noteInput.trim().length < 3}>
                      <MessageSquarePlus className="h-3.5 w-3.5" aria-hidden="true" />
                      <span>{addingNote ? "Adding..." : "Add Note"}</span>
                    </Button>
                  </form>
                  <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                    {Array.isArray(selectedIncident.timeline_notes) &&
                    selectedIncident.timeline_notes.length > 0 ? (
                      selectedIncident.timeline_notes.map((ev) => (
                        <div
                          key={ev.id}
                          className="rounded-lg border border-slate-800/90 bg-[#080D1B] px-3 py-2 text-xs"
                        >
                          <div className="flex items-center justify-between gap-2 text-[10px] text-slate-400">
                            <span className="font-semibold text-cyan-300">
                              {ev.author_name} • {ev.event_type}
                            </span>
                            <span>{formatTimestamp(ev.created_at)}</span>
                          </div>
                          <p className="mt-1 text-slate-200">{ev.content}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-[11px] text-slate-400">No timeline events recorded yet.</p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


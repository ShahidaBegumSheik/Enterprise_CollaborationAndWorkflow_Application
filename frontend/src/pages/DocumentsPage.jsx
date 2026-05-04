import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import { getDocuments, getDocumentDownloadUrl, uploadDocument, downloadDocument } from "../api/documentApi";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, []);

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load documents");
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      await uploadDocument(file);
      setFile(null);
      e.target.reset();
      loadDocuments();
    } catch (err) {
      console.error(err);
      setError("Upload failed. Check backend document service file saving fields.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="rounded-4xl bg-linear-to-r from-cyan-600 to-blue-600 p-8 text-white shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-white/75">Document Management</p>
          <h2 className="mt-3 text-3xl font-black">Upload, Version and Download files</h2>
        </div>

        {error && <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">{error}</div>}

        <form onSubmit={handleUpload} className="rounded-3xl border-2 border-dashed border-sky-200 bg-white p-8 text-center shadow-xl">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl bg-sky-100 text-3xl">📁</div>
          <h3 className="mt-4 text-xl font-black text-slate-900">Upload Document</h3>
          <p className="mt-2 text-sm text-slate-500">Attach files related to tasks or approval requests.</p>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mt-6 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 md:max-w-md" />
          <button disabled={loading || !file} className="mt-5 rounded-2xl bg-sky-600 px-6 py-3 font-black text-white shadow-lg shadow-sky-600/25 hover:bg-sky-700 disabled:opacity-50">
            {loading ? "Uploading..." : "Upload File"}
          </button>
        </form>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {documents.map((doc) => (
            <div key={doc.id} className="rounded-3xl bg-white p-5 shadow-xl">
              <div className="flex items-start gap-4">
                <div className="rounded-2xl bg-sky-100 p-3 text-2xl">📄</div>
                <div className="min-w-0 flex-1">
                  <h3 className="truncate font-black text-slate-900">{doc.original_name}</h3>
                  <p className="mt-1 text-sm font-semibold text-slate-500">Version {doc.version}</p>
                  <p className="mt-1 text-xs text-slate-400">Uploaded: {doc.created_at ? new Date(doc.created_at).toLocaleDateString() : "N/A"}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => downloadDocument(doc.id, doc.original_name)}
                className="mt-3 inline-flex w-full justify-center rounded-2xl bg-sky-600 px-4 py-2 font-black text-white hover:bg-sky-700"
              >
                Download
              </button>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}

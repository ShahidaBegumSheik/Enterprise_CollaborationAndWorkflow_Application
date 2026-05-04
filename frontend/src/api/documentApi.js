import api from "./client";

export async function uploadDocument(file, taskId = null, approvalRequestId = null) {
  const formData = new FormData();
  formData.append("file", file);

  if (taskId && Number(taskId) > 0) {
    formData.append("task_id", Number(taskId));
  }

  if (approvalRequestId && Number(approvalRequestId) > 0) {
    formData.append("approval_request_id", Number(approvalRequestId));
  }

  const { data } = await api.post("/documents/upload", formData);

  return data;
}


export async function getDocuments(params = {}) {
    const { data } = await api.get("/documents", { params });
    return data;
}

export async function getDocumentById(documentId) {
    const { data } = await api.get(`/documents/${documentId}`);
    return data;
}

export async function deleteDocument(documentId) {
    const { data } = await api.delete(`/documents/${documentId}`);
    return data;
}

export function getDocumentDownloadUrl(documentId) {
    const base = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api/v1";
    return `${base}/documents/${documentId}/download`;
}


export async function downloadDocument(documentId, filename = "document") {
    const response = await api.get(`/documents/${documentId}/download`, {
        responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");

    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    link.remove();
    window.URL.revokeObjectURL(url);
} 

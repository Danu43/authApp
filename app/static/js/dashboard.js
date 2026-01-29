console.log("dashboard.js loaded");

// 1️⃣ Read logged-in user
const user = JSON.parse(localStorage.getItem("user"));

if (!user || !user._id) {
  console.error("❌ User not found in localStorage");
  window.location.href = "/login";
}

// 2️⃣ Show greeting
document.getElementById("welcome").innerText = `Hi, ${user.name}`;

// 3️⃣ Load PDFs
async function loadPdfs() {
  try {
    const res = await fetch(`/pdf/list/${user._id}`);
    const data = await res.json();

    const list = document.getElementById("pdfList");
    list.innerHTML = "";

    data.forEach(pdf => {
      const li = document.createElement("li");
      li.innerHTML = `
        ${pdf.filename}
        <button onclick="renamePdf('${pdf._id}')">Rename</button>
        <button onclick="deletePdf('${pdf._id}')">Delete</button>
      `;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Failed to load PDFs", err);
  }
}

loadPdfs();

// 4️⃣ Handle PDF upload
const uploadForm = document.getElementById("uploadForm");

uploadForm.addEventListener("submit", async (e) => {
    console.log("🔥 upload submit triggered");
  e.preventDefault();

  const fileInput = document.getElementById("pdfFile");
  if (!fileInput.files.length) {
    alert("Please select a PDF file");
    return;
  }

  const formData = new FormData();
  formData.append("pdf", fileInput.files[0]);
  formData.append("user_id", user._id);

  try {
    const res = await fetch("/pdf/upload/pdf", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.message || "Upload failed");
      return;
    }

    alert("PDF uploaded successfully");
    fileInput.value = "";
    loadPdfs(); // 🔥 refresh list
  } catch (err) {
    console.error("Upload error", err);
    alert("Upload failed");
  }
});

async function renamePdf(pdfId) {
    const newName = prompt("Enter new filename");
  
    if (!newName) return;
  
    const res = await fetch(`/pdf/rename/${pdfId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: newName })
    });
  
    const data = await res.json();
    alert(data.message);
  
    if (res.ok) loadPdfs();
  }
  
  async function deletePdf(pdfId) {
    if (!confirm("Are you sure you want to delete this PDF?")) return;
  
    const res = await fetch(`/pdf/delete/${pdfId}`, {
      method: "DELETE"
    });
  
    const data = await res.json();
    alert(data.message);
  
    if (res.ok) loadPdfs();
  }
  
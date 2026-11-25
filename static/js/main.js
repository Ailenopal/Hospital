/* Hospital Management System - front-end behaviour
   SECTIONS (in order): sidebar toggle | auto-dismiss alerts | confirmation pop-up (<form data-confirm="...">)
                        | profile photo preview | live age from date of birth | scroll to first form error */
(function () {
  "use strict";

  // Responsive sidebar
  const body = document.body;
  document.querySelectorAll("[data-sidebar-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () { body.classList.toggle("sidebar-open"); });
  });
  const overlay = document.querySelector(".sidebar-overlay");
  if (overlay) overlay.addEventListener("click", function () { body.classList.remove("sidebar-open"); });

  // Auto-dismiss success alerts
  document.querySelectorAll(".alert[data-autodismiss]").forEach(function (el) {
    setTimeout(function () {
      if (window.bootstrap) bootstrap.Alert.getOrCreateInstance(el).close();
    }, 6000);
  });

  // Confirmation modal for any <form data-confirm="..."> (archive, deactivate, sign out ...)
  const modalEl = document.getElementById("confirmModal");
  if (modalEl && window.bootstrap) {
    const modal = new bootstrap.Modal(modalEl);
    const titleEl = modalEl.querySelector("[data-confirm-title]");
    const textEl = modalEl.querySelector("[data-confirm-text]");
    const okBtn = modalEl.querySelector("[data-confirm-ok]");
    let pendingForm = null;

    document.addEventListener("submit", function (event) {
      const form = event.target;
      if (!form.matches || !form.matches("form[data-confirm]")) return;
      event.preventDefault();
      pendingForm = form;
      titleEl.textContent = form.dataset.confirmTitle || "Please confirm";
      textEl.textContent = form.dataset.confirm;
      okBtn.textContent = form.dataset.confirmBtn || "Confirm";
      okBtn.className = "btn " + (form.dataset.confirmClass || "btn-danger");
      modal.show();
    });
    okBtn.addEventListener("click", function () {
      if (pendingForm) { const f = pendingForm; pendingForm = null; modal.hide(); f.submit(); }
    });
  }

  // Profile photo preview
  const photoInput = document.querySelector("input[type=file][data-preview]");
  if (photoInput) {
    photoInput.addEventListener("change", function () {
      const file = photoInput.files[0];
      const box = document.getElementById("photoPreview");
      if (!file || !box) return;
      const reader = new FileReader();
      reader.onload = function (e) { box.innerHTML = '<img src="' + e.target.result + '" alt="Preview" style="width:100%;height:100%;object-fit:cover">'; };
      reader.readAsDataURL(file);
    });
  }

  // Live age calculation from date of birth
  const dob = document.getElementById("id_date_of_birth");
  const ageOut = document.getElementById("ageDisplay");
  function showAge() {
    if (!dob || !ageOut || !dob.value) { if (ageOut) ageOut.textContent = "-"; return; }
    const b = new Date(dob.value), t = new Date();
    if (isNaN(b)) { ageOut.textContent = "-"; return; }
    let age = t.getFullYear() - b.getFullYear();
    const m = t.getMonth() - b.getMonth();
    if (m < 0 || (m === 0 && t.getDate() < b.getDate())) age--;
    ageOut.textContent = age >= 0 ? age + " years old" : "Invalid date";
  }
  if (dob) { dob.addEventListener("change", showAge); dob.addEventListener("input", showAge); showAge(); }

  // Scroll to first form error
  const firstError = document.querySelector(".field-has-error");
  if (firstError) firstError.scrollIntoView({ block: "center", behavior: "smooth" });
})();

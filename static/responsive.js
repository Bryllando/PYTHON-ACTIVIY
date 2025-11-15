document.addEventListener('DOMContentLoaded', function () {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalContent = document.getElementById('modalContent');
    const addStudentBtn = document.getElementById('addstudent');
    const cancelBtn = document.getElementById('cancelBtn');
    const saveBtn = document.getElementById('saveBtn');
    const studentForm = document.getElementById('studentForm');
    const modalTitle = document.getElementById('modalTitle');

    // Show modal
    function showModal() {
        modalOverlay.classList.remove('hidden');
        setTimeout(() => {
            modalContent.classList.remove('scale-95', 'opacity-0');
            modalContent.classList.add('scale-100', 'opacity-100');
        }, 50);
    }

    // Hide modal
    function hideModal() {
        modalContent.classList.remove('scale-100', 'opacity-100');
        modalContent.classList.add('scale-95', 'opacity-0');
        setTimeout(() => {
            modalOverlay.classList.add('hidden');
        }, 300);
    }

    // Reset form to add mode
    function resetToAddMode() {
        studentForm.reset();
        modalTitle.textContent = 'Add New Student';
        saveBtn.textContent = 'Save Student';
        studentForm.action = "/add_student";
        document.getElementById('studentId').disabled = false;
    }

    // Add Student button click
    addStudentBtn.addEventListener('click', function () {
        resetToAddMode();
        showModal();
    });

    // Cancel button click
    cancelBtn.addEventListener('click', hideModal);

    // Modal overlay click
    modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) {
            hideModal();
        }
    });

    // Save Student button click - simply submit the form
    saveBtn.addEventListener('click', function () {
        // Basic validation
        const studentId = document.getElementById('studentId').value;
        const lastName = document.getElementById('lastName').value;
        const firstName = document.getElementById('firstName').value;
        const course = document.getElementById('course').value;
        const level = document.getElementById('level').value;

        if (!studentId || !lastName || !firstName || !course || !level) {
            alert('Please fill in all fields');
            return;
        }

        // Submit the form
        studentForm.submit();
    });

    // Edit button click - FIXED VERSION
    document.addEventListener('click', function (e) {
        // Find the closest .edit-btn button (works even if span is clicked)
        const editBtn = e.target.closest('.edit-btn');

        if (editBtn) {
            const studentId = editBtn.getAttribute('data-id');
            const lastname = editBtn.getAttribute('data-lastname');
            const firstname = editBtn.getAttribute('data-firstname');
            const course = editBtn.getAttribute('data-course');
            const level = editBtn.getAttribute('data-level');

            // Fill form with student data
            document.getElementById('studentId').value = studentId;
            document.getElementById('lastName').value = lastname;
            document.getElementById('firstName').value = firstname;
            document.getElementById('course').value = course;
            document.getElementById('level').value = level;

            // Set to edit mode
            modalTitle.textContent = 'Edit Student';
            saveBtn.textContent = 'Update Student';
            studentForm.action = `/edit_student/${studentId}`;
            document.getElementById('studentId').disabled = true;

            // Show modal
            showModal();
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const cancelBtn = document.getElementById('cancelBtn');
    const saveBtn = document.getElementById('saveBtn');
    const studentForm = document.getElementById('studentForm');
    const profilePictureInput = document.getElementById('profilePictureInput');
    const profilePreview = document.getElementById('profilePreview');
    const defaultAvatar = document.getElementById('defaultAvatar');
    const uploadButton = document.getElementById('uploadButton');
    const profilePictureContainer = document.getElementById('profilePictureContainer');

    let currentProfilePicture = null;

    // Trigger file input when upload button or container is clicked
    uploadButton.addEventListener('click', function (e) {
        e.stopPropagation();
        profilePictureInput.click();
    });

    profilePictureContainer.addEventListener('click', function () {
        profilePictureInput.click();
    });

    // Handle profile picture selection and preview
    profilePictureInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            if (!file.type.match('image.*')) {
                alert('Please select an image file');
                return;
            }

            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('Image size should be less than 5MB');
                return;
            }

            // Preview the image
            const reader = new FileReader();
            reader.onload = function (e) {
                currentProfilePicture = e.target.result;
                profilePreview.src = e.target.result;
                profilePreview.classList.remove('hidden');
                defaultAvatar.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    // Reset form to add mode
    function resetToAddMode() {
        studentForm.reset();
        saveBtn.textContent = 'SAVE';
        studentForm.action = "/add_student";
        document.getElementById('studentId').disabled = false;

        // Reset profile picture
        profilePreview.classList.add('hidden');
        defaultAvatar.classList.remove('hidden');
        profilePictureInput.value = '';
        currentProfilePicture = null;

        // Reset select placeholders
        document.getElementById('course').selectedIndex = 0;
        document.getElementById('level').selectedIndex = 0;
    }

    // Cancel button click
    cancelBtn.addEventListener('click', function () {
        resetToAddMode();
    });

    // Save Student button click
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

    // Edit button click
    document.addEventListener('click', function (e) {
        const editBtn = e.target.closest('.edit-btn');
        if (editBtn) {
            const studentId = editBtn.getAttribute('data-id');
            const lastname = editBtn.getAttribute('data-lastname');
            const firstname = editBtn.getAttribute('data-firstname');
            const course = editBtn.getAttribute('data-course');
            const level = editBtn.getAttribute('data-level');
            const picture = editBtn.getAttribute('data-picture');

            // Fill form with student data
            document.getElementById('studentId').value = studentId;
            document.getElementById('lastName').value = lastname;
            document.getElementById('firstName').value = firstname;
            document.getElementById('course').value = course;
            document.getElementById('level').value = level;

            // Load profile picture if exists
            if (picture) {
                profilePreview.src = 'data:image/jpeg;base64,' + picture;
                profilePreview.classList.remove('hidden');
                defaultAvatar.classList.add('hidden');
                currentProfilePicture = picture;
            } else {
                profilePreview.classList.add('hidden');
                defaultAvatar.classList.remove('hidden');
                currentProfilePicture = null;
            }

            // Set to edit mode
            saveBtn.textContent = 'UPDATE';
            studentForm.action = `/edit_student/${studentId}`;
            document.getElementById('studentId').disabled = true;

            // Scroll to form on mobile
            if (window.innerWidth < 1024) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
    });
});
// Profile picture upload functionality
document.addEventListener('DOMContentLoaded', function () {
    const profileContainer = document.getElementById('profilePictureContainer');
    const profileInput = document.getElementById('profilePictureInput');
    const profilePreview = document.getElementById('profilePreview');
    const defaultAvatar = document.getElementById('defaultAvatar');
    const uploadButton = document.getElementById('uploadButton');
    const saveBtn = document.getElementById('saveBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const studentForm = document.getElementById('studentForm');

    // Profile picture upload
    if (uploadButton && profileInput) {
        uploadButton.addEventListener('click', function () {
            profileInput.click();
        });

        profileInput.addEventListener('change', function (e) {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    profilePreview.src = e.target.result;
                    profilePreview.classList.remove('hidden');
                    defaultAvatar.classList.add('hidden');
                }

                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }

    // Form handling
    if (saveBtn) {
        saveBtn.addEventListener('click', function () {
            studentForm.submit();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            studentForm.reset();
            profilePreview.classList.add('hidden');
            defaultAvatar.classList.remove('hidden');
            if (profileInput) profileInput.value = '';
        });
    }

    // Edit button functionality
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const lastname = this.getAttribute('data-lastname');
            const firstname = this.getAttribute('data-firstname');
            const course = this.getAttribute('data-course');
            const level = this.getAttribute('data-level');
            const picture = this.getAttribute('data-picture');

            // Populate form fields
            document.getElementById('studentId').value = id;
            document.getElementById('lastName').value = lastname;
            document.getElementById('firstName').value = firstname;
            document.getElementById('course').value = course;
            document.getElementById('level').value = level;

            // Handle profile picture
            if (picture) {
                profilePreview.src = 'data:image/jpeg;base64,' + picture;
                profilePreview.classList.remove('hidden');
                defaultAvatar.classList.add('hidden');
            } else {
                profilePreview.classList.add('hidden');
                defaultAvatar.classList.remove('hidden');
            }

            // Change form action to edit
            studentForm.action = `/edit_student/${id}`;

            // Scroll to form
            document.querySelector('.lg\\:col-span-1').scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Mobile responsiveness
    function handleResize() {
        const tableContainer = document.querySelector('.overflow-x-auto');
        if (tableContainer && window.innerWidth < 768) {
            tableContainer.style.overflowX = 'auto';
        }
    }

    window.addEventListener('resize', handleResize);
    handleResize();
});
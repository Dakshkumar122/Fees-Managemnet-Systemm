document.addEventListener("DOMContentLoaded", function () {
    const dobInput = document.getElementById('id_dob');
    const ageLabel = document.getElementById('age');

    dobInput.addEventListener('change', function () {
        const dobValue = this.value;
        if (!dobValue) return;

        const dob = new Date(dobValue);
        const today = new Date();

        let years = today.getFullYear() - dob.getFullYear();
        let months = today.getMonth() - dob.getMonth();
        let days = today.getDate() - dob.getDate();

        if (days < 0) {
            months -= 1;
            days += new Date(today.getFullYear(), today.getMonth(), 0).getDate(); // last day of previous month
        }

        if (months < 0) {
            years -= 1;
            months += 12;
        }

        age.textContent = `${years} years, ${months} months, ${days} days`;
    });
});

$(document).ready(function () {
    function generateStudentID() {
        var name = $('#id_student_name').val().trim();
        var phone = $('#id_phone_number').val().trim();

        var initials = '';
        if (name.length > 0) {
            var parts = name.split(" ");
            for (var i = 0; i < parts.length; i++) {
                if (parts[i].length > 0) {
                    initials += parts[i].charAt(0);
                }
            }
        }

        var student_id = initials + phone;
        $('#id_student_id').val(student_id);
    }

    $('#id_student_name, #id_phone_number').on('input', generateStudentID);


    // ============

    const courseFees = {
        'python': '12000',
        'wd': '3000',
        'olevel': '1200',
        'adca': '500',
        'dca': '500',
        'DTP': '500',
        'dcfa': '500',
        'ccc': '800',
        'excel': '1000',
        'tally': '1000',
        'word': '1000',
        'typing':'400',
    };

    function updateFees() {
        const selectedCourse = $('#id_course_name').val();
        const fee = courseFees[selectedCourse] || '';
        $('#id_course_fees').val(fee);
    }

    // Update on course change
    $('#id_course_name').on('change', updateFees);

    // Set default value if editing
    updateFees();






    // =============
    const studentId = $("#student_id").val();

    if (studentId) {
        $.get("/ajax/installment/" + studentId + "/", function (data) {
            $("#id_installment_no").val(data.installment_no + 1);
        });
    }




    // ++++++++++++++++++++





});



// ==================================

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('student-search');
    const resultsBox = document.getElementById('search-results');

    function fillStudentDetails(id) {
        fetch(`/get-student-details/${id}/`)
            .then(res => res.json())
            .then(details => {
                // Auto-fill form fields
                document.getElementById('student_id').value = details.Student_id;
                document.getElementById('id_student_name').value = details.student_name;
                document.getElementById('id_father_name').value = details.father_name;
                document.getElementById('id_dob').value = details.dob;
                document.getElementById('id_email').value = details.email;
                document.getElementById('id_phone_number').value = details.phone_number;
                document.getElementById('id_student_id').value = details.Student_id;
                document.getElementById('id_course_name').value = details.course_name;
                document.getElementById('id_course_fees').value = details.course_fees;
                document.getElementById('id_installment_no').value = details.installment_no;

                // Make some fields readonly
                document.getElementById('id_student_name').readOnly = true;
                document.getElementById('id_father_name').readOnly = true;
                document.getElementById('id_dob').readOnly = true;
                document.getElementById('id_email').readOnly = true;
                document.getElementById('id_phone_number').readOnly = true;
                document.getElementById('id_student_img').disabled = true;
                document.getElementById('id_student_id').readOnly = true;
                document.getElementById('id_course_name').readOnly = true;

                resultsBox.style.display = 'none';
            });
    }

    function searchAndFill(query) {
        if (query.length === 0) {
            resultsBox.style.display = 'none';
            return;
        }

        fetch(`/search-student-ids/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                resultsBox.innerHTML = '';
                if (data.results.length > 0) {
                    resultsBox.style.display = 'block';
                    let exactMatchItem = null;

                    data.results.forEach(item => {
                        if (item.student_id.toLowerCase() === query.toLowerCase()) {
                            exactMatchItem = item;
                        }

                        const li = document.createElement('li');
                        li.classList.add('list-group-item', 'list-group-item-action');
                        li.textContent = item.student_id;
                        li.dataset.id = item.id;
                        li.addEventListener('click', function () {
                            fillStudentDetails(this.dataset.id);
                        });
                        resultsBox.appendChild(li);
                    });

                    if (exactMatchItem) {
                        fillStudentDetails(exactMatchItem.id);
                    }
                } else {
                    resultsBox.style.display = 'none';
                }
            })
            .catch(() => {
                resultsBox.style.display = 'none';
            });
    }

    // Trigger search if input has value on page load
    if (searchInput.value.trim().length > 0) {
        searchAndFill(searchInput.value.trim());
    }

    // Trigger search on keyup (live typing)
    searchInput.addEventListener('keyup', function () {
        const query = this.value.trim();
        searchAndFill(query);
    });
});


// ===========================image validations 


document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');  // Your form element
    const installmentInput = document.getElementById('id_installment_no');
    const imageInput = document.getElementById('id_student_img');
    const errorSpan = document.getElementById('img-error');

    function toggleImageRequired() {
        if (installmentInput.value === 1) {
            imageInput.required = true;
        } else {
            imageInput.required = false;
            errorSpan.style.display = 'none'; // hide error if not first installment
        }
    }

    // Run on page load and input change
    toggleImageRequired();
    installmentInput.addEventListener('input', toggleImageRequired);

    // On form submit, validate
    form.addEventListener('submit', function (e) {
        if (installmentInput.value === 1 && !imageInput.value) {
            e.preventDefault();  // Stop form submission
            errorSpan.style.display = 'inline';  // Show error message
            imageInput.focus();
        } else {
            errorSpan.style.display = 'none';  // Hide error message if valid
        }
    });

    // Hide error if user selects image after seeing error
    imageInput.addEventListener('change', function () {
        if (imageInput.value) {
            errorSpan.style.display = 'none';
        }
    });
});





// ===============================Error message 

document.getElementById('clear-btn').addEventListener('click', function () {
    const form = document.getElementById('student-form') || document.querySelector('form');
    if (!form) return;

    // Preserve hidden fields if needed
    const preserveHidden = ['student_id'];
    const preservedValues = {};
    preserveHidden.forEach(id => {
        const el = document.getElementById(id);
        if (el) preservedValues[id] = el.value;
    });

    // Reset the form
    form.reset();

    // Clear file inputs and previews
    form.querySelectorAll('input[type="file"]').forEach(input => {
        input.value = '';
        const preview = document.getElementById(input.id + '-preview');
        if (preview) preview.src = '';
    });

    // Clear checkboxes and radios
    form.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(ch => ch.checked = false);

    // Clear custom spans (like age display)
    const ageSpan = document.getElementById('age');
    if (ageSpan) ageSpan.textContent = '';

    // Hide inline validation messages
    form.querySelectorAll('.text-danger.small').forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });

    // Hide image error span
    const imgErr = document.getElementById('img-error');
    if (imgErr) imgErr.style.display = 'none';

    // Restore preserved hidden values
    Object.keys(preservedValues).forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = preservedValues[id];
    });

    // Make all inputs editable again
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.readOnly = false;
        input.disabled = false;
    });

    // Explicitly enable student image field
    const studentImg = document.getElementById('id_student_img');
    const stu_id = document.getElementById('id_student_id');
    const stu_inst = document.getElementById('id_installment_no');
    const course_fee = document.getElementById('id_course_fees');
    if (stu_id && course_fee && stu_inst) {
        stu_id.readOnly = true;
        stu_inst.readOnly = true;
        course_fee.readOnly = true;
    }
    if (studentImg) {
        studentImg.disabled = false;
        studentImg.readOnly = false;
    }

    // Focus first visible input
    const first = form.querySelector('input:not([type=hidden]):not([type=file]), select, textarea');
    if (first) first.focus();
});






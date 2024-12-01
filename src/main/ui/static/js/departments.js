document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('departments-table')) {
        loadDepartments();

        // Event listener for create department button
        document.getElementById('create-department-btn').addEventListener('click', showCreateDepartmentModal);
    }
});

function loadDepartments() {
    fetch('api/v1/departments?limit=100') // Adjust limit as needed
        .then(response => response.json())
        .then(data => {
            const departments = data.departments;
            const tableBody = document.querySelector('#departments-table tbody');
            tableBody.innerHTML = '';
            departments.forEach(department => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${department.department_id}</td>
                    <td>${department.department}</td>
                    <td>
                        <button class="btn btn-sm btn-primary edit-department-btn" data-id="${department.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-department-btn" data-id="${department.id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners for edit and delete buttons
            document.querySelectorAll('.edit-department-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    showEditDepartmentModal(id);
                });
            });

            document.querySelectorAll('.delete-department-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    deleteDepartment(id);
                });
            });
        })
        .catch(error => {
            console.error('Error fetching departments:', error);
        });
}

function showCreateDepartmentModal() {
    const modalContent = document.querySelector('#department-modal .modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h5 class="modal-title">Create New Department</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form id="department-form">
                <div class="form-group">
                    <label for="department_id">Department ID</label>
                    <input type="number" class="form-control" id="department_id" name="department_id" required>
                </div>
                <div class="form-group">
                    <label for="department">Department Name</label>
                    <input type="text" class="form-control" id="department" name="department" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    `;
    document.getElementById('department-form').addEventListener('submit', createDepartment);
    $('#department-modal').modal('show');
}

function createDepartment(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const departmentData = Object.fromEntries(formData.entries());
    fetch('api/v1/departments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(departmentData)
    })
        .then(response => response.json())
        .then(data => {
            $('#department-modal').modal('hide');
            loadDepartments();
        })
        .catch(error => {
            console.error('Error creating department:', error);
        });
}

function showEditDepartmentModal(id) {
    fetch(`api/v1/departments/${encodeURIComponent(id)}`)
        .then(response => response.json())
        .then(department => {
            const modalContent = document.querySelector('#department-modal .modal-content');
            modalContent.innerHTML = `
                <div class="modal-header">
                    <h5 class="modal-title">Edit Department</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="department-form">
                        <input type="hidden" id="department_id" name="department_id" value="${department.department_id}">
                        <div class="form-group">
                            <label for="department">Department Name</label>
                            <input type="text" class="form-control" id="department" name="department" value="${department.department}" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            `;
            document.getElementById('department-form').addEventListener('submit', function (event) {
                updateDepartment(event, id);
            });
            $('#department-modal').modal('show');
        })
        .catch(error => {
            console.error('Error fetching department:', error);
        });
}

function updateDepartment(event, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const departmentData = Object.fromEntries(formData.entries());
    fetch(`api/v1/departments?id=${encodeURIComponent(id)}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(departmentData)
    })
        .then(response => response.json())
        .then(data => {
            $('#department-modal').modal('hide');
            loadDepartments();
        })
        .catch(error => {
            console.error('Error updating department:', error);
        });
}

function deleteDepartment(id) {
    if (confirm('Are you sure you want to delete this department?')) {
        fetch(`api/v1/departments?id=${encodeURIComponent(id)}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                loadDepartments();
            })
            .catch(error => {
                console.error('Error deleting department:', error);
            });
    }
}

// static/js/aisles.js

document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('aisles-table')) {
        loadAisles();

        // Event listener for create aisle button
        document.getElementById('create-aisle-btn').addEventListener('click', showCreateAisleModal);
    }
});

function loadAisles() {
    fetch('api/v1/aisles?limit=100') // Adjust limit as needed
        .then(response => response.json())
        .then(data => {
            const aisles = data.aisles;
            const tableBody = document.querySelector('#aisles-table tbody');
            tableBody.innerHTML = '';
            aisles.forEach(aisle => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${aisle.aisle_id}</td>
                    <td>${aisle.aisle}</td>
                    <td>
                        <button class="btn btn-sm btn-primary edit-aisle-btn" data-id="${aisle.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-aisle-btn" data-id="${aisle.id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners for edit and delete buttons
            document.querySelectorAll('.edit-aisle-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    showEditAisleModal(id);
                });
            });

            document.querySelectorAll('.delete-aisle-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    deleteAisle(id);
                });
            });
        })
        .catch(error => {
            console.error('Error fetching aisles:', error);
        });
}

function showCreateAisleModal() {
    const modalContent = document.querySelector('#aisle-modal .modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h5 class="modal-title">Create New Aisle</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form id="aisle-form">
                <div class="form-group">
                    <label for="aisle_id">Aisle ID</label>
                    <input type="number" class="form-control" id="aisle_id" name="aisle_id" required>
                </div>
                <div class="form-group">
                    <label for="aisle">Aisle Name</label>
                    <input type="text" class="form-control" id="aisle" name="aisle" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    `;
    document.getElementById('aisle-form').addEventListener('submit', createAisle);
    $('#aisle-modal').modal('show');
}

function createAisle(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const aisleData = Object.fromEntries(formData.entries());
    fetch('api/v1/aisles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(aisleData)
    })
        .then(response => response.json())
        .then(data => {
            $('#aisle-modal').modal('hide');
            loadAisles();
        })
        .catch(error => {
            console.error('Error creating aisle:', error);
        });
}

function showEditAisleModal(id) {
    fetch(`api/v1/aisles/${encodeURIComponent(id)}`)
        .then(response => response.json())
        .then(aisle => {
            const modalContent = document.querySelector('#aisle-modal .modal-content');
            modalContent.innerHTML = `
                <div class="modal-header">
                    <h5 class="modal-title">Edit Aisle</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="aisle-form">
                        <input type="hidden" id="aisle_id" name="aisle_id" value="${aisle.aisle_id}">
                        <div class="form-group">
                            <label for="aisle">Aisle Name</label>
                            <input type="text" class="form-control" id="aisle" name="aisle" value="${aisle.aisle}" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            `;
            document.getElementById('aisle-form').addEventListener('submit', function (event) {
                updateAisle(event, id);
            });
            $('#aisle-modal').modal('show');
        })
        .catch(error => {
            console.error('Error fetching aisle:', error);
        });
}

function updateAisle(event, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const aisleData = Object.fromEntries(formData.entries());
    fetch(`api/v1/aisles?id=${encodeURIComponent(id)}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(aisleData)
    })
        .then(response => response.json())
        .then(data => {
            $('#aisle-modal').modal('hide');
            loadAisles();
        })
        .catch(error => {
            console.error('Error updating aisle:', error);
        });
}

function deleteAisle(id) {
    if (confirm('Are you sure you want to delete this aisle?')) {
        fetch(`api/v1/aisles?id=${encodeURIComponent(id)}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                loadAisles();
            })
            .catch(error => {
                console.error('Error deleting aisle:', error);
            });
    }
}

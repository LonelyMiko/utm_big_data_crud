document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('products-table')) {
        loadProducts();

        // Event listener for create product button
        document.getElementById('create-product-btn').addEventListener('click', ProductModal);
    }
});

function loadProducts() {
    fetch('api/v1/products?limit=100') // Adjust limit as needed
        .then(response => response.json())
        .then(data => {
            const products = data.products;
            const tableBody = document.querySelector('#products-table tbody');
            tableBody.innerHTML = '';
            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.product_id}</td>
                    <td>${product.product_name}</td>
                    <td>${product.aisle_id}</td>
                    <td>${product.department_id}</td>
                    <td>
                        <button class="btn btn-sm btn-primary edit-product-btn" data-id="${product.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-product-btn" data-id="${product.id}">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Add event listeners for edit and delete buttons
            document.querySelectorAll('.edit-product-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    showEditProductModal(id);
                });
            });

            document.querySelectorAll('.delete-product-btn').forEach(button => {
                button.addEventListener('click', event => {
                    const id = event.currentTarget.getAttribute('data-id');
                    deleteProduct(id);
                });
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });showCreate
}

function showCreateProductModal() {
    const modalContent = document.querySelector('#product-modal .modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h5 class="modal-title">Create New Product</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form id="product-form">
                <div class="form-group">
                    <label for="product_id">Product ID</label>
                    <input type="number" class="form-control" id="product_id" name="product_id" required>
                </div>
                <div class="form-group">
                    <label for="product_name">Product Name</label>
                    <input type="text" class="form-control" id="product_name" name="product_name" required>
                </div>
                <div class="form-group">
                    <label for="aisle_id">Aisle ID</label>
                    <input type="number" class="form-control" id="aisle_id" name="aisle_id" required>
                </div>
                <div class="form-group">
                    <label for="department_id">Department ID</label>
                    <input type="number" class="form-control" id="department_id" name="department_id" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    `;
    document.getElementById('product-form').addEventListener('submit', createProduct);
    $('#product-modal').modal('show');
}

function createProduct(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const productData = Object.fromEntries(formData.entries());
    fetch('api/v1/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
        .then(response => response.json())
        .then(data => {
            $('#product-modal').modal('hide');
            loadProducts();
        })
        .catch(error => {
            console.error('Error creating product:', error);
        });
}

function showEditProductModal(id) {
    fetch(`api/v1/products/${encodeURIComponent(id)}`)
        .then(response => response.json())
        .then(product => {
            const modalContent = document.querySelector('#product-modal .modal-content');
            modalContent.innerHTML = `
                <div class="modal-header">
                    <h5 class="modal-title">Edit Product</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="product-form">
                        <input type="hidden" id="product_id" name="product_id" value="${product.product_id}">
                        <div class="form-group">
                            <label for="product_name">Product Name</label>
                            <input type="text" class="form-control" id="product_name" name="product_name" value="${product.product_name}" required>
                        </div>
                        <div class="form-group">
                            <label for="aisle_id">Aisle ID</label>
                            <input type="number" class="form-control" id="aisle_id" name="aisle_id" value="${product.aisle_id}" required>
                        </div>
                        <div class="form-group">
                            <label for="department_id">Department ID</label>
                            <input type="number" class="form-control" id="department_id" name="department_id" value="${product.department_id}" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            `;
            document.getElementById('product-form').addEventListener('submit', function (event) {
                updateProduct(event, id);
            });
            $('#product-modal').modal('show');
        })
        .catch(error => {
            console.error('Error fetching product:', error);
        });
}

function updateProduct(event, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const productData = Object.fromEntries(formData.entries());
    fetch(`api/v1/products?id=${encodeURIComponent(id)}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
        .then(response => response.json())
        .then(data => {
            $('#product-modal').modal('hide');
            loadProducts();
        })
        .catch(error => {
            console.error('Error updating product:', error);
        });
}

function deleteProduct(id) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/api/v1/products?id=${encodeURIComponent(id)}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                loadProducts();
            })
            .catch(error => {
                console.error('Error deleting product:', error);
            });
    }
}

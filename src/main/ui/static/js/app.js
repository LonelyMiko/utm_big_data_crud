document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('orders-table')) {
        loadOrders();

        // Event listener for create order button
        document.getElementById('create-order-btn').addEventListener('click', showCreateOrderModal);
    }
});

function loadOrders() {
    fetch('/api/v1/orders?limit=100')
        .then(response => response.json())
        .then(data => {
            const orders = data.orders;
            const tableBody = document.querySelector('#orders-table tbody');
            tableBody.innerHTML = '';
            orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.order_id}</td>
                    <td>${order.user_id}</td>
                    <td>${order.order_number}</td>
                    <td>${order.order_dow}</td>
                    <td>${order.order_hour_of_day}</td>
                    <td>${order.days_since_prior_order}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="showEditOrderModal('${order.id}')">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteOrder('${order.id}')">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function showCreateOrderModal() {
    const modalContent = document.querySelector('#order-modal .modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h5 class="modal-title" id="orderModalLabel">Create New Order</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form id="order-form">
                <div class="form-group">
                    <label for="order_id">Order ID</label>
                    <input type="number" class="form-control" id="order_id" name="order_id" required>
                </div>
                <div class="form-group">
                    <label for="user_id">User ID</label>
                    <input type="number" class="form-control" id="user_id" name="user_id" required>
                </div>
                <div class="form-group">
                    <label for="user_id">Order Number</label>
                    <input type="number" class="form-control" id="order_number" name="order_number" required>
                </div>
                <div class="form-group">
                    <label for="user_id">Order DOW</label>
                    <input type="number" class="form-control" id="order_dow" name="order_dow" required>
                </div>
                <div class="form-group">
                    <label for="user_id">Order Hour</label>
                    <input type="number" class="form-control" id="order_hour_of_day" name="order_hour_of_day" required>
                </div>
                <div class="form-group">
                    <label for="user_id">Days Since Prior</label>
                    <input type="number" class="form-control" id="days_since_prior_order" name="days_since_prior_order" required>
                </div>
                <!-- ... -->
                <button type="submit" class="btn btn-primary">Save</button>
            </form>
        </div>
    `;
    // Add event listener for form submission
    document.getElementById('order-form').addEventListener('submit', createOrder);
    // Show the modal
    $('#order-modal').modal('show');
}

function createOrder(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const orderData = Object.fromEntries(formData.entries());
    fetch('/api/v1/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
        .then(response => response.json())
        .then(data => {
            $('#order-modal').modal('hide');
            loadOrders();
        });
}

function showEditOrderModal(id) {
    fetch(`api/v1/orders/${id}`)
        .then(response => response.json())
        .then(order => {
            const modalContent = document.querySelector('#order-modal .modal-content');
            modalContent.innerHTML = `
                <div class="modal-header">
                    <h5 class="modal-title" id="orderModalLabel">Edit Order</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="order-form">
                        <input type="hidden" id="order_id" name="order_id" value="${order.order_id}">
                        <input type="hidden" id="eval_set" name="eval_set" value="test">
                        <div class="form-group">
                            <label for="user_id">User ID</label>
                            <input type="number" class="form-control" id="user_id" name="user_id" value="${order.user_id}" required>
                        </div>
                        <div class="form-group">
                            <label for="user_id">Order Number</label>
                            <input type="number" class="form-control" id="order_number" name="order_number" value="${order.order_number}" required>
                        </div>
                        <div class="form-group">
                            <label for="user_id">Order DOW</label>
                            <input type="number" class="form-control" id="order_dow" name="order_dow" value="${order.order_dow}" required>
                        </div>
                        <div class="form-group">
                            <label for="user_id">Order Hour</label>
                            <input type="number" class="form-control" id="order_hour_of_day" name="order_hour_of_day" value="${order.order_hour_of_day}" required>
                        </div>
                        <div class="form-group">
                            <label for="user_id">Days Since Prior</label>
                            <input type="number" class="form-control" id="days_since_prior_order" name="days_since_prior_order" value="${order.days_since_prior_order}" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            `;
            document.getElementById('order-form').addEventListener('submit', function (event) {
                updateOrder(event, id);
            });
            // Show the modal
            $('#order-modal').modal('show');
        });
}

function updateOrder(event, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const orderData = Object.fromEntries(formData.entries());
    fetch(`api/v1/orders?id=${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
        .then(response => response.json())
        .then(data => {
            $('#order-modal').modal('hide');
            loadOrders();
        });
}

function deleteOrder(id) {
    if (confirm('Are you sure you want to delete this order?')) {
        fetch(`api/v1/orders?id=${id}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                loadOrders();
            });
    }
}

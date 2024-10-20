const combinedApiUrl = 'http://138.197.60.159:8888';

// Fetch todos and display them
async function fetchTodos() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${combinedApiUrl}/todo?Username=${username}&Password=${password}`);
    const todos = await response.json();

    const todoList = document.getElementById('todoList');
    todoList.innerHTML = ''; // Clear the list

    if (Array.isArray(todos)) {
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.innerText = `${todo[1]} - ${todo[2]} (Due: ${todo[3]})`; // Accessing the elements by index

            // Add a delete button
            const deleteButton = document.createElement('button');
            deleteButton.innerText = 'Delete';
            deleteButton.onclick = () => deleteTodo(todo[0]); // Use todo[0] for ID
            li.appendChild(deleteButton);

            // Add an update button
            const updateButton = document.createElement('button');
            updateButton.innerText = 'Update';
            updateButton.onclick = () => openUpdateForm(todo); // Pass the entire todo for updating
            li.appendChild(updateButton);

            todoList.appendChild(li);
        });
    } else {
        // Handle error response if needed
        alert(todos.error || 'Failed to load todos.');
    }
}

// Create a new todo
async function createTodo() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('dueDate').value;
    const username = document.getElementById('username').value; // Get username
    const password = document.getElementById('password').value; // Get password

    // Construct the payload
    const todoData = {
        Username: username,
        Password: password,
        Title: title,
        Description: description,
        DueDate: dueDate
    };

    const response = await fetch(combinedApiUrl + '/todo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todoData)
    });

    if (response.ok) {
        fetchTodos(); // Refresh the list
    } else {
        const errorData = await response.json();
        alert(`Failed to create todo: ${errorData.error}`);
    }
}

// Open the update form with existing todo details
function openUpdateForm(todo) {
    document.getElementById('updateId').value = todo[0]; // Access ID using index
    document.getElementById('updateTitle').value = todo[1]; // Title
    document.getElementById('updateDescription').value = todo[2]; // Description
    document.getElementById('updateDueDate').value = todo[3]; // DueDate
}

// Update an existing todo
async function updateTodo() {
    const id = document.getElementById('updateId').value;
    const title = document.getElementById('updateTitle').value;
    const description = document.getElementById('updateDescription').value;
    const dueDate = document.getElementById('updateDueDate').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const updatedTodo = { Title: title, Description: description, DueDate: dueDate };

    const response = await fetch(`${combinedApiUrl}/todo/${id}?Username=${username}&Password=${password}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTodo)
    });

    if (response.ok) {
        // Clear the update form
        document.getElementById('updateId').value = '';
        document.getElementById('updateTitle').value = '';
        document.getElementById('updateDescription').value = '';
        document.getElementById('updateDueDate').value = '';

        // Refresh the list
        fetchTodos();
    } else {
        alert('Failed to update todo!');
    }
}

// Delete a todo
async function deleteTodo(id) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${combinedApiUrl}/todo/${id}?Username=${username}&Password=${password}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        // Refresh the list
        fetchTodos();
    } else {
        alert('Failed to delete todo!');
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${combinedApiUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ Username: username, Password: password })
    });

    if (response.ok) {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('todoApp').style.display = 'block';
        fetchTodos();
    } else {
        alert('Login failed!');
    }
}

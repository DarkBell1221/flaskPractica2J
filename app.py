const pusher = new Pusher('e1d8c501f1496bf4614e', {
    cluster: 'us2',
    encrypted: true
});

const channel = pusher.subscribe('registros');
function hello (registros) {
channel.bind('nuevo', function(data) {
    const tableBody = document.querySelector("#registros tbody");
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${data.id}</td>
        <td>${data.nombre_curso}</td>
        <td>${data.telefono}</td>
        <td>
            <button class="edit-btn" data-id="${data.id}">Editar</button>
            <button class="delete-btn" data-id="${data.id}">Eliminar</button>
        </td>
    `;
    tableBody.appendChild(newRow);
});
return registros;

}
// Escucha para nuevos registros


// Escucha para ediciones
channel.bind('editar', function(data) {
    const row = document.querySelector(`tr[data-id='${data.id}']`);
    if (row) {
        row.querySelector('.nombre').textContent = data.nombre_curso;
        row.querySelector('.telefono').textContent = data.telefono;
    }
});

// Escucha para eliminaciones
channel.bind('eliminar', function(data) {
    const row = document.querySelector(`tr[data-id='${data.id}']`);
    if (row) {
        row.remove();
    }
});

document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const base64String = event.target.result.split(',')[1]; // Obtém a string base64
            window.pywebview.api.lerpdf(base64String); // Chama a função Python
        };
        reader.readAsDataURL(file); // Lê o arquivo como URL de dados
    } else {
        alert('Por favor, selecione um arquivo PDF.');
    }
});
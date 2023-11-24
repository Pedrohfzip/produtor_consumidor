function enviarRequisicoes() {
  for (let i = 0; i < 1000; i++) {
    enviarRequisicao();
  }
}

function enviarRequisicao() {
  $.ajax({
    type: "POST",
    url: "http://localhost:5000/receber", // Substitua pelo URL correto do seu servidor
    data: JSON.stringify({
      ID: generateUUID(),
      Price: Math.random() * 100,
      Tax: Math.random() * 10,
    }),
    contentType: "application/json",
    success: function (response) {
      console.log("Requisição enviada com sucesso:", response);
    },
    error: function (error) {
      console.error("Erro ao enviar a requisição:", error);
    },
  });
}

// Função para gerar UUID (simplificada, pode ser necessário usar uma biblioteca)
function generateUUID() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = (Math.random() * 16) | 0,
      v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

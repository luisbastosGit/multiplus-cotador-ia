const URL_BACKEND = "httpsmultiplus-cotador-ia.onrender.com"; 

// --- CONTROLE DA TELA DE ESCOLHA E UPLOAD ---
function showManual() {
  document.getElementById('stepChoice').style.display = 'none';
  document.getElementById('formManual').style.display = 'block';
}

function showUpload() {
  document.getElementById('stepChoice').style.display = 'none';
  document.getElementById('stepUpload').style.display = 'block';
}

function resetToChoice() {
  document.getElementById('stepUpload').style.display = 'none';
  document.getElementById('stepChoice').style.display = 'block';
}

function handleFile(input) {
  const file = input.files[0];
  if (file) {
    if (file.type !== "application/pdf") {
      alert("Erro: Formato inválido. Por favor, envie apenas arquivos em PDF.");
      input.value = "";
      return;
    }
    document.getElementById('fileName').innerText = "Selecionado: " + file.name;
    document.getElementById('uploadText').innerText = "Arquivo pronto para análise!";
    document.getElementById('btnSendPdf').style.display = 'block';
  }
}

// Envio do PDF para a IA (Backend Python)
async function sendPdf() {
  const fileInput = document.getElementById('pdfInput');
  if (!fileInput.files[0]) return;

  const btn = document.getElementById('btnSendPdf');
  btn.innerText = "Enviando para IA...";
  btn.disabled = true;

  const formData = new FormData();
  formData.append('arquivo_pdf', fileInput.files[0]);

  try {
    const response = await fetch(URL_BACKEND + '/extrair-apolice', {
      method: 'POST',
      body: formData
    });
    
    if(response.ok) {
        document.getElementById('stepUpload').style.display = 'none';
        document.getElementById('telaSucesso').style.display = 'block';
    } else {
        throw new Error('Falha no servidor');
    }
  } catch (error) {
    console.error("Erro:", error);
    alert("Ocorreu um erro na comunicação com o motor de IA.");
    btn.innerText = "Iniciar Análise por IA";
    btn.disabled = false;
  }
}

// --- CONTROLE DO WIZARD MANUAL ---
function avancarPasso(p) {
  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-' + p).classList.add('active');
  document.querySelectorAll('.progress-bar li').forEach((l, i) => { if(i < p) l.classList.add('active'); });
}

function voltarPasso(p) {
  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-' + p).classList.add('active');
  document.querySelectorAll('.progress-bar li').forEach((l, i) => { if(i >= p) l.classList.remove('active'); });
}

function selecionarPacote(pac, el) {
  document.querySelectorAll('.card-pacote').forEach(c => c.classList.remove('selecionado'));
  el.classList.add('selecionado');
  document.getElementById('pacoteSelecionado').value = pac;
}

// Envio dos dados manuais para o Backend Python
async function enviarCotacaoManual() {
  if(!document.getElementById('pacoteSelecionado').value) { 
    alert("Por favor, selecione um pacote de cobertura."); 
    return; 
  }
  
  const btn = document.getElementById('btnFinalizar');
  btn.innerText = "Enviando para Seguradoras..."; 
  btn.disabled = true;

  const dados = {
    origem: "manual",
    nome: document.getElementById('nome').value,
    cpf: document.getElementById('cpf').value.replace(/\D/g,''),
    placa: document.getElementById('placa').value,
    email: document.getElementById('email').value,
    pacote: document.getElementById('pacoteSelecionado').value
  };

  try {
    const response = await fetch(URL_BACKEND + '/iniciar-cotacao', { 
        method: "POST", 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados) 
    });
    
    if(response.ok) {
        document.querySelectorAll('.wizard-step').forEach(s => s.style.display = 'none');
        document.querySelector('.progress-bar').style.display = 'none';
        document.getElementById('telaSucesso').style.display = 'block';
    } else {
        throw new Error('Falha no servidor');
    }

  } catch (e) {
    console.error("Erro:", e);
    alert("Ocorreu um erro na comunicação com o motor de cotação."); 
    btn.innerText = "Enviar Pedido"; 
    btn.disabled = false;
  }
}

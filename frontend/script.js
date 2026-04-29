// NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 22:50
const URL_BACKEND = "https://multiplus-cotador-ia.onrender.com"; 

// --- CONTROLE DE TELAS INICIAIS ---
function showManual() {
  document.getElementById('stepChoice').style.display = 'none';
  document.getElementById('formManual').style.display = 'block';
  document.getElementById('telaSucesso').style.display = 'none';
}

function showUpload() {
  document.getElementById('stepChoice').style.display = 'none';
  document.getElementById('stepUpload').style.display = 'block';
  document.getElementById('telaSucesso').style.display = 'none';
}

function resetToChoice() {
  document.getElementById('stepUpload').style.display = 'none';
  document.getElementById('formManual').style.display = 'none';
  document.getElementById('stepChoice').style.display = 'block';
  document.getElementById('telaSucesso').style.display = 'none';
}

// --- LÓGICA DE UPLOAD E IA ---
function handleFile(input) {
  const file = input.files[0];
  if (file) {
    if (file.type !== "application/pdf") {
      alert("Erro: Por favor, selecione um arquivo PDF válido.");
      input.value = "";
      return;
    }
    document.getElementById('fileName').innerText = "Arquivo: " + file.name;
    document.getElementById('uploadText').innerText = "Documento pronto para análise";
    document.getElementById('btnSendPdf').style.display = 'inline-block';
  }
}

async function sendPdf() {
  const fileInput = document.getElementById('pdfInput');
  if (!fileInput.files[0]) return;

  const btn = document.getElementById('btnSendPdf');
  btn.innerText = "Analisando Documento...";
  btn.disabled = true;

  const formData = new FormData();
  formData.append('arquivo_pdf', fileInput.files[0]);

  try {
    const response = await fetch(`${URL_BACKEND}/extrair-apolice`, {
      method: 'POST',
      body: formData
    });
    
    const res = await response.json();
    
    if (response.ok) {
      document.getElementById('stepUpload').style.display = 'none';
      document.getElementById('telaSucesso').style.display = 'block';
      
      // Exibição dos dados capturados
      document.getElementById('dadosExtraidos').style.display = 'block';
      document.getElementById('msgSucesso').innerText = "Análise da IA e Injeção concluídas!";
      document.getElementById('resNome').innerText = res.dados.nome || "Não identificado";
      document.getElementById('resCpf').innerText = res.dados.cpf || "Não identificado";
      document.getElementById('resPlaca').innerText = res.dados.placa || "Não identificado";
      document.getElementById('resStatusRobo').innerText = res.automacao.status || "Pendente";
    } else {
      throw new Error(res.detail || "Erro no processamento");
    }
  } catch (error) {
    console.error("Erro:", error);
    alert("Falha na comunicação com o motor de IA.");
  } finally {
    btn.innerText = "Analisar e Cotar";
    btn.disabled = false;
  }
}

// --- LÓGICA DO WIZARD MANUAL (PASSOS 1 A 4) ---
function avancarPasso(p) {
  // Validação simples antes de avançar
  if (p === 2) {
    if (!document.getElementById('nome').value || !document.getElementById('cpf').value) {
      alert("Por favor, preencha o Nome e CPF.");
      return;
    }
  }

  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-' + p).classList.add('active');
  
  // Atualiza barra de progresso
  document.querySelectorAll('.progress-bar li').forEach((l, i) => {
    if (i < p) l.classList.add('active');
    else l.classList.remove('active');
  });
}

function voltarPasso(p) {
  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-' + p).classList.add('active');
  
  document.querySelectorAll('.progress-bar li').forEach((l, i) => {
    if (i >= p) l.classList.remove('active');
  });
}

function selecionarPacote(pac, el) {
  document.querySelectorAll('.card-pacote').forEach(c => c.classList.remove('selecionado'));
  el.classList.add('selecionado');
  document.getElementById('pacoteSelecionado').value = pac;
}

// --- FINALIZAÇÃO MANUAL ---
async function enviarCotacaoManual() {
  const pacote = document.getElementById('pacoteSelecionado').value;
  if (!pacote) {
    alert("Selecione um plano de cobertura para continuar.");
    return;
  }

  const btn = document.getElementById('btnFinalizar');
  btn.innerText = "Iniciando Robô...";
  btn.disabled = true;

  const dados = {
    origem: "manual",
    nome: document.getElementById('nome').value,
    cpf: document.getElementById('cpf').value.replace(/\D/g, ''),
    placa: document.getElementById('placa').value.toUpperCase(),
    email: document.getElementById('email').value,
    pacote: pacote
  };

  try {
    const response = await fetch(`${URL_BACKEND}/iniciar-cotacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });

    const res = await response.json();

    if (response.ok) {
      document.getElementById('formManual').style.display = 'none';
      document.getElementById('telaSucesso').style.display = 'block';
      document.getElementById('dadosExtraidos').style.display = 'none';
      document.getElementById('msgSucesso').innerText = "Pedido enviado! O robô está processando no portal.";
    } else {
      throw new Error("Erro no servidor");
    }
  } catch (e) {
    console.error(e);
    alert("Erro ao conectar com o motor de cotação.");
    btn.innerText = "Enviar Pedido";
    btn.disabled = false;
  }
}

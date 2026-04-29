// NOVO CÓDIGO INSERIDO AQUI - 28/04/2026 23:00
const URL_BACKEND = "https://multiplus-cotador-ia.onrender.com"; 

// --- CONTROLE DE NAVEGAÇÃO ---
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

// --- FLUXO DE UPLOAD E INTELIGÊNCIA ARTIFICIAL ---
function handleFile(input) {
  const file = input.files[0];
  if (file) {
    if (file.type !== "application/pdf") {
      alert("Erro: Por favor, selecione apenas arquivos PDF.");
      input.value = "";
      return;
    }
    document.getElementById('fileName').innerText = "Arquivo: " + file.name;
    document.getElementById('uploadText').innerText = "Documento carregado!";
    document.getElementById('btnSendPdf').style.display = 'inline-block';
  }
}

async function sendPdf() {
  const fileInput = document.getElementById('pdfInput');
  if (!fileInput.files[0]) return;

  const btn = document.getElementById('btnSendPdf');
  btn.innerText = "IA Analisando & Robô em Ação...";
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
      
      // Exibição dos dados capturados (Layout Original)
      document.getElementById('dadosExtraidos').style.display = 'block';
      document.getElementById('msgSucesso').innerText = "Processamento concluído com sucesso!";
      
      document.getElementById('resNome').innerText = res.dados.nome || "Não encontrado";
      document.getElementById('resCpf').innerText = res.dados.cpf || "Não encontrado";
      document.getElementById('resPlaca').innerText = res.dados.placa || "Não encontrado";
      document.getElementById('resStatusRobo').innerText = res.automacao.status || "Erro no Robô";
    } else {
      throw new Error(res.detail || "Erro de servidor");
    }
  } catch (error) {
    console.error("Erro na comunicação:", error);
    alert("Ocorreu um erro na comunicação com o motor de IA.");
  } finally {
    btn.innerText = "Iniciar Análise por IA";
    btn.disabled = false;
  }
}

// --- FLUXO MANUAL (WIZARD) ---
function avancarPasso(p) {
  // Validação básica do Passo 1
  if (p === 2) {
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value;
    if (!nome || !cpf) {
      alert("Nome e CPF são obrigatórios para prosseguir.");
      return;
    }
  }

  document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step-' + p).classList.add('active');
  
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

// --- ENVIO DO FORMULÁRIO MANUAL ---
async function enviarCotacaoManual() {
  const pacote = document.getElementById('pacoteSelecionado').value;
  if (!pacote) {
    alert("Selecione um plano de cobertura.");
    return;
  }

  const btn = document.getElementById('btnFinalizar');
  btn.innerText = "Acionando Robô...";
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
      document.getElementById('msgSucesso').innerText = "Seus dados manuais foram enviados ao robô com sucesso.";
    } else {
      throw new Error("Falha no servidor");
    }
  } catch (e) {
    console.error(e);
    alert("Erro ao conectar com o servidor.");
    btn.innerText = "Enviar Pedido";
    btn.disabled = false;
  }
}

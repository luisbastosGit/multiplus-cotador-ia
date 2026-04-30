// NOVO CÓDIGO INSERIDO AQUI - 30/04/2026 14:30
// A URL agora aponta para o motor-multiplus-docker, que é o seu backend real.
const URL_BACKEND = "https://motor-multiplus-docker.onrender.com"; 

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
  btn.innerText = "IA Analisando Documento...";
  btn.disabled = true;

  const formData = new FormData();
  formData.append('arquivo_pdf', fileInput.files[0]);

  try {
    // Bate no endpoint /cotar-ia que agora existe no backend
    const response = await fetch(`${URL_BACKEND}/cotar-ia`, {
      method: 'POST',
      body: formData
    });
    
    const res = await response.json();
    
    if (response.ok) {
      document.getElementById('stepUpload').style.display = 'none';
      document.getElementById('telaSucesso').style.display = 'block';
      document.getElementById('dadosExtraidos').style.display = 'block';
      
      document.getElementById('resNome').innerText = res.dados.nome || "Não encontrado";
      document.getElementById('resCpf').innerText = res.dados.cpf || "Não encontrado";
      document.getElementById('resPlaca').innerText = res.dados.placa || "Não encontrado";
      document.getElementById('resStatusRobo').innerText = "Delegado à Extensão Local";
      document.getElementById('msgSucesso').innerText = "Processamento concluído com sucesso!";

      // DISPARA SINAL PARA A EXTENSÃO
      const eventoExtensao = new CustomEvent("AcionarRoboMultiplus", { detail: res.dados });
      window.dispatchEvent(eventoExtensao);

    } else {
      throw new Error(res.detail || "Erro de servidor");
    }
  } catch (error) {
    console.error("Erro na comunicação:", error);
    alert("Ocorreu um erro na comunicação com o motor de IA. Verifique se o backend está rodando no Render.");
  } finally {
    btn.innerText = "Iniciar Análise por IA";
    btn.disabled = false;
  }
}

function avancarPasso(p) {
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

async function enviarCotacaoManual() {
  const pacote = document.getElementById('pacoteSelecionado').value;
  if (!pacote) {
    alert("Selecione um plano de cobertura.");
    return;
  }

  const btn = document.getElementById('btnFinalizar');
  btn.innerText = "Acionando Robô Local...";
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
    // Bate no endpoint /enviar-cotacao que agora existe no backend
    const response = await fetch(`${URL_BACKEND}/enviar-cotacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });

    if (response.ok) {
      document.getElementById('formManual').style.display = 'none';
      document.getElementById('telaSucesso').style.display = 'block';
      document.getElementById('dadosExtraidos').style.display = 'none';
      document.getElementById('msgSucesso').innerText = "Dados enviados para a Extensão!";
      
      // DISPARA SINAL PARA A EXTENSÃO MANUALMENTE
      const eventoExtensao = new CustomEvent("AcionarRoboMultiplus", { detail: dados });
      window.dispatchEvent(eventoExtensao);
    }
  } catch (e) {
    alert("Erro ao conectar com o servidor.");
  } finally {
    btn.innerText = "Enviar Pedido";
    btn.disabled = false;
  }
}

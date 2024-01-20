var mapa;
var autocomplete;
var marcadores = []; // Array para armazenar os marcadores


function initMap() {
    if (typeof google !== 'undefined' && google.maps) {
        // Tenta obter a localização do usuário...
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                
                // Obtém as coordenadas da localização do usuário...
                var userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // Configurações do mapa
                    
                

                // Cria o mapa usando Google Maps e centraliza na localização do usuário...
                mapa = new google.maps.Map(document.getElementById('mapa'), {
                    center: userLocation,
                    zoom: 14, // Ajuste o nível de zoom conforme necessário
                
                    // Configurações do estilo do mapa para desativar os marcadores padrão
                    styles: [
                        {
                            featureType: 'poi',
                            elementType: 'labels.icon',
                            stylers: [{ visibility: 'off' }]
                        }
                    ]
                });

                // Adiciona um marcador na localização do usuário...
                var marker = new google.maps.Marker({
                    position: userLocation,
                    map: mapa,
                    title: 'Estou Aqui'
                });

                // Inicializa a função de autocomplete...
                initAutocomplete();
            }, function (error) {
                console.log('Erro ao obter a localização do usuário:', error);
                initAutocomplete(); // Inicializa a função de autocomplete mesmo em caso de erro
            }, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 30000
            });
        } else {
            console.log('Seu navegador não suporta geolocalização.');
            initAutocomplete(); // Inicializa a função de autocomplete mesmo se a geolocalização não for suportada
        }
    } else {
        setTimeout(initMap, 100);
    }
}

function initAutocomplete() {
    if (google.maps.places) {
        var input = document.getElementById('id_endereco');
        autocomplete = new google.maps.places.Autocomplete(input);
        // Configurações adicionais do Autocomplete aqui...
        autocomplete.addListener('place_changed', function () {
            var place = autocomplete.getPlace();
            if (place.geometry) {
                adicionarMarcador(place.geometry.location, place.formatted_address);
                limparInputEndereco();

            }
        });
    }
}

// Inicialize o contador global
// var proximoNumeroMarcador = 1;

function adicionarMarcador(localizacao, endereco) {
    if (mapa) {
        // Obtém o último ID na tabela de endereços
        var ultimoIdTabela = obterUltimoIdNaTabela();

        // Inicia o próximo número disponível como o maior ID na tabela
        var numeroMarcador = ultimoIdTabela ? ultimoIdTabela + 1 : 1;

        var marker = new google.maps.Marker({
            position: localizacao,
            map: mapa,
            title: endereco,
            animation: google.maps.Animation.DROP,
            label: numeroMarcador.toString(),
            id: numeroMarcador
        });

        marker.setAnimation(google.maps.Animation.DROP);

        var infoWindow = new google.maps.InfoWindow({
            content: 'Marcador #' + numeroMarcador + '<br>Endereço: ' + endereco
        });

        marker.addListener('click', function () {
            infoWindow.open(mapa, marker);
        });

        mapa.panTo(localizacao);

        marcadores.push(marker);

        // Atualiza a variável global para o próximo número de marcador
        proximoNumeroMarcador = numeroMarcador + 1;

        // Obter números atuais dos marcadores em um array
        var numerosMarcadoresAtuais = marcadores.map(function(marcador) {
            return { id: marcador.id, idEndereco: marcador.idEndereco };
        });

        // Exibir os números dos marcadores no console
        console.log('linha-117: Números dos Marcadores Atuais:', numerosMarcadoresAtuais);

        adicionarEntradaTabela(numeroMarcador, endereco);
        var valoresTabelaEnderecos = obterValoresTabelaEnderecos();

        document.getElementById('sugestoes-lista').innerHTML = '';
    }
}

// Função para verificar se um marcador com o ID já existe
function marcadorComIdExiste(id) {
    return marcadores.some(function (marcador) {
        return marcador.id === id;
    });
}


function limparInputEndereco() {
    document.getElementById('id_endereco').value = '';
    document.getElementById('sugestoes-lista').innerHTML = '';
}


// Função para atualizar a numeração dos marcadores
function atualizarNumeracaoMarcadores() {
    for (var i = 0; i < marcadores.length; i++) {
        var novoIdMarcador = i + 1;
        var novoLabel = novoIdMarcador.toString();

        // Atualiza o rótulo do marcador
        marcadores[i].setLabel(novoLabel);

        // Atualiza o ID na tabela
        document.getElementById('tabela-enderecos').rows[i + 1].cells[0].innerText = novoIdMarcador;
    }
}
  
 

// Função para excluir um endereço
function excluirEndereco(valor) {
   console.log(`linha-203: Excluindo endereço com ID: ${valor}`);
    
   // Encontrar o índice do marcador com base no valor do ID
   var indiceMarcador = marcadores.findIndex(function (marcador) {
       return marcador.id == valor;
   });

   // Verifica se o marcador com o ID especificado foi encontrado
   if (indiceMarcador !== -1) {
       // Remove o marcador do mapa
       var marcadorExcluir = marcadores[indiceMarcador];
       if (marcadorExcluir) {
           marcadorExcluir.setMap(null);
       }
       // Remove o marcador do array
       marcadores.splice(indiceMarcador, 1);
       // Atualiza a tabela de endereços
       atualizarTabelaEnderecos();

       // Atualiza a numeração dos marcadores restantes
       atualizarNumeracaoMarcadores();
   } else {
       // O marcador com o ID especificado não foi encontrado
       console.log(`O marcador com o ID ${valor} não foi encontrado.`);
    }
}
  
  
// Função para atualizar a tabela de endereços após a exclusão de um marcador
function atualizarTabelaEnderecos() {
    var tabela = document.getElementById('tabela-enderecos');
    tabela.innerHTML = ''; // Limpa a tabela

    // Adiciona os cabeçalhos da tabela
    var headerRow = tabela.insertRow(0);
    headerRow.insertCell(0).innerHTML = 'ID';
    headerRow.insertCell(1).innerHTML = 'Endereço';

    // Adiciona os dados da tabela com base nos marcadores restantes
    for (var i = 0; i < marcadores.length; i++) {
        adicionarEntradaTabela(marcadores[i].id, marcadores[i].title);
    }
}




function limparInputEndereco() {
    document.getElementById('id_endereco').value = '';
    document.getElementById('sugestoes-lista').innerHTML = '';
}



// Função para Adicionar entrada na Tabela Enderecos
function adicionarEntradaTabela(id, endereco) {
    var tabela = document.getElementById('tabela-enderecos');

    // Calcula o próximo ID com base no maior ID existente na tabela
    var novoId = obterMaiorIdNaTabela() + 1;

    var novaLinha = tabela.insertRow(-1);
    var celulaId = novaLinha.insertCell(0);
    var celulaEndereco = novaLinha.insertCell(1);
    var celulaExclusao = novaLinha.insertCell(2);

    celulaId.innerHTML = novoId;
    celulaEndereco.innerHTML = endereco;

    // Adiciona o ID invisível na célula
    celulaEndereco.classList.add('id-hidden');
    celulaEndereco.dataset.id = novoId;

    // Botão de exclusão
    var botaoExcluir = document.createElement('button');
    botaoExcluir.innerHTML = 'Excluir';

    botaoExcluir.onclick = function () {
        excluirEndereco(id); // Chame a função para excluir o endereço aqui
        atualizarNumeracaoMarcadores();
    };

    celulaExclusao.appendChild(botaoExcluir);
}

function excluirEndereco(valor) {
    console.log(`linha-203: Excluindo endereço com ID: ${valor}`);
    // Função para excluir um endereço com base no ID
    var tabela = document.getElementById('tabela-enderecos');
    var linhas = tabela.getElementsByTagName('tr');

    // Encontrar o índice do marcador com base no valor do ID
    var indiceMarcador = marcadores.findIndex(function (marcador) {
        return marcador.id == valor;
    });

    // Verifica se o marcador com o ID especificado foi encontrado
    if (indiceMarcador !== -1) {
        // Exclui a linha selecionada
        tabela.deleteRow(indiceMarcador + 1); // +1 para compensar o cabeçalho

        // Remove o marcador do mapa
        var marcadorExcluir = marcadores[indiceMarcador];
        if (marcadorExcluir) {
            marcadorExcluir.setMap(null); // Remover o marcador do mapa
            marcadores.splice(indiceMarcador, 1); // Remover o marcador do array
        }

        // Atualiza a numeração dos marcadores restantes
        atualizarNumeracaoMarcadores(marcadores.map(function (marcador) {
            return { id: marcador.id, idEndereco: marcador.idEndereco };
        }));
    } else {
        // O marcador com o ID especificado não foi encontrado
        console.log(`O marcador com o ID ${valor} não foi encontrado.`);
    }
}



// Função para obter o maior ID na tabela
function obterMaiorIdNaTabela() {
    var tabela = document.getElementById('tabela-enderecos');
    var linhas = tabela.getElementsByTagName('tr');
    
    var maiorId = 0;

    // Verifica se há linhas na tabela
    if (linhas.length > 0) {
        for (var i = 0; i < linhas.length; i++) {
            var celulaId = linhas[i].cells[0];
            var idAtual = parseInt(celulaId.innerHTML);

            // Atualiza o maior ID se o ID atual for maior
            if (idAtual > maiorId) {
                maiorId = idAtual;
            }
        }
    }

    return maiorId;
}

// Função para obter o último ID na tabela
function obterUltimoIdNaTabela() {
    var tabela = document.getElementById('tabela-enderecos');
    var linhas = tabela.getElementsByTagName('tr');
    
    // Verifica se há linhas na tabela
    if (linhas.length > 0) {
        var ultimaLinha = linhas[linhas.length - 1];
        var celulaId = ultimaLinha.cells[0];

        // Retorna o ID da última linha
        return parseInt(celulaId.innerHTML);
    } else {
        // Se não há linhas, retorna null indicando que não há IDs existentes

        return 1;
    }
}

// Função para Gerar proximo ID
function obterProximoId() {
    var tabela = document.getElementById('tabela-enderecos');
    var idsExistentes = [];

    for (var i = 1; i < tabela.rows.length; i++) {
        var row = tabela.rows[i];
        var id = parseInt(row.cells[0].innerHTML);
        idsExistentes.push(id);
    }

    // Se não houver IDs existentes, comece com 1, caso contrário, use o próximo número disponível
    return idsExistentes.length > 0 ? Math.max(...idsExistentes) + 1 : 1;
}





// Função para atualizar a ordem de numeração da Tabela de enderecos
function atualizarNumeracaoTabelaEnderecos() {
    // Atualiza a numeração dos IDs da tabela de endereços
    var tabela = document.getElementById('tabela-enderecos');
    var linhas = tabela.getElementsByTagName('tr');

    for (var i = 1; i < linhas.length; i++) {
        var celulas = linhas[i].getElementsByTagName('td');
        if (celulas.length > 0) {
            celulas[0].innerHTML = i; // Atualiza o ID
            console.log(`Atualizando ID na linha ${i} para ${i}`);
            atualizarNumeracaoMarcadores()
        }
    }
}



async function buscarEndereco() {
    try {
        await carregarAPIAutocompletar();
        var enderecoInput = document.getElementById('id_endereco').value;
        var predictions = await obterSugestoesEndereco(enderecoInput);
        
        if (predictions.length > 0) {
            exibirListaSugestoes(predictions);
        } else {
            buscarEnderecoDireto();
        }
    } catch (error) {
        console.error('Erro ao buscar endereço:', error);
    }
}

async function carregarAPIAutocompletar() {
    if (!autocomplete) {
        await loadScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyAl4N-KtLVFhvzJ6MuDua1CbN0LJSEBH1U&libraries=places');
        initAutocomplete();
    }
}

function loadScript(src) {
    return new Promise((resolve, reject) => {
        var script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

async function obterSugestoesEndereco(input) {
    return new Promise((resolve, reject) => {
        var service = new google.maps.places.AutocompleteService();
        service.getPlacePredictions(
            {
                input: input,
                componentRestrictions: { country: 'br' },
            },
            (predictions, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && predictions) {
                    resolve(predictions);
                } else {
                    reject('Erro ao obter sugestões de endereço.');
                }
            }
        );
    });
}

// Adiciona a função calcularRota ao escopo global
window.calcularRota = function () {
    var directionsService = new google.maps.DirectionsService();

    // Criar array de waypoints a partir dos marcadores
    var waypoints = marcadores.map(function (marcador) {
        return {
            location: marcador.position,
            stopover: true
        };
    });

    // Verificar se o usuário forneceu um endereço de início
    var enderecoInicio = document.getElementById('endereco-inicio').value;

    if (enderecoInicio.trim() !== '') {
        // Se o usuário forneceu um endereço de início, use-o
        var request = {
            origin: enderecoInicio,
            destination: marcadores[marcadores.length - 1].position,
            waypoints: waypoints,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.DRIVING
        };
    } else {

        // Se o usuário não forneceu um endereço de início, use a localização atual do usuário
        var request = {
            origin: marcadores[0].position,
            destination: marcadores[marcadores.length - 1].position,
            waypoints: waypoints,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.DRIVING
        };
    }

    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            var directionsRenderer = new google.maps.DirectionsRenderer({
                map: mapa,
                directions: result
            });

            // Atualizar a tabela com a sequência otimizada
            atualizarTabelaSequencia(result);

            // Exemplo de uso
            var valoresTabelaEnderecos = obterValoresTabelaEnderecos();
            var ValoresTabelaOtimizada = obterValoresTabelaOtimizada();
            console.log('linha-347:  O valor da var é:', ValoresTabelaOtimizada)
            

        } else {
            alert('Não foi possível calcular a rota: ' + status);
        }
    });
};


// Função para adicionar endereços otimizados
function adicionarEnderecosOtimizados(directionsResult) {
    var ordemOtimizada = directionsResult.routes[0].waypoint_order;
    var tabelaOtimizada = document.getElementById('tabela-enderecos-otimizada');
    
    for (var i = 0; i < ordemOtimizada.length; i++) {
        var index = ordemOtimizada[i];
        var endereco = marcadores[index].title;
        var idEndereco = marcadores[index].id;
        
        // Adicionar entrada à tabela otimizada
        adicionarEntradaTabelaOtimizada(i + 1, endereco);

        // Atualizar o marcador existente com nova posição e rótulo
        atualizarMarcador(marcadores[index], i + 1, idEndereco);
    }
}


// Função para atualizar marcadores
function atualizarMarcador(marker, indiceLinha, endereco) {
    // Remove o marcador do mapa
    marker.setMap(null);

    // Atualizar rótulo do marcador
    marker.setLabel(indiceLinha.toString());

    // Adicionar uma janela de informações atualizada
    var infoWindow = new google.maps.InfoWindow({
        content: 'Marcador #' + indiceLinha + '<br>Endereço: ' + endereco
    });

    // Atualiza a numeração dos marcadores restantes
    var valoresTabelaEnderecos = obterValoresTabelaEnderecos(); // Certifique-se de obter os valores corretos
    var numerosMarcadoresAtuais = valoresTabelaEnderecos.map(function (valor) {
        return parseInt(valor.id);
    });

    atualizarNumeracaoMarcadores(numerosMarcadoresAtuais);

    marker.addListener('click', function () {
        infoWindow.open(mapa, marker);
    });
}


// Função para a realizar entreada na tabela otimizada
function adicionarEntradaTabelaOtimizada(id, endereco) {
    var tabelaOtimizada = document.getElementById('tabela-enderecos-otimizada');
    var novaLinha = tabelaOtimizada.insertRow(-1);
    var celulaId = novaLinha.insertCell(0);
    var celulaEndereco = novaLinha.insertCell(1);
    var celulaSequencia = novaLinha.insertCell(2);

    celulaId.innerHTML = id;
    celulaEndereco.innerHTML = endereco;
    celulaSequencia.innerHTML = id; // Sequência começa em 1

    // Adicionar o ID do endereço como um atributo personalizado da linha
    // novaLinha.setAttribute('data-id-endereco', idEndereco);
}



function atualizarTabelaSequencia(directionsResult) {
    // Verificar se a resposta possui rotas e se há uma ordem otimizada de waypoints
    if (directionsResult.routes && directionsResult.routes.length > 0 && directionsResult.routes[0].waypoint_order) {
        var ordemOtimizada = directionsResult.routes[0].waypoint_order;

        // Obter os valores da tabela de endereços
        var valoresTabelaEnderecos = obterValoresTabelaEnderecos();

        

        // Atualizar a tabela com a sequência otimizada
        var tabelaEnderecosOtimizada = document.getElementById('tabela-otimizada');
        
        for (var i = 0; i < ordemOtimizada.length; i++) {
            var index = ordemOtimizada[i];
            var row = tabelaEnderecosOtimizada.insertRow(-1);
            var cellIdEndereco = row.insertCell(0);
            var cellEndereco = row.insertCell(1);
            var cellSequencia = row.insertCell(2);

            cellIdEndereco.innerHTML = valoresTabelaEnderecos[index].idEndereco;
            cellEndereco.innerHTML = valoresTabelaEnderecos[index].endereco;
            cellSequencia.innerHTML = i + 1; // Sequência começa em 1
        }
    } else {
        console.error('Não foi possível obter a ordem otimizada dos waypoints na resposta da API.');
        return;
    }
}

function obterValoresTabelaEnderecos() {
    var tabelaEnderecos = document.getElementById('tabela-enderecos');
    var valores = [];

    for (var i = 1; i < tabelaEnderecos.rows.length; i++) {
        var row = tabelaEnderecos.rows[i];
        var idEndereco = row.cells[0].innerHTML;
        var endereco = row.cells[1].innerHTML;

        valores.push({
            idEndereco: idEndereco,
            endereco: endereco
        });
    }

    return valores;
}


function obterValoresTabelaOtimizada() {
    var tabelaOtimizada = document.getElementById('tabela-otimizada');
    var valores = [];

    for (var i = 1; i < tabelaOtimizada.rows.length; i++) {
        var row = tabelaOtimizada.rows[i];
        var idEndereco = row.cells[0].innerHTML;
        var endereco = row.cells[1].innerHTML;
        var parada = row.cells[2].innerHTML;

        valores.push({
            idEndereco: idEndereco,
            endereco: endereco,
            parada: parada
        });
    }
    
    return valores;
}

function imprimirRota() {
    // Obtenha a referência à div
    var tabela = obterValoresTabelaOtimizada();
    var quant_parada = tabela.length

    // Inicie a string HTML com o cabeçalho da tabela
    var htmlTabela = `
        <table border="1" id="tabela-otimizada" name="tabela-otimizada" style="color: black;">
            <caption>Paradas Otimizada</caption>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Endereço</th>
                    <th>Parada</th>
                </tr>
            </thead>

            <tbody>
    `;

    // Adicione linhas à string HTML com base nos valores da tabela
    for (var i = 0; i < quant_parada; i++) {
        var idEndereco = tabela[i].idEndereco;
        var endereco = tabela[i].endereco;
        var parada = tabela[i].parada;

        // Adicione cada linha à string HTML
        htmlTabela += `
            <tr>
                <td>${idEndereco}</td>
                <td>${endereco}</td>
                <td>${parada}</td>
                
            </tr>
        `;

        
    }

    // Finalize a string HTML
    htmlTabela += `
            </tbody>
        </table>
    `;


    // Configurações para o PDF
    var opt = {
        margin: 1,
        filename: "Rota.pdf",
        html2canvas: { scale: 2 },
        jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
        fontOptions: {
            textColor: [0, 0, 0] // Define a cor da fonte como preto (RGB)
        }
    };

    // Gere o PDF
    html2pdf().set(opt).from(htmlTabela).save();
    // Exiba as informações do loop no console
    for (var i = 0; i < quant_parada; i++) {
        console.log(`Loop ${i + 1} - ID: ${idEndereco}, Endereço: ${endereco}, Parada: ${parada}`);
}



// Função para obter o valor de um cookie pelo nome
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}}
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

function adicionarMarcador(localizacao, endereco) {
    if (mapa) {
        var numeroMarcador = marcadores.length + 1; // Número sequencial do marcador
        var marker = new google.maps.Marker({
            position: localizacao,
            map: mapa,
            title: endereco,
            animation: google.maps.Animation.DROP,
            label: (marcadores.length + 1).toString(), // Adiciona a numeração ao marcador
        });

        marker.setAnimation(google.maps.Animation.DROP);

        // Ou adicione uma janela de informações (info window)
        var infoWindow = new google.maps.InfoWindow({
            content: 'Marcador #' + numeroMarcador + '<br>Endereço: ' + endereco
        });

        marker.addListener('click', function () {
            infoWindow.open(mapa, marker);
        });

        // Pode adicionar mais personalizações ao marcador, se necessário
        // Exemplo: marker.setIcon('caminho/do/ícone.png');
        // ...

        // Centraliza o mapa na nova localização
        mapa.panTo(localizacao);

        // Adiciona o marcador ao array
        marcadores.push(marker);

        // Adiciona entrada à tabela
        adicionarEntradaTabela(numeroMarcador, endereco);
        var valoresTabelaEnderecos = obterValoresTabelaEnderecos();
        console.log('linha-114: Enderecos Adicionado:',valoresTabelaEnderecos);
        
        // Limpa a lista de sugestões
        document.getElementById('sugestoes-lista').innerHTML = '';
    }
}

function limparInputEndereco() {
    document.getElementById('id_endereco').value = '';
    document.getElementById('sugestoes-lista').innerHTML = '';
}

function adicionarEntradaTabela(numero, endereco) {
    var tabela = document.getElementById('tabela-enderecos');
    var novaLinha = tabela.insertRow(-1);
    var celulaNumero = novaLinha.insertCell(0);
    var celulaEndereco = novaLinha.insertCell(1);

    celulaNumero.innerHTML = numero;
    celulaEndereco.innerHTML = endereco;
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

// Adicione a função calcularRota ao escopo global
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
            console.log('linha-238: tabela Enderecos Não Otimizada:',valoresTabelaEnderecos);
            var ValoresTabelaOtimizada = obterValoresTabelaOtimizada();
            console.log('linha-240: tabela Enderecos Otimizada:', ValoresTabelaOtimizada);

        } else {
            alert('Não foi possível calcular a rota: ' + status);
        }
    });
};

function adicionarEnderecosOtimizados(directionsResult) {
    var ordemOtimizada = directionsResult.routes[0].waypoint_order;
    var tabelaOtimizada = document.getElementById('tabela-enderecos-otimizada');
    console.log(tabelaOtimizada)
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

function atualizarMarcador(marker, numero, endereco) {
    // Atualizar posição do marcador
    marker.setPosition(marker.position);

    // Atualizar rótulo do marcador
    marker.setLabel(numero.toString());

    // Adicionar uma janela de informações atualizada
    var infoWindow = new google.maps.InfoWindow({
        content: 'Marcador #' + numero + '<br>Endereço: ' + endereco
    });

    marker.addListener('click', function () {
        infoWindow.open(mapa, marker);
    });
}

function adicionarEntradaTabelaOtimizada(numero, endereco) {
    var tabelaOtimizada = document.getElementById('tabela-enderecos-otimizada');
    var novaLinha = tabelaOtimizada.insertRow(-1);
    var celulaNumero = novaLinha.insertCell(0);
    var celulaEndereco = novaLinha.insertCell(1);
    var celulaSequencia = novaLinha.insertCell(2);

    celulaNumero.innerHTML = numero;
    celulaEndereco.innerHTML = endereco;
    celulaSequencia.innerHTML = numero; // Sequência começa em 1

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
    console.log(quant_parada)
    console.log(tabela);

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

        // Exiba as informações do loop no console
        console.log(`Loop ${i + 1} - ID: ${idEndereco}, Endereço: ${endereco}, Parada: ${parada}`);
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
}
}